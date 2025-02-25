from __future__ import annotations
from typing import Any, Optional, Union
import numpy as np
import copy
from Bio.Seq import Seq  # Assuming Biopython is used
from . import unload_pickle, config
from .SeqMats import SeqMat, MutSeqMat
from .Fasta_segment import Fasta_segment

class Transcript:
    """
    Represents a transcript with associated genomic information such as exons, introns, and sequences.

    A Transcript object is expected to contain attributes loaded from a dictionary `d` representing
    annotations and metadata. This includes (at least):
    - transcript_start
    - transcript_end
    - rev (boolean indicating if the transcript is on the reverse strand)
    - chrm (chromosome)
    - donors
    - acceptors
    - cons_vector
    - cons_seq
    - transcript_seq
    - transcript_biotype
    - primary_transcript
    - transcript_id
    - TIS, TTS (if protein-coding)
    """

    def __init__(self, d: dict[str, Any], organism: str = 'hg38'):
        """
        Initialize a Transcript object from a dictionary of attributes and metadata.

        Args:
            d (dict): Dictionary containing transcript attributes and data.
            organism (str): Genome build or organism reference (e.g., 'hg38').

        Raises:
            AssertionError: If required attributes are missing.
        """
        # Convert certain attributes to NumPy arrays for consistent processing
        array_fields = {'acceptors', 'donors', 'cons_vector'}
        for k, v in d.items():
            if k in array_fields and v is not None:
                v = np.array(v)
            setattr(self, k, v)

        self.organism: str = organism

        # Required attributes to form a valid transcript object
        required_attrs = ['transcript_start', 'transcript_end', 'rev', 'chrm']
        missing = [attr for attr in required_attrs if not hasattr(self, attr)]
        if missing:
            raise AssertionError(f"Transcript is missing required attributes: {missing}")

        # Default fallback values for optional attributes
        if not hasattr(self, 'donors') or self.donors is None:
            self.donors = np.array([])
        if not hasattr(self, 'acceptors') or self.acceptors is None:
            self.acceptors = np.array([])
        if not hasattr(self, 'cons_available'):
            self.cons_available = False

        # Determine if transcript is protein-coding
        self.protein_coding: bool = hasattr(self, 'TIS') and hasattr(self, 'TTS')

        # Calculate transcript boundaries
        self.transcript_upper = max(self.transcript_start, self.transcript_end)
        self.transcript_lower = min(self.transcript_start, self.transcript_end)

        # Generate pre-mRNA sequence data
        self.generate_pre_mrna()

        # If consensus data is available and ends with '*', adjust cons_vector and cons_seq
        if self.cons_available and hasattr(self, 'cons_seq') and hasattr(self, 'cons_vector'):
            if self.cons_seq.endswith('*') and len(self.cons_seq) == len(self.cons_vector):
                self.cons_vector = self.cons_vector[:-1]
                self.cons_seq = self.cons_seq[:-1]

    def __repr__(self) -> str:
        """Official string representation."""
        return f"Transcript({getattr(self, 'transcript_id', 'unknown_id')})"

    def __str__(self) -> str:
        """
        Unofficial, user-friendly string representation of the transcript.

        Returns:
            str: A summary of the transcript including ID, type, and primary status.
        """
        transcript_biotype = getattr(self, 'transcript_biotype', 'unknown').replace('_', ' ').title()
        primary = getattr(self, 'primary_transcript', False)
        return f"Transcript {getattr(self, 'transcript_id', 'unknown_id')}, " \
               f"Type: {transcript_biotype}, Primary: {primary}"

    def __len__(self) -> int:
        """
        Length of the transcript sequence.

        Returns:
            int: Length of the transcript sequence.
        """
        return len(getattr(self, 'transcript_seq', ''))

    def __eq__(self, other: object) -> bool:
        """
        Check equality of two transcripts based on their transcript sequences.

        Args:
            other (object): Another transcript-like object.

        Returns:
            bool: True if sequences match, False otherwise.
        """
        if not isinstance(other, Transcript):
            return NotImplemented
        return self.transcript_seq == other.transcript_seq

    def __contains__(self, subvalue: Any) -> bool:
        """
        Check if a given subsequence (e.g., another SeqMat) is contained within the pre_mRNA.

        Args:
            subvalue (Any): The substring (or sub-SeqMat) to search for in the mature mRNA.

        Returns:
            bool: True if subvalue's indices are all present in the pre_mRNA, False otherwise.

        Notes:
            This assumes `subvalue` has a `seqmat` attribute and that `subvalue.seqmat[1, :]` represents indices.
        """
        if not hasattr(subvalue, 'seqmat'):
            return False
        return np.all(np.isin(subvalue.seqmat[1, :], self.pre_mrna.seqmat[1, :]))

    @property
    def exons(self) -> list[tuple[int, int]]:
        """
        Return a list of exon boundary tuples (acceptor, donor).

        Returns:
            list of (int, int): List of exon boundaries.
        """
        exon_starts = np.concatenate(([self.transcript_start], self.acceptors))
        exon_ends = np.concatenate((self.donors, [self.transcript_end]))
        return list(zip(exon_starts, exon_ends))

    @property
    def exons_pos(self) -> list[tuple[int, int]]:
        """
        Return exons with positions adjusted for strand orientation.

        Returns:
            list of (int, int): Exons adjusted for strand orientation.
        """
        exon_positions = self.exons
        if self.rev:
            # Reverse order and swap coordinates for reverse strand
            exon_positions = [(end, start) for start, end in exon_positions[::-1]]
        return exon_positions

    @property
    def introns(self) -> list[tuple[int, int]]:
        """
        Return a list of intron boundaries derived from donors and acceptors.

        Returns:
            list of (int, int): Intron boundaries.
        """
        valid_donors = self.donors[self.donors != self.transcript_end]
        valid_acceptors = self.acceptors[self.acceptors != self.transcript_start]
        return list(zip(valid_donors, valid_acceptors))

    @property
    def introns_pos(self) -> list[tuple[int, int]]:
        """
        Return introns with positions adjusted for strand orientation.

        Returns:
            list of (int, int): Introns adjusted for strand orientation.
        """
        intron_positions = self.introns
        if self.rev:
            intron_positions = [(end, start) for start, end in intron_positions[::-1]]
        return intron_positions

    def _fix_and_check_introns(self) -> Transcript:
        """
        Ensure acceptors and donors are sorted and unique, and validate exon/intron structures.

        Raises:
            ValueError: If there are mismatches or ordering issues in exons/introns.

        Returns:
            Transcript: The current Transcript object (for chaining).
        """
        # Ensure uniqueness and correct ordering based on strand
        self.acceptors = np.unique(self.acceptors)
        self.donors = np.unique(self.donors)

        if self.rev:
            self.acceptors = np.sort(self.acceptors)[::-1]
            self.donors = np.sort(self.donors)[::-1]
        else:
            self.acceptors = np.sort(self.acceptors)
            self.donors = np.sort(self.donors)

        # Validation checks
        if self.__exon_intron_matchup_flag():
            raise ValueError("Unequal number of acceptors and donors.")

        if self.__exon_intron_order_flag():
            raise ValueError("Exon/intron order out of position.")

        if self.__transcript_boundary_flag():
            raise ValueError("Transcript boundaries must straddle acceptors and donors.")

        return self

    def __exon_intron_matchup_flag(self) -> bool:
        """Check if acceptors and donors count match."""
        return len(self.acceptors) != len(self.donors)

    def __exon_intron_order_flag(self) -> bool:
        """Check for ordering issues in exon boundaries."""
        return any(start > end for start, end in self.exons_pos)

    def __transcript_boundary_flag(self) -> bool:
        """Check if boundaries are within the transcript start/end range."""
        if not len(self.acceptors) and not len(self.donors):
            return False
        min_boundary = np.min(np.concatenate((self.acceptors, self.donors)))
        max_boundary = np.max(np.concatenate((self.acceptors, self.donors)))
        return (self.transcript_lower > min_boundary) or (self.transcript_upper < max_boundary)

    @property
    def exonic_indices(self) -> np.ndarray:
        """
        Return the indices covering exons in the transcript.

        Returns:
            np.ndarray: Array of exon indices.
        """
        return np.concatenate([np.arange(a, b + 1) for a, b in self.exons_pos])

    def pull_pre_mrna_pos(self) -> dict[str, Any]:
        """
        Retrieve the pre-mRNA sequence and indices using a Fasta_segment object.

        Returns:
            dict: A dictionary with 'seq' and 'indices' keys.
        """
        fasta_obj = Fasta_segment()
        return fasta_obj.read_segment_endpoints(
            config[self.organism]['CHROM_SOURCE'] / f'chr{self.chrm}.fasta',
            self.transcript_lower - 1,
            self.transcript_upper + 1
        )

    def generate_pre_mrna(self) -> Transcript:
        """
        Generate the pre-mRNA sequence for the transcript and store it as `self.pre_mrna`.

        Returns:
            Transcript: The current Transcript object (for chaining).
        """
        pre_mrna = SeqMat.from_seq(self.pull_pre_mrna_pos())
        if self.rev:
            pre_mrna.reverse_complement()
        self.pre_mrna = pre_mrna
        return self

    def mutate(self, mutation: MutSeqMat, inplace: bool = False) -> Union[Transcript, SeqMat]:
        """
        Apply a mutation to the pre_mRNA sequence of this Transcript.

        If the transcript is on the reverse strand (self.rev is True),
        the mutation is first reverse-complemented to ensure strand compatibility.

        Args:
            mutation (SeqMat): The mutation to apply. Must be a SeqMat or a compatible object that supports .mutate().
            inplace (bool): If True, apply the mutation directly to this Transcript's pre_mRNA
                            and return 'self'. If False, return a new SeqMat with the mutated sequence.

        Returns:
            Transcript: If inplace=True, returns the updated Transcript object.
            SeqMat: If inplace=False, returns a new SeqMat object representing the mutated sequence.
        """
        # If transcript is reversed, reverse-complement the mutation first
        if self.rev:
            mutation.reverse_complement()

        # Attempt the mutation operation
        mutated_seqmat = self.pre_mrna.mutate(mutation).seqmat
        if inplace:
            # Update this Transcript's pre_mRNA and return the Transcript itself
            self.pre_mrna = SeqMat(mutated_seqmat)
            return self

        else:
            # Create a copy of the current Transcript and update its pre_mrna
            # Assuming you have a way to clone the Transcript; if not, manually recreate it.
            new_transcript = copy.deepcopy(self)
            new_transcript.pre_mrna = SeqMat(mutated_seqmat)
            return new_transcript

    def generate_mature_mrna(self, inplace: bool = True) -> Union[Transcript, SeqMat]:
        """
        Generate the mature mRNA by concatenating exon regions from pre_mRNA.

        Args:
            inplace (bool): If True, set `self.mature_mrna`, else return a new SeqMat.

        Returns:
            Transcript or SeqMat: The Transcript object (if inplace=True) or a SeqMat (if inplace=False).
        """
        self._fix_and_check_introns()

        mature_mrna = SeqMat.empty()
        pos_mrna = self.pre_mrna

        for exon_start, exon_end in self.exons:
            # Add each exon region to the mature_mrna
            mature_mrna += pos_mrna[exon_start:exon_end]

        if inplace:
            self.mature_mrna = mature_mrna
            return self
        return mature_mrna

    @property
    def orf(self, tis=None):
        """
        Return the ORF (Open Reading Frame) SeqMat object, if TIS and TTS are available.

        Returns:
            SeqMat or self: The ORF SeqMat if TIS/TTS are set, else self.
        """
        if not self.protein_coding:
            print("Cannot create protein without set TIS and TTS values.")
            return self

        if tis is None:
            tis = self.TIS
        return self.mature_mrna.orf_seqmat(tis)

    def clone(self) -> Transcript:
        """
        Returns a deep copy of this Transcript instance.

        Returns:
            Transcript: A new Transcript object that is a deep copy of the current instance.
        """
        return copy.deepcopy(self)

    def generate_protein(self, inplace: bool = True, domains: Optional[np.ndarray] = None) -> Union[
        Transcript, tuple[str, np.ndarray]]:
        """
        Translate the ORF into a protein sequence and optionally filter consensus vector by domains.

        Args:
            inplace (bool): If True, store protein and cons_vector in self. Otherwise, return them.
            domains (np.ndarray, optional): Array of domain indices.

        Returns:
            Transcript or (protein: str, cons_vector: np.ndarray): The Transcript object if inplace=True, else the protein and cons_vector.
        """
        if not self.protein_coding:
            print("No protein can be generated without TIS/TTS.")
            return self if inplace else ("", np.array([]))

        # Translate the ORF to protein
        protein = str(Seq(self.orf.seq).translate()).strip('*') # .replace('*', '')

        # Use existing cons_vector or default to an array of ones
        self.cons_vector = self.cons_vector if hasattr(self, 'cons_vector') and len(self.cons_vector) == len(protein) else np.ones(len(protein))
        self.protein = protein
        return self
