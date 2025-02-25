from Bio import pairwise2
import re
import hashlib
from datetime import datetime
from tqdm import tqdm
import pandas as pd
import numpy as np
from .SeqMats import SeqMat, MutSeqMat
from .splicing_utils import find_transcript_missplicing_seqs, develop_aberrant_splicing, Missplicing
from .Gene import Gene
import copy
from . import config

from .tis_utils import find_tis

def short_hash_of_list(numbers, length=5):
    encoded = repr(numbers).encode('utf-8')
    full_hash = hashlib.sha256(encoded).hexdigest()
    return full_hash[:length]

def find_continuous_gaps(sequence):
    """Find continuous gap sequences in an alignment."""
    return [(m.start(), m.end()) for m in re.finditer(r'-+', sequence)]

def get_logical_alignment(ref_prot, var_prot):
    """
    Aligns two protein sequences and finds the optimal alignment with the least number of gaps.

    Parameters:
    ref_prot (str): Reference protein sequence.
    var_prot (str): Variant protein sequence.

    Returns:
    tuple: Optimal alignment, number of insertions, and number of deletions.
    """

    if var_prot == '':
        print("here")
        var_prot = ref_prot[0]

    # Perform global alignment
    alignments = pairwise2.align.globalms(ref_prot, var_prot, 1, -1, -3, 0, penalize_end_gaps=(True, True))
    if len(alignments) == 0:
        print(ref_prot, var_prot)
        print(alignments)

    # Selecting the optimal alignment
    if len(alignments) > 1:
        # Calculate continuous gaps for each alignment and sum their lengths
        gap_lengths = [sum(end - start for start, end in find_continuous_gaps(al.seqA) + find_continuous_gaps(al.seqB))
                       for al in alignments]
        optimal_alignment = alignments[gap_lengths.index(min(gap_lengths))]
    else:
        optimal_alignment = alignments[0]

    return optimal_alignment


def find_indels_with_mismatches_as_deletions(seqA, seqB):
    """
    Identify insertions and deletions in aligned sequences, treating mismatches as deletions.

    Parameters:
    seqA, seqB (str): Aligned sequences.

    Returns:
    tuple: Two dictionaries containing deletions and insertions.
    """
    if len(seqA) != len(seqB):
        raise ValueError("Sequences must be of the same length")

    mapperA, counter = {}, 0
    for i, c in enumerate(list(seqA)):
        if c != '-':
            counter += 1
        mapperA[i] = counter

    mapperB, counter = {}, 0
    for i, (c1, c2) in enumerate(list(zip(seqA, seqB))):
        if c2 != '-':
            counter += 1
        mapperB[i] = counter

    seqA_array, seqB_array = np.array(list(seqA)), np.array(list(seqB))

    # Find and mark mismatch positions in seqB
    mismatches = (seqA_array != seqB_array) & (seqA_array != '-') & (seqB_array != '-')
    seqB_array[mismatches] = '-'
    modified_seqB = ''.join(seqB_array)

    gaps_in_A = find_continuous_gaps(seqA)
    gaps_in_B = find_continuous_gaps(modified_seqB)

    insertions = {mapperB[start]: modified_seqB[start:end].replace('-', '') for start, end in gaps_in_A if
                  seqB[start:end].strip('-')}
    deletions = {mapperA[start]: seqA[start:end].replace('-', '') for start, end in gaps_in_B if
                 seqA[start:end].strip('-')}

    return deletions, insertions


def parabolic_window(window_size):
    """Create a parabolic window function with a peak at the center."""
    x = np.linspace(-1, 1, window_size)
    return 0.9 * (1 - x ** 2) + 0.1


def transform_conservation_vector(conservation_vector, window=13, factor=4):
    """
    Transforms a 1D conservation vector using different parameters.

    Args:
        conservation_vector (numpy.ndarray): Input 1D vector of conservation values.

    Returns:
        numpy.ndarray: A matrix containing transformed vectors.
    """
    # window = 13
    # factor = 4
    convolving_window = parabolic_window(window)
    transformed_vector = np.convolve(conservation_vector, convolving_window, mode='same') / np.sum(convolving_window)
    assert len(transformed_vector) == len(conservation_vector), f"Len Ref: {len(conservation_vector)}, Len New: {len(transformed_vector)}"
    # Compute exponential factors
    exp_factors = np.exp(-transformed_vector * factor)

    # Normalize and scale exponential factors
    # exp_factors /= exp_factors.sum()
    return exp_factors


def find_modified_positions(sequence_length, deletions, insertions, reach_limit=16):
    """
    Identify unmodified positions in a sequence given deletions and insertions.

    :param sequence_length: Length of the sequence.
    :param deletions: Dictionary of deletions.
    :param insertions: Dictionary of insertions.
    :param reach_limit: Limit for considering the effect of insertions/deletions.
    :return: Array indicating unmodified positions.
    """
    unmodified_positions = np.zeros(sequence_length, dtype=float)

    for pos, deletion in deletions.items():
        deletion_length = len(deletion)
        unmodified_positions[pos:pos + deletion_length] = 1

    for pos, insertion in insertions.items():
        reach = min(len(insertion) // 2, reach_limit)
        front_end, back_end = max(0, pos - reach), min(sequence_length, pos + reach)
        # len_start, len_end = pos - front_end, back_end - pos + 1
        # gradient_front = np.linspace(0, 1, len_start, endpoint=False)
        # gradient_back = np.linspace(0, 1, len_end, endpoint=True)[::-1]
        # combined_gradient = np.concatenate([gradient_front, gradient_back])  #np.array([1]),
        # print(len(unmodified_positions[front_end:back_end]), len(combined_gradient))
        unmodified_positions[front_end:back_end] = 1 #combined_gradient

    return unmodified_positions


def calculate_penalty(domains, cons_scores, W, is_insertion=False):
    """
    Calculate the penalty for mutations (either insertions or deletions) on conservation scores.

    :param domains: Dictionary of mutations (inserted or deleted domains).
    :param cons_scores: Conservation scores.
    :param W: Window size.
    :param is_insertion: Boolean flag to indicate if the mutation is an insertion.
    :return: Penalty array.
    """
    penalty = np.zeros(len(cons_scores))
    for pos, seq in domains.items():
        mutation_length = len(seq)
        weight = max(1.0, mutation_length / W)

        if is_insertion:
            reach = min(W // 2, mutation_length // 2)
            penalty[pos - reach:pos + reach] = weight * cons_scores[pos - reach:pos + reach]
        else:  # For deletion
            penalty[pos:pos + mutation_length] = cons_scores[pos:pos + mutation_length] * weight

    return penalty


def calculate_legacy_oncosplice_score(deletions, insertions, cons_vec, W):
    """
    Calculate the legacy Oncosplice score based on deletions, insertions, and conservation vector.

    :param deletions: Dictionary of deletions.
    :param insertions: Dictionary of insertions.
    :param cons_vec: Conservation vector.
    :param W: Window size.
    :return: Legacy Oncosplice score.
    """
    smoothed_conservation_vector = np.exp(np.negative(moving_average_conv(cons_vec, W, 2)))
    del_penalty = calculate_penalty(deletions, smoothed_conservation_vector, W, is_insertion=False)
    ins_penalty = calculate_penalty(insertions, smoothed_conservation_vector, W, is_insertion=True)
    combined_scores = del_penalty + ins_penalty
    return np.max(np.convolve(combined_scores, np.ones(W), mode='same'))


def moving_average_conv(vector, window_size, factor=1):
    """
    Calculate the moving average convolution of a vector.

    Parameters:
    vector (iterable): Input vector (list, tuple, numpy array).
    window_size (int): Size of the convolution window. Must be a positive integer.
    factor (float): Scaling factor for the average. Default is 1.

    Returns:
    numpy.ndarray: Convolved vector as a numpy array.
    """
    if not isinstance(vector, (list, tuple, np.ndarray)):
        raise TypeError("vector must be a list, tuple, or numpy array")
    if not isinstance(window_size, int) or window_size <= 0:
        raise ValueError("window_size must be a positive integer")
    if len(vector) < window_size:
        raise ValueError("window_size must not be greater than the length of vector")
    if factor == 0:
        raise ValueError("factor must not be zero")

    return np.convolve(vector, np.ones(window_size), mode='same') / window_size

def find_splice_site_proximity(pos, transcript):
    for i, (ex_start, ex_end) in enumerate(transcript.exons):
        if min(ex_start, ex_end) <= pos <= max(ex_start, ex_end):
            return i + 1, None, abs(pos - ex_start), abs(pos - ex_end)

    for i, (in_start, in_end) in enumerate(transcript.introns):
        if min(in_start, in_end) <= pos <= max(in_start, in_end):
            return None, i + 1, abs(pos - in_end), abs(pos - in_start)

    return None, None, np.inf, np.inf

def define_missplicing_events(ref, var):
    ref_introns, ref_exons = ref.introns, ref.exons
    var_introns, var_exons = var.introns, var.exons

    num_ref_exons = len(ref_exons)
    num_ref_introns = len(ref_introns)

    partial_exon_skipping = ','.join(
        [f'Exon {exon_count + 1}/{num_ref_exons} truncated: {(t1, t2)} --> {(s1, s2)}' for (s1, s2) in var_exons for
         exon_count, (t1, t2) in enumerate(ref_exons)
         if (not ref.rev and ((s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)))
         or (ref.rev and ((s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)))])

    partial_intron_retention = ','.join(
        [f'Intron {intron_count + 1}/{num_ref_introns} partially retained: {(t1, t2)} --> {(s1, s2)}' for (s1, s2)
         in var_introns for intron_count, (t1, t2) in enumerate(ref_introns)
         if (not ref.rev and ((s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)))
         or (ref.rev and ((s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)))])

    exon_skipping = ','.join(
        [f'Exon {exon_count + 1}/{num_ref_exons} skipped: {(t1, t2)}' for exon_count, (t1, t2) in enumerate(ref_exons)
         if t1 not in var.acceptors and t2 not in var.donors])

    novel_exons = ','.join([f'Novel Exon: {(t1, t2)}' for (t1, t2) in var_exons if
                            t1 not in ref.acceptors and t2 not in ref.donors])

    intron_retention = ','.join(
        [f'Intron {intron_count + 1}/{num_ref_introns} retained: {(t1, t2)}' for intron_count, (t1, t2) in
         enumerate(ref_introns)
         if t1 not in var.donors and t2 not in var.acceptors])

    return partial_exon_skipping, partial_intron_retention, exon_skipping, novel_exons, intron_retention


def summarize_missplicing_event(pes, pir, es, ne, ir):
    event = []
    if pes:
        event.append('PES')
    if es:
        event.append('ES')
    if pir:
        event.append('PIR')
    if ir:
        event.append('IR')
    if ne:
        event.append('NE')
    if len(event) >= 1:
        return ','.join(event)
    else:
        return '-'

def missense_effect(r, v):
    nt_changes, aa_changes = '', ''
    if len(r.protein) != len(v.protein) or len(r.orf) != len(v.orf):
        return '', '', -1

    if r.protein != v.protein:
        for i, (x, y) in enumerate(zip(r.protein, v.protein)):
            if x != y:
                aa_changes += f'{x}{i}{y},'

    if r.orf.seq != v.orf.seq:
        for i in range(len(r.protein)):
            p = i*3
            if r.orf.seq[p:p+3] != v.orf.seq[p:p+3]:
                nt_changes += f'{r.orf.seq[p:p+3]}{p}{v.orf.seq[p:p+3]},'
    return aa_changes, nt_changes

# Annotating
def OncospliceAnnotator(reference_transcript, variant_transcript, mut, ref_attributes=[], var_attributes=[]):
    affected_exon, affected_intron, distance_from_5, distance_from_3 = find_splice_site_proximity(np.floor(mut.indices[0]),
                                                                                                  reference_transcript)

    report = {}
    report['primary_transcript'] = reference_transcript.primary_transcript
    report['transcript_id'] = reference_transcript.transcript_id
    report['reference_protein'] = reference_transcript.protein
    report['variant_protein'] = variant_transcript.protein
    report['variant_protein_length'] = len(variant_transcript.protein)
    descriptions = define_missplicing_events(reference_transcript, variant_transcript)
    report['exon_changes'] = '|'.join([v for v in descriptions if v])
    report['splicing_codes'] = summarize_missplicing_event(*descriptions)
    report['affected_exon'] = affected_exon
    report['affected_intron'] = affected_intron
    report['mutation_distance_from_5'] = distance_from_5
    report['mutation_distance_from_3'] = distance_from_3
    aa_c, c_c, pos = missense_effect(reference_transcript, variant_transcript)
    report['missense_effect'] = aa_c
    report['codon_change'] = c_c
    report['missense_position'] = pos
    return report


def oncosplice(mut_id, splicing_threshold=0.5, protein_coding=True, primary_transcript=False,
               window_length=13, organism='hg38', splicing_engine=None, splicing_db=None, verbose=False,
               tis_engine=None, target_transcripts=None):

    gene = Gene.from_file(mut_id.split(':')[0], organism=organism)
    reference_gene_proteins = {
        transcript.generate_pre_mrna().generate_mature_mrna().generate_protein().protein: transcript.transcript_id for
        transcript in gene if transcript.transcript_biotype == 'protein_coding'}

    mutations = [MutSeqMat.from_mutid(m) for m in mut_id.split('|')]
    if gene.rev:
        mutations = [m.reverse_complement() for m in mutations[::-1]]

    results = []
    for reference_transcript in tqdm(gene, desc=f'Processing {mut_id}...'):
        if target_transcripts is not None and reference_transcript.transcript_id not in target_transcripts:
            continue

        # if (cons_required and not reference_transcript.cons_available) or (
        #         protein_coding and not reference_transcript.transcript_biotype == 'protein_coding'):
        if protein_coding and not reference_transcript.transcript_biotype == 'protein_coding':
            print("Not protein coding...")
            continue

        current_mutations = [m for m in mutations if m in reference_transcript]
        if len(current_mutations) == 0:
            print(f"No mutations within transcript ({reference_transcript.transcript_start} > {reference_transcript.transcript_end})...")
            continue

        center = np.mean([m.indices[0] for m in current_mutations]) // 1

        mutated_transcript = reference_transcript.clone()

        for mutation in current_mutations:
            mutated_transcript.mutate(mutation, inplace=True)

        reference_transcript.generate_mature_mrna().generate_protein()

        if len(reference_transcript.protein) < window_length:
            print(f"> Window length issue {reference_transcript.transcript_id}")
            continue

        reference_transcript.cons_vector = transform_conservation_vector(reference_transcript.cons_vector,
                                                                         window=window_length)

        assert len(reference_transcript.protein) == len(
            reference_transcript.cons_vector), f"Protein ({len(reference_transcript.protein)}) and conservation vector ({len(reference_transcript.cons_vector)}) must be same length."

        if splicing_engine is None:
            missplicing = Missplicing()
        else:
            missplicing, no_splicing_record = None, True
            if splicing_db is not None:
                missplicing = Missplicing(splicing_db.get_mutation_data(engine=splicing_engine, mut_id=mut_id, gene=gene.gene_name, transcript_id=reference_transcript.transcript_id))
                no_splicing_record = missplicing is None

            if missplicing is None:
                missplicing = find_transcript_missplicing_seqs(
                    reference_transcript.pre_mrna.get_context(center, context=7500, padding='N'),
                    mutated_transcript.pre_mrna.get_context(center, context=7500, padding='N'), reference_transcript.donors,
                    reference_transcript.acceptors, threshold=splicing_threshold, engine=splicing_engine)
                if no_splicing_record and splicing_db is not None:
                    splicing_db.store_mutation_data(engine=splicing_engine, mut_id=mut_id, gene=gene.gene_name, transcript_id=reference_transcript.transcript_id, data=missplicing.missplicing)

        alternative_splicing_paths = develop_aberrant_splicing(reference_transcript, missplicing) #.missplicing)
        for i, new_boundaries in enumerate(alternative_splicing_paths):
            print("iterating through new boundaries...")

            mutated_transcript.acceptors = new_boundaries['acceptors']
            mutated_transcript.donors = new_boundaries['donors']
            mutated_transcript.generate_mature_mrna().generate_protein()

            ### Experimental
            # mutated_transcript.generate_mature_mrna()
            # if tis_engine is None:
            #     tis_candidates = [(mutated_transcript.tis, 1)]
            # else:
            #     from tis_utils import tis_predictor
            #     tis_candidates = tis_predictor(mutated_transcript.mature_mrna)
            #
            # for tis_candidate, tis_score in tis_candidates:
            #     mutated_transcript.generate_protein(tis_candidate)
            ######

            alignment = get_logical_alignment(reference_transcript.protein, mutated_transcript.protein)
            deleted, inserted = find_indels_with_mismatches_as_deletions(alignment.seqA, alignment.seqB)
            modified_positions = find_modified_positions(len(reference_transcript.protein), deleted, inserted)
            temp_cons = np.convolve(reference_transcript.cons_vector * modified_positions,
                                    np.ones(window_length)) / window_length
            affected_cons_scores = max(temp_cons)
            percentile = (
                    sorted(reference_transcript.cons_vector).index(
                        next(x for x in sorted(reference_transcript.cons_vector) if x >= affected_cons_scores)) / len(
                reference_transcript.cons_vector))

            report = OncospliceAnnotator(reference_transcript, mutated_transcript, current_mutations[0])
            report['mut_id'] = mut_id
            report['splicing_engine'] = splicing_engine if splicing_engine is not None else 'None'
            # report['tis_engine'] = tis_engine if tis_engine is not None else 'None'
            # report['tis_pos'] = tis_candidate
            # report['tis_score'] = tis_score
            report['oncosplice_score'] = affected_cons_scores
            report['percentile'] = percentile
            report['isoform_id'] = short_hash_of_list(mutated_transcript.exons)
            report['isoform_prevalence'] = new_boundaries['path_weight']
            report['full_missplicing'] = missplicing.aberrant_splicing
            report['missplicing'] = missplicing.max_delta
            report['reference_resemblance'] = reference_gene_proteins.get(mutated_transcript.protein, None)
            results.append(report)

    if len(results) == 0:
        # print("Nothing...")
        return pd.DataFrame()

    return pd.DataFrame(results)[
        ['mut_id', 'transcript_id', 'isoform_id', 'primary_transcript', 'missplicing', 'full_missplicing',
         'exon_changes', 'splicing_codes', 'affected_exon', 'affected_intron', 'mutation_distance_from_5',
         'mutation_distance_from_3', 'missense_effect', 'codon_change', 'missense_position', 'reference_resemblance',
         'oncosplice_score', 'percentile', 'isoform_prevalence', 'reference_protein', 'variant_protein', 'splicing_engine']]


def process_splicing_path(new_boundaries, reference_transcript, mutated_transcript,
                          current_mutations, missplicing, mut_id, transcript_id,
                          splicing_engine, window_length, start_time):
    """
    Processes a single alternative splicing path and returns an annotation report.
    """
    # Update acceptors and donors
    mutated_transcript.acceptors = new_boundaries['acceptors']
    mutated_transcript.donors = new_boundaries['donors']
    mutated_transcript.generate_mature_mrna().generate_protein()

    # Align reference and mutated proteins
    alignment = get_logical_alignment(reference_transcript.protein, mutated_transcript.protein)
    deleted, inserted = find_indels_with_mismatches_as_deletions(alignment.seqA, alignment.seqB)
    modified_positions = find_modified_positions(len(reference_transcript.protein), deleted, inserted)

    # Compute conservation impact
    temp_cons = np.convolve(reference_transcript.cons_vector * modified_positions,
                            np.ones(window_length)) / window_length
    affected_cons_scores = max(temp_cons)

    # Compute percentile of conservation change
    sorted_cons = sorted(reference_transcript.cons_vector)
    percentile = (
            sorted_cons.index(next(x for x in sorted_cons if x >= affected_cons_scores)) / len(sorted_cons)
    )

    # Generate annotation report
    report = OncospliceAnnotator(reference_transcript, mutated_transcript, current_mutations[0])
    report.update({
        'mut_id': mut_id,
        'transcript_id': transcript_id,
        'splicing_engine': splicing_engine if splicing_engine is not None else 'None',
        'oncosplice_score': affected_cons_scores,
        'percentile': percentile,
        'isoform_id': short_hash_of_list(mutated_transcript.exons),
        'isoform_prevalence': new_boundaries['path_weight'],
        'full_missplicing': missplicing.aberrant_splicing,
        'missplicing': missplicing.max_delta,
        'execution_time': start_time,
        'status': 'Success'
    })
    return report


def oncosplice_df(row, splicing_threshold=0.5, window_length=13,
                  organism='hg38', splicing_engine='spliceai'):
    """
    Process a given mutation-transcript pair to analyze alternative splicing events
    and their oncogenic potential.

    Ensures that every `mut_id` and `transcript_id` is included in the output,
    even if processing fails, with an appropriate failure status.

    Parameters:
    - row (pd.Series): A row from a DataFrame containing `mut_id` and `transcript_id`
    - splicing_threshold (float): The threshold for splicing disruption detection
    - window_length (int): The window size for conservation analysis
    - organism (str): Genome assembly version
    - splicing_engine (str or None): The splicing prediction engine to use

    Returns:
    - pd.DataFrame: Processed results of the oncosplice analysis
    - Run "pd.concat(applied_function_output.to_list(), ignore_index=True)" to build result dataframe
    """

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Log function start time
    mut_id, transcript_id = row.mut_id, row.transcript_id

    # Default response template (to ensure all IDs are included)
    base_result = {
        'mut_id': mut_id,
        'transcript_id': transcript_id,
        'status': 'Success',  # Will be updated if an issue occurs
        'execution_time': start_time
    }

    # Load gene and transcript
    gene = Gene.from_file(mut_id.split(':')[0], organism=organism)
    if gene is None:
        base_result['status'] = 'Gene not found'
        return pd.DataFrame([base_result])

    mutations = [MutSeqMat.from_mutid(m) for m in mut_id.split('|')]
    reference_transcript = gene.transcript(transcript_id)

    if reference_transcript is None:
        base_result['status'] = 'Transcript not found'
        return pd.DataFrame([base_result])

    # Generate the reference transcript
    reference_transcript = (
        reference_transcript.generate_pre_mrna()
        .generate_mature_mrna()
        .generate_protein()
    )

    # Skip non-protein-coding transcripts
    if reference_transcript.transcript_biotype != 'protein_coding':
        base_result['status'] = 'Non-protein-coding transcript'
        return pd.DataFrame([base_result])

    # Filter mutations relevant to this transcript
    current_mutations = [m for m in mutations if m in reference_transcript]
    if not current_mutations:
        base_result['status'] = 'No relevant mutations'
        return pd.DataFrame([base_result])

    # Define mutation center
    center = np.mean([m.indices[0] for m in current_mutations]) // 1

    # Clone and apply mutations
    mutated_transcript = reference_transcript.clone()
    for mutation in current_mutations:
        mutated_transcript.mutate(mutation, inplace=True)

    # Adjust window length if necessary
    window_length = min(window_length, len(reference_transcript.protein))

    # Transform conservation vector
    reference_transcript.cons_vector = transform_conservation_vector(
        reference_transcript.cons_vector, window=window_length
    )

    # Identify missplicing events
    if splicing_engine is None:
        missplicing = Missplicing()
    else:
        missplicing = find_transcript_missplicing_seqs(
            reference_transcript.pre_mrna.get_context(center, context=7500, padding='N'),
            mutated_transcript.pre_mrna.get_context(center, context=7500, padding='N'),
            reference_transcript.donors, reference_transcript.acceptors,
            threshold=splicing_threshold, engine=splicing_engine
        )

    # Generate alternative splicing paths
    alternative_splicing_paths = develop_aberrant_splicing(reference_transcript, missplicing)
    results = [
        process_splicing_path(new_boundaries, reference_transcript, mutated_transcript,
                              current_mutations, missplicing, mut_id, transcript_id,
                              splicing_engine, window_length, start_time)
        for new_boundaries in alternative_splicing_paths
    ]

    # Return results as DataFrame
    if not results:
        base_result['status'] = 'No alternative splicing detected'
        return pd.DataFrame([base_result])

    return pd.DataFrame(results)[
        ['mut_id', 'transcript_id', 'isoform_id', 'primary_transcript', 'missplicing', 'full_missplicing',
         'exon_changes', 'splicing_codes', 'affected_exon', 'affected_intron', 'mutation_distance_from_5',
         'mutation_distance_from_3', 'missense_effect', 'codon_change', 'oncosplice_score', 'percentile',
         'isoform_prevalence', 'reference_protein', 'variant_protein', 'splicing_engine', 'execution_time', 'status']
    ]


#
# import asyncio
# async def oncosplice_prototype(mut_id, splicing_threshold=0.5, protein_coding=True, primary_transcript=False,
#                                window_length=13, organism='hg38', engine='spliceai', use_cons=True, require_cons=False):
#     import sys, os
#     needed_file1 = config[organism]['yoram_path'] / 'rest_api_utils.py'
#     needed_file2 = config[organism]['yoram_path'] / 'uniprot_utils.py'
#
#     if sys.platform == 'linux' and (needed_file1.is_file() and os.access(needed_file1, os.R_OK)) and (
#             needed_file2.is_file() and os.access(needed_file2, os.R_OK)):
#         sys.path.append(str(config[organism]['yoram_path']))
#         import uniprot_utils as uput
#
#     else:
#         raise SystemError(
#             "Oncosplice Prototype can only be run on Power with access to the /tamir2/yoramzar/Projects/Cancer_mut/Utils folder.")
#
#     from .tis_utils import find_tis
#
#     # Define async functions
#     async def background_request(ensb_id, Uniprot_features=["Topological domain", "Transmembrane", "Domain"]):
#         return uput.retrieve_protein_data_features_subset(uput.ensembl_id2uniprot_id(ensb_id), Uniprot_features)
#
#     def inspect_domain(row, modified_vector, conservation_vector):
#         v1, v2 = modified_vector[row.start:row.end], conservation_vector[row.start:row.end]
#         if sum(v2) == 0:
#             return pd.Series([f'{row.type}|{row.start}|{row.end}|{row.description}', 0],
#                              index=['domain_identifier', 'score'])
#
#         return pd.Series([f'{row.type}|{row.start}|{row.end}|{row.description}', sum(v1 * v2) / sum(v2)],
#                          index=['domain_identifier', 'score'])
#
#     gene = Gene(mut_id.split(':')[0], organism=organism)
#     reference_gene_proteins = {tid: transcript.generate_pre_mrna().generate_mature_mrna().generate_protein() for tid, transcript in gene.run_transcripts(protein_coding=True)}
#     mutations = [get_mutation(mut_id, rev=gene.rev) for mut_id in mut_id.split('|')]
#     results = []
#     for tid, transcript in gene.run_transcripts(protein_coding=protein_coding, primary_transcript=primary_transcript):
#         if require_cons and not transcript.cons_available:
#             continue
#
#         if all(mutation not in transcript for mutation in mutations):
#             # results.append({'transcript_id': transcript.transcript_id})
#             continue
#
#         task1 = asyncio.create_task(background_request(tid))
#         transcript.generate_pre_mrna()
#         transcript.cons_vector = transform_conservation_vector(transcript.cons_vector, window=window_length)
#         transcript.generate_mature_mrna().generate_protein(inplace=True)
#         ref_protein, cons_vector = transcript.protein, transcript.cons_vector
#
#         if not use_cons:
#             cons_vector = np.ones(len(ref_protein))
#
#         if sum(cons_vector) == 0:
#             cons_vector = np.ones(len(ref_protein)) #/len(ref_protein)
#
#         reference_transcript = copy.deepcopy(transcript)
#
#         assert len(ref_protein) == len(
#             cons_vector), f"Protein ({len(ref_protein)}) and conservation vector ({len(cons_vector)} must be same length."
#
#         missplicing = Missplicing(find_transcript_missplicing(transcript, mutations, engine=engine, threshold=splicing_threshold),
#                                   threshold=splicing_threshold)
#         for mutation in mutations:
#             transcript.pre_mrna += mutation
#
#         domains_df = await task1
#         for i, new_boundaries in enumerate(develop_aberrant_splicing(transcript, missplicing.aberrant_splicing)):
#             transcript.acceptors = new_boundaries['acceptors']
#             transcript.donors = new_boundaries['donors']
#             transcript.generate_mature_mrna()
#             transcript.TIS = find_tis(ref_seq=reference_transcript, mut_seq=transcript)
#             transcript.generate_protein()
#
#             alignment = get_logical_alignment(reference_transcript.protein, transcript.protein)
#             deleted, inserted = find_indels_with_mismatches_as_deletions(alignment.seqA, alignment.seqB)
#             modified_positions = find_modified_positions(len(ref_protein), deleted, inserted)
#             temp_cons = np.convolve(cons_vector * modified_positions, np.ones(window_length)) / window_length
#             affected_cons_scores = max(temp_cons)
#             percentile = (
#                     sorted(cons_vector).index(next(x for x in sorted(cons_vector) if x >= affected_cons_scores)) / len(
#                 cons_vector))
#
#             out = domains_df.apply(lambda row: inspect_domain(row, modified_positions, cons_vector), axis=1)
#             domains_affected = '+'.join([f'{a}:{round(b, 3)}' for a, b in list(zip(out.domain_identifier, out.score))])
#
#             report = OncospliceAnnotator(reference_transcript, transcript, mutation)
#             report['mut_id'] = mut_id
#             report['oncosplice_score'] = affected_cons_scores
#             report['cons_available'] = transcript.cons_available
#             report['transcript_id'] = transcript.transcript_id
#             report['percentile'] = percentile
#             report['isoform_id'] = i
#             report['isoform_prevalence'] = new_boundaries['path_weight']
#             report['full_missplicing'] = missplicing.aberrant_splicing
#             report['missplicing'] = max(missplicing)
#             report['domains'] = domains_affected
#             report['max_domain_score'] = out.score.max()
#
#             report['reference_resemblance'] = reference_gene_proteins.get(transcript.protein, None)
#             results.append(pd.Series(report))
#
#     report = pd.concat(results, axis=1).T
#     return report


if __name__ == '__main__':
    pass