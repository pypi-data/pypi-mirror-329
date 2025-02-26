import re
import numpy as np

ALPHABET = {'N': 'N', 'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', '-': '-'}

class SeqMat:
    ROW_SEQ = 0
    ROW_INDS = 1
    ROW_SUPERINDS = 2
    ROW_MUTATED = 3
    ROW_ANNOTATION = 4

    def __init__(self, seqmat, alphabet=None):
        self.seqmat = seqmat
        self.alphabet = alphabet or {'N': 'N', 'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', '-': '-'}

        self.char_to_value = {c: i for i, c in enumerate(self.alphabet.keys())}
        self.value_to_char = {i: c for i, c in enumerate(self.alphabet.keys())}
        self.value_complements = {self.char_to_value[c1]: self.char_to_value[c2] for c1, c2 in self.alphabet.items()}

    def __repr__(self):
        return f"<SeqMat: {self.seq}>"

    def __str__(self):
        return self.seq

    def __len__(self):
        return self.seqmat.shape[1]

    def __getitem__(self, key):
        if isinstance(key, slice):
            pos1, pos2 = self._rel_index(key.start), self._rel_index(key.stop)
            return SeqMat(self.seqmat[:, pos1:pos2+1])
        else:
            pos = self._rel_index(key)
            return SeqMat(self.seqmat[:, pos:pos + 1])

    def __contains__(self, other):
        """
        Checks if another SeqMat object is entirely contained within this SeqMat object.

        Args:
            other (SeqMat): Another SeqMat object to check for containment.

        Returns:
            bool: True if `other` is contained in `self`, False otherwise.
        """
        # Ensure `other` is a SeqMat
        if not isinstance(other, SeqMat):
            raise TypeError("Can only check containment with another SeqMat object.")

        # Check if all indices of `other` are in `self`
        other_indices = other.seqmat[other.ROW_INDS, :]
        self_indices = self.seqmat[self.ROW_INDS, :]
        if not np.all(np.isin(other_indices, self_indices)):
            return False

        return True

    def __eq__(self, other):
        """
        Implements the == operator to compare two SeqMat objects.

        Args:
            other (SeqMat): The other SeqMat object to compare.

        Returns:
            bool: True if the two SeqMat objects are equal, False otherwise.
        """
        # Ensure `other` is a SeqMat object
        if not isinstance(other, SeqMat):
            return False

        # Compare the sequence matrix
        if not np.array_equal(self.seqmat, other.seqmat):
            return False

        return True

    @classmethod
    def empty(cls, alphabet=None):
        """
        Creates an empty SeqMat object.

        Args:
            alphabet (dict): Optional alphabet dictionary (default: {'N': 'N', 'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}).

        Returns:
            SeqMat: An empty SeqMat object.
        """
        empty_seqmat = np.zeros((4, 0), dtype=np.int32)  # 4 rows, 0 columns (no data)
        return cls(empty_seqmat, alphabet=alphabet)

    def __add__(self, other):
        """
        Implements the + operator. Joins two SeqMat objects or applies mutations.

        If `other` is outside the range of indices, the sequences are concatenated, provided the indices are
        monotonically increasing or decreasing. Otherwise, it applies the mutation.

        Args:
            other (SeqMat): Another SeqMat object to join or mutate.

        Returns:
            SeqMat: A new SeqMat object with the resulting sequence.
        """
        # Ensure `other` is a SeqMat
        if not isinstance(other, SeqMat):
            raise TypeError("Can only add another SeqMat object.")

        if other in self:
            return self.mutate(other)

        else:
            combined_seqmat = np.hstack((self.seqmat, other.seqmat))

        # Ensure the combined sequence is monotonic
        if not self._is_monotonic(combined_seqmat[self.ROW_INDS]):
            raise ValueError("Resulting sequence indices are not monotonic.")

        return SeqMat(combined_seqmat, alphabet=self.alphabet)

    def __iadd__(self, other):
        """
        Implements the += operator. Joins two SeqMat objects or applies mutations in place.

        Args:
            other (SeqMat): Another SeqMat object to join or mutate.

        Returns:
            SeqMat: The mutated or joined SeqMat object.
        """
        # Ensure `other` is a SeqMat
        if not isinstance(other, SeqMat):
            raise TypeError("Can only add another SeqMat object.")

        if other in self:
            self.seqmat = self.mutate(other).seqmat
            return self
        else:
            self.seqmat = np.hstack((self.seqmat, other.seqmat))

        if not self._is_monotonic(self.seqmat[self.ROW_INDS]):
            raise ValueError("Resulting sequence indices are not monotonic.")

        return self

    # def get_context(self, pos, context=500):
    #     pos = self._rel_index(pos)
    #     lower_bound, upper_bound = max(0, pos - context), min(len(self), pos + context + 1)
    #     return SeqMat(self.seqmat[:, lower_bound:upper_bound])

    def get_context(self, pos, context=500, padding=None):
        """
        Returns a SeqMat object representing the region around `pos` with the given context.
        If padding is provided and the requested context extends beyond the sequence boundaries,
        the result is padded with the specified nucleotide in the sequence row and -1 in the indices rows.

        Args:
            pos (int): The position of interest in the original coordinate space.
            context (int): The number of nucleotides to include on each side of pos (default 500).
            padding (str or None): The nucleotide to use for padding. If None, no padding is applied and
                                   the returned region may be shorter than requested.

        Returns:
            SeqMat: A new SeqMat object containing the context region (padded if requested).
        """
        # Resolve the relative index
        pos = self._rel_index(pos)

        # Calculate desired start and end positions
        desired_length = 2 * context + 1
        start = pos - context
        end = pos + context + 1

        # Actual bounds clipped to the available length
        actual_start = max(start, 0)
        actual_end = min(len(self), end)

        # Extract the slice that fits within the sequence
        slice_seqmat = self.seqmat[:, actual_start:actual_end]

        extracted_length = slice_seqmat.shape[1]

        # If no padding requested, just return the slice
        if padding is None or extracted_length == desired_length:
            return SeqMat(slice_seqmat)

        # If padding is requested and we have fewer columns than desired, pad the result
        if extracted_length < desired_length:
            # Determine how much we need to pad on each side
            pad_left = max(-start, 0)  # How many columns needed before actual_start
            pad_right = max(end - len(self), 0)  # How many columns needed after actual_end

            # Determine numeric code for padding nucleotide
            # Assuming self.char_to_value is available and 'N' is known if padding isn't recognized
            N_val = self.char_to_value.get(padding, self.char_to_value['N'])

            # Create a new array with the desired length
            new_seqmat = np.full((self.seqmat.shape[0], desired_length), -1, dtype=self.seqmat.dtype)
            # Fill the sequence row with N_val
            new_seqmat[0, :] = N_val

            # Place the extracted slice into the correct position
            new_seqmat[:, pad_left:pad_left + extracted_length] = slice_seqmat
            return SeqMat(new_seqmat)

        # If for some reason extracted_length > desired_length (unlikely), just truncate
        if extracted_length > desired_length:
            return SeqMat(slice_seqmat[:, :desired_length])

        # Fallback (should not reach here normally)
        return SeqMat(slice_seqmat)


    def _rel_index(self, pos):
        if pos in self.raw_indices:
            return np.where(self.seqmat[self.ROW_INDS, :] == pos)[0][0]
        else:
            raise IndexError(f"Position {pos} not found in sequence.")

    def _is_same_strand(self, other):
        """
        Checks if two SeqMat objects are on the same strand.

        Args:
            other (SeqMat): The other SeqMat object to compare.

        Returns:
            bool: True if both are on the same strand, False otherwise.
        """
        self_indices = self.seqmat[self.ROW_INDS, :]
        other_indices = other.seqmat[self.ROW_INDS, :]

        # Determine monotonicity
        self_increasing = np.all(np.diff(self_indices) >= 0)
        self_decreasing = np.all(np.diff(self_indices) <= 0)
        other_increasing = np.all(np.diff(other_indices) >= 0)
        other_decreasing = np.all(np.diff(other_indices) <= 0)

        # Both must be either increasing or decreasing
        return (self_increasing and other_increasing) or (self_decreasing and other_decreasing)

    def reverse_complement(self, inplace=True):
        """
        Reverse complement the sequence in place.
        """
        seqmat = self.seqmat[:, ::-1].copy()
        seqmat[self.ROW_SEQ, :] = np.vectorize(self.value_complements.get)(seqmat[self.ROW_SEQ])

        if inplace:
            self.seqmat = seqmat
            return self

        return SeqMat(seqmat)

    @classmethod
    def from_seq(cls, seq_dict, alphabet=None):
        """
        Create a SeqMat object from a dictionary containing sequence information.
        """
        seq = np.array(list(seq_dict["seq"]))
        inds = seq_dict.get("indices", np.arange(len(seq), dtype=np.int32))
        superinds = seq_dict.get("superinds", np.zeros(len(seq), dtype=np.int32))
        mutmark = np.zeros_like(superinds)

        assert len(seq) == len(inds), f"Sequence length {len(seq)} must match indices length {len(inds)}"
        if not cls._is_monotonic(inds):
            raise ValueError(f"Sequence indices must be monotonic, got {inds}")

        # Create character-to-value mapping
        char_to_value = {c: i for i, c in enumerate(ALPHABET.keys())}
        seq_values = [char_to_value[nt] for nt in seq]

        # Stack sequence matrix
        seqmat = np.vstack([seq_values, inds, superinds, mutmark]).astype(np.int32)
        return cls(seqmat)

    @staticmethod
    def _is_monotonic(inds):
        if len(inds) <= 1:
            return True

        return all(x >= y for x, y in zip(inds, inds[1:])) if inds[0] > inds[-1] else all(
            x <= y for x, y in zip(inds, inds[1:]))

    @property
    def seq(self):
        return self.rawseq.replace('-', '')

    @property
    def rawseq(self):
        return ''.join([self.value_to_char[int(ind)] for ind in self.seqmat[self.ROW_SEQ, :]])

    @property
    def indices(self):
        return self.seqmat[self.ROW_INDS, self.seqmat[self.ROW_SEQ, :] != 5] + (
                    self.seqmat[self.ROW_SUPERINDS, self.seqmat[self.ROW_SEQ, :] != 5] / 10)

    @property
    def raw_indices(self):
        return self.seqmat[self.ROW_INDS, :] + (self.seqmat[self.ROW_SUPERINDS, :] / 10)

    @property
    def filter(self):
        return self.seqmat[:, self.seqmat[self.ROW_SEQ, :] != 5]


    def mutate(self, mut, inplace=False):
        """
        Apply mutations to the sequence matrix.
        Args:
            mut (SeqMat): A SeqMat object containing mutations.
            return_seqmat (bool): If True, return the mutated seqmat; otherwise, return updated sequence.

        Returns:
            str or np.ndarray: Mutated sequence or sequence matrix based on `return_seqmat`.
        """
        ### NEEDS some work to make sure that mutations can continue being added without issue...

        # Ensure strand compatibility
        # if not self._is_same_strand(mut):
        #     raise ValueError("Mutation and sequence are not on the same strand.")

        # something to make sure the mutation is contained as one deletion, insertion, or snp or indel
        ref_seqmat = self.seqmat.copy()
        mut_seqmat = mut.seqmat

        # Ensure mutation indices exist in the reference
        if not np.all(np.isin(mut_seqmat[self.ROW_INDS, :], ref_seqmat[self.ROW_INDS, :])):
            return self

        # Handle the fact that only part of the mutation is in the sequence and isertable
        if not np.all(np.isin(mut_seqmat[self.ROW_INDS, :], ref_seqmat[self.ROW_INDS, :])):
            raise ValueError("Some mutation indices are not found in the reference sequence.")

        # Handle replacements
        temp = mut_seqmat[:, np.where(mut_seqmat[self.ROW_SUPERINDS, :] == 0)[0]]
        condition = (
            np.isin(ref_seqmat[self.ROW_INDS, :],
                    temp[self.ROW_INDS, :])
        )

        indices = np.where(condition)[0]
        ref_seqmat[:, indices] = temp[:, :]

        # Handle insertions
        insertions = np.where(mut_seqmat[self.ROW_SUPERINDS, :] > 0)[0]
        if insertions.size > 0:
            ins_seqmat = mut_seqmat[:, insertions]
            correction = 1 if self.seqmat[self.ROW_INDS, 0] > self.seqmat[self.ROW_INDS, -1] else 0
            ins_loc = np.where(ref_seqmat[self.ROW_INDS, :] == ins_seqmat[self.ROW_INDS, 0])[0][0] + 1 - correction
            ref_seqmat = np.insert(ref_seqmat, ins_loc, ins_seqmat.T, axis=1)

        if inplace:
            self.seqmat = ref_seqmat
            return self

        return SeqMat(ref_seqmat)

    def orf_seqmat(self, tis_index):
        stop_index = None
        if tis_index not in self.indices:
            return SeqMat.from_seq({'seq': ''})

        raw_seq = SeqMat(self.seqmat[:, self._rel_index(tis_index):])
        raw_seq = SeqMat(raw_seq.filter)

        # temp = temp[:, temp[0, :] != 5]
        # temp = SeqMat(temp)  # .drop_indices()
        # raw_seq = temp.seq  # Extract the raw sequence
        pattern = re.compile(r"TAA|TAG|TGA")
        matches = pattern.finditer(raw_seq.seq)  # Use finditer to get all matches
        for m in matches:
            if m.start() % 3 == 0:
                stop_index = m.start()
                break

        if stop_index is None:
            stop_index = len(raw_seq) - (len(raw_seq) % 3)

        return SeqMat(raw_seq.seqmat[:, :stop_index])

    def translate(self, tis_index):
        """
        Translates a nucleotide sequence into an amino acid sequence.
        Ensures the sequence length is divisible by 3 by trimming excess nucleotides.

        Args:
            sequence (str): Nucleotide sequence (e.g., ACGT).

        Returns:
            str: Translated amino acid sequence.
        """
        # Codon-to-amino acid mapping table (standard genetic code)
        codon_table = {
            'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
            'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
            'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
            'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
            'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
            'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
            'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
            'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
            'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
            'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
            'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
            'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
            'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
            'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
            'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
        }
        sequence = self.orf_seqmat(tis_index).seq

        # Ensure sequence is uppercase
        sequence = sequence.upper()

        # Trim sequence to ensure divisibility by 3
        trimmed_length = len(sequence) - (len(sequence) % 3)
        sequence = sequence[:trimmed_length]

        # Translate sequence in chunks of 3
        amino_acids = [codon_table.get(sequence[i:i+3], 'X') for i in range(0, len(sequence), 3)]

        # Join amino acids into a single string
        return ''.join(amino_acids)


    def to_dict(self):
        return {'seq': self.rawseq, 'indices': self.indices, 'superinds': self.seqmat[self.ROW_SUPERINDS, :]}

class DnaSeqMat(SeqMat):
    pass


class RnaSeqMat(SeqMat):
    pass


class AASeqMat(SeqMat):
    pass


class MutSeqMat(SeqMat):
    """
    A subclass of SeqMat designed specifically for mutation sequences.

    Additional Conditions:
    1. Mutation indices must be consecutive (increasing or decreasing).
    2. The superinds row must have a maximum value of 10.
    """

    def __init__(self, seqmat, alphabet=None):
        super().__init__(seqmat, alphabet)

        # Validate the mutation-specific conditions
        self._validate_mutation_indices()
        self.seqmat[-1, :] = 1
        self.position = min(self.seqmat[self.ROW_INDS, :])

        # self._validate_superinds()

    def _validate_mutation_indices(self):
        """
        Validates that the mutation indices are consecutive (increasing or decreasing).
        """
        indices = self.seqmat[self.ROW_INDS, :]
        if not (np.all(abs(np.diff(indices)) <= 1)):
            raise ValueError(f"Mutation indices must be consecutive. Got: {indices}")

    @property
    def indices(self):
        return self.seqmat[self.ROW_INDS, :] + (self.seqmat[self.ROW_SUPERINDS, :] / 10)

    @classmethod
    def from_mutid(cls, mid):
        gene, chrom, i, r, a = mid.split(':')
        if list(set(a))[0] == '-' and len(a) > 1 and len(list(set(a))) == 1:
            a = '-'

        if list(set(r))[0] == '-' and len(r) > 1 and len(list(set(r))) == 1:
            r = '-'

        i = int(i)

        if len(a) == len(r) == 1 and a != '-' and r != '-':
            temp = {'seq': a, 'indices': [i], 'superinds': [0]}

        elif a == '-' and r != '-':
            # return Allele('-' *len(r), np.arange(i, i+ len(r), dtype=np.int32), [0] * len(r), rev)
            temp = {'seq': '-'*len(r), 'indices': np.arange(i, i + len(r), dtype=np.int32), 'superinds':  [0] * len(r)}

        elif r == '-' and a != '-':
            # print(a, np.full(len(a), int(i)), np.arange(1, len(a)+1),)
            # return Allele(a, np.full(len(a), int(i)), np.arange(1, len(a)+1), rev)
            temp = {'seq': a, 'indices': np.full(len(a), int(i)), 'superinds':  np.arange(1, len(a)+1)}

        elif a != '-' and r != '-':
            ind1 = np.concatenate(
                [np.arange(i, i + len(r), dtype=np.int32), np.full(len(a), len(r) + i - 1, dtype=np.int32)])
            ind2 = np.concatenate([np.zeros(len(r), dtype=np.int32), np.arange(1, len(a) + 1, dtype=np.int32)])
            # return Allele('-' * len(r) + a, ind1, ind2, rev)
            temp = {'seq': '-' * len(r) + a, 'indices': ind1, 'superinds':  ind2}

        return cls.from_seq(temp)


    # def _validate_superinds(self):
    #     """
    #     Validates that the superinds row has a maximum value of 10.
    #     """
    #     superinds = self.seqmat[self.ROW_SUPERINDS, :]
    #     if np.max(superinds) > 10:
    #         raise ValueError(f"Superinds row must have a maximum value of 10. Got: {superinds}")


