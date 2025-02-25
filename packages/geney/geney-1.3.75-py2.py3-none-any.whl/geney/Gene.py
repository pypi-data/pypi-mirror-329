import copy
import random
from typing import Any, Dict, List, Tuple, Optional, Iterator, Union, TYPE_CHECKING
from collections import Counter
from . import unload_pickle, config
from .Transcript import Transcript

class Gene:
    """
    A class representing a Gene, with associated transcripts and metadata.

    Attributes:
        organism (str): The organism build (e.g. 'hg38').
        transcripts (dict): A dictionary of transcript annotations keyed by transcript ID.
        gene_name (str): The name of the gene.
        gene_id (str): The unique identifier for the gene.
        chrm (str): The chromosome on which the gene resides.
    """

    def __init__(self, gene_name, gene_id, rev, chrm, transcripts, organism='hg38'):
        """
        Initialize a Gene instance by loading gene information from stored pickled files.

        Args:
            gene_name (str): Name of the gene (default 'KRAS').
            variation: Variation information (unused currently).
            organism (str): Organism reference build (default 'hg38').

        Raises:
            FileNotFoundError: If no files for the specified gene are found.
            AssertionError: If required attributes are missing after loading.
        """

    def __init__(self, gene_name, gene_id, rev, chrm, transcripts, organism='hg38'):
        self.gene_name = gene_name
        self.gene_id = gene_id
        self.rev = rev
        self.chrm = chrm
        self.organism = organism
        self.transcripts = transcripts if transcripts is not None else {}

    def __repr__(self) -> str:
        """
        Official string representation of the Gene object.
        """
        return f"Gene({self.gene_name})"

    def __str__(self) -> str:
        """
        Unofficial, user-friendly string representation of the Gene object.
        """
        return f"Gene: {self.gene_name}, ID: {self.gene_id}, Chr: {self.chrm}, Transcripts: {len(self.transcripts)}"

    def __len__(self) -> int:
        """
        Returns the number of transcripts associated with this gene.

        Returns:
            int: The count of transcripts.
        """
        return len(self.transcripts)

    def __copy__(self):
        """
        Returns a shallow copy of the Gene object.
        """
        return copy.copy(self)

    def __deepcopy__(self, memo):
        """
        Returns a deep copy of the Gene object.
        """
        return copy.deepcopy(self, memo)

    def __iter__(self):
        """
        Allow iteration over the gene's transcripts, yielding Transcript objects.
        """
        for tid, annotations in self.transcripts.items():
            yield Transcript(annotations, organism=self.organism)

    def __getitem__(self, item):
        print(f"{item} not an annotated transcript of this gene.")
        return Transcript(self.transcripts[item], organism=self.organism) if item in self.transcripts else None

    @classmethod
    def from_file(cls, gene_name, organism='hg38'):
        # Load data from file here

        # Find gene data files in the configured organism MRNA path
        gene_files = list((config[organism]['MRNA_PATH'] / 'protein_coding').glob(f'*_{gene_name}.pkl'))
        if not gene_files:
            print(f"No files available for gene '{gene_name}'.")
            return None
            # raise FileNotFoundError(f"No files available for gene '{gene_name}'.")

        # Load gene data from the first matching file
        data = unload_pickle(gene_files[0])
        gene_name = data.get('gene_name')
        gene_id = data.get('gene_id')
        rev = data.get('rev')
        chrm = data.get('chrm')
        transcripts = data.get('transcripts', {})

        return cls(
            gene_name=gene_name,
            gene_id=gene_id,
            rev=rev,
            chrm=chrm,
            transcripts=transcripts,
            organism=organism
        )

    def splice_sites(self) -> Tuple['Counter', 'Counter']:
        """
        Aggregates splice sites (acceptors and donors) from all transcripts.

        Returns:
            tuple(Counter, Counter): A tuple of two Counters for acceptors and donors.
        """
        from collections import Counter
        acceptors: List[Any] = []
        donors: List[Any] = []

        # Collect acceptor and donor sites from each transcript
        for transcript in self.transcripts.values():
            acceptors.extend(transcript.get('acceptors', []))
            donors.extend(transcript.get('donors', []))

        return Counter(acceptors), Counter(donors)

    def transcript(self, tid: Optional[str] = None):
        """
        Retrieve a Transcript object by ID, or the primary transcript if no ID is given.

        Args:
            tid (str, optional): Transcript ID. If None, returns primary transcript.

        Returns:
            Transcript: The Transcript object with the given ID or the primary transcript.

        Raises:
            AttributeError: If the requested transcript does not exist.
        """
        if tid is None:
            tid = self.primary_transcript

        if tid is None:
            tid = random.choice(list(self.transcripts.keys()))
            return None #Transcript()

        if tid not in self.transcripts:
            return None
            # raise AttributeError(f"Transcript '{tid}' not found in gene '{self.gene_name}'.")

        return Transcript(self.transcripts[tid], organism=self.organism)

    @property
    def primary_transcript(self) -> Optional[str]:
        """
        Returns the primary transcript ID for this gene.
        If not explicitly defined, it attempts to select a primary transcript.
        If none is found, it falls back to the first protein-coding transcript.
        If still none is found, returns None.

        Returns:
            str or None: The primary transcript ID or None if not available.
        """
        # If already calculated, return it
        if hasattr(self, '_primary_transcript'):
            return self._primary_transcript

        # Try to find a primary transcript
        primary_transcripts = [k for k, v in self.transcripts.items() if v.get('primary_transcript')]
        if primary_transcripts:
            self._primary_transcript = primary_transcripts[0]
            return self._primary_transcript

        # Fallback: find a protein-coding transcript
        protein_coding = [k for k, v in self.transcripts.items() if v.get('transcript_biotype') == 'protein_coding']
        if protein_coding:
            self._primary_transcript = protein_coding[0]
            return self._primary_transcript

        # # Fallback 2: find a proitein coding transcript that is not fully defined
        # protein_coding = [k for k, v in self.transcripts.items() if v.get('transcript_biotype') == 'protein_coding_CDS_not_defined']
        # if protein_coding:
        #     self._primary_transcript = protein_coding[0]
        #     return self._primary_transcript

        # No primary or protein-coding transcript found
        self._primary_transcript = None
        return None


