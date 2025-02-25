from __future__ import annotations

from io import StringIO
from typing import TypeAlias, Iterator

from Bio import Phylo, SeqIO
from Bio.Align import substitution_matrices, Alignment
from Bio.Align.substitution_matrices import Array
from Bio.Blast import Records, parse
from Bio.KEGG import REST
from Bio.PDB.Atom import Atom
from Bio.PDB.Chain import Chain
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB.Model import Model
from Bio.PDB.NeighborSearch import NeighborSearch
from Bio.PDB.PDBIO import PDBIO
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Residue import Residue
from Bio.PDB.Structure import Structure
from Bio.PDB.Superimposer import Superimposer
from Bio.Phylo.BaseTree import Tree
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor, DistanceMatrix
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.motifs import Motif
from Bio.motifs.matrix import PositionSpecificScoringMatrix
from sapiopylib.rest.User import SapioUser

SeqAlias: TypeAlias = Seq | str
TreeAlias: TypeAlias = Tree | str


class BioPythonAliasUtil:
    @staticmethod
    def to_sequence(sequence: SeqAlias) -> Seq:
        """
        Converts the input to a Bio.Seq.Seq object if necessary

        :param sequence: The sequence, either as a Bio.Seq.Seq object or as a string.
        :return: The sequence as a Bio.Seq.Seq object.
        """
        if isinstance(sequence, str):
            return Seq(sequence)
        return sequence

    @staticmethod
    def to_tree(tree: TreeAlias) -> Tree:
        """
        Converts the input to a Bio.Phylo.BaseTree.Tree object if necessary.

        :param tree: The tree, either as a Bio.Phylo.BaseTree.Tree object or as a Newick string.
        :return: The tree as a Bio.Phylo.BaseTree.Tree object
        """
        if isinstance(tree, str):
            with StringIO(tree) as tree_io:
                return Phylo.read(tree_io, "newick")
        return tree


class BioPythonHelper:
    """
    A class designed for simplifying and better documenting the behavior of commonly used BioPython functions.
    """
    user: SapioUser
    exp_id: int
    tab_prefix: str | None

    def __init__(self, user: SapioUser, exp_id: int, tab_prefix: str | None = None):
        """
        :param user: The user to make requests from.
        :param exp_id: The ID of the experiment that the user is in.
        :param tab_prefix: The prefix of the tab for displaying results of functions in. Defaults to None.
        """
        self.user = user
        self.exp_id = exp_id
        self.tab_prefix = tab_prefix

    @staticmethod
    def _parse_pdb_structure(pdb_id: str, file_format: str, file_contents: str | None = None) -> Structure:
        """
        Helper function to parse PDB structures, handling file input and format selection.clade_

        :param pdb_id: PDB ID of the structure. Used only if file_contents is None.
        :param file_format: File format ("pdb", "mmcif", "mmtf", "binarycif").
        :param file_contents: PDB/mmCIF file contents as a string. If provided, takes precedence over pdb_id.
        """
        if file_contents:
            if file_format == "pdb":
                parser = PDBParser()
                with StringIO(file_contents) as pdb_io:
                    structure = parser.get_structure("input_structure", pdb_io)
            elif file_format == "mmcif":
                parser = MMCIFParser()
                with StringIO(file_contents) as mmcif_io:
                    structure = parser.get_structure("input_structure", mmcif_io)
            else:
                raise ValueError("Invalid file format when providing file_contents")
            return structure

        from Bio.PDB import PDBList
        pdbl = PDBList()
        pdb_id = pdb_id.strip().upper()
        if '|' in pdb_id:
            pdb_id = pdb_id.split('|')[0]

        if file_format == "pdb":
            parser = PDBParser()
            file_path = pdbl.retrieve_pdb_file(pdb_id, file_format="pdb", overwrite=True)
            return parser.get_structure(pdb_id, file_path)
        elif file_format == "mmcif":
            parser = MMCIFParser()
            file_path = pdbl.retrieve_pdb_file(pdb_id, file_format="mmcif", overwrite=True)
            return parser.get_structure(pdb_id, file_path)
        elif file_format == "mmtf":
            from Bio.PDB.mmtf import MMTFParser
            parser = MMTFParser()
            return parser.get_structure_from_url(pdb_id)
        elif file_format == "binarycif":
            from Bio.PDB.binary_cif import BinaryCIFParser
            parser = BinaryCIFParser()
            file_path = pdbl.retrieve_pdb_file(pdb_id, file_format="bcif", overwrite=True)  # Corrected file_format
            return parser.get_structure(pdb_id, file_path)
        else:
            raise ValueError("Invalid file format.")

    @staticmethod
    def load_matrix(matrix_name: str) -> Array:
        """
        Loads a substitution matrix from the Bio.Align.substitution_matrices module.

        :param matrix_name: The name of the matrix to load (e.g., "BLOSUM62").
        :return: An Array object representing the substitution matrix.
        """
        return substitution_matrices.load(matrix_name)

    @staticmethod
    def blast_run(blast_output: str) -> Records:
        """
        Parses BLAST output (in plain text format) and returns a Bio.Blast.Records object.

        :param blast_output: BLAST output in plain text format, as a string.
        :return: A Bio.Blast.Records iterator, yielding Bio.Blast.Record objects.
        """
        with StringIO(blast_output) as blast_io:
            blast_records: Records = parse(blast_io)
            return blast_records

    @staticmethod
    def kegg_get(argument: str | list[str]) -> str:
        """
        Retrieves KEGG entries in flat text format using KEGG REST API.

        :param argument: KEGG database entry identifier(s) or command arguments (e.g., "eco:b0002", ["eco:b0002", "eco:b0003"]).
        :return: A string containing the raw text data from KEGG.
        """
        with REST.kegg_get(argument) as handle:
            data: str = handle.read()
        return data

    @staticmethod
    def kegg_list(database: str, arguments: str | None = None) -> str:
        """
        Retrieves a list of entries from a KEGG database using KEGG REST API.

        :param database: KEGG database name (e.g., "pathway", "enzyme", "compound").
        :param arguments: Optional additional arguments for the list command (e.g., "hsa" for human pathways).
            Defaults to None.
        :return: Raw text list of entries from KEGG, as a single string.
        """
        with REST.kegg_list(database, arguments) as handle:
            data: str = handle.read()
        return data

    @staticmethod
    def kegg_find(database: str, query: str, arguments: str | None = None) -> str:
        """
        Finds entries in a KEGG database based on a text query using KEGG REST API.

        :param database: KEGG database name.
        :param query: Search term or query.
        :param arguments: Optional additional arguments for the find command. Defaults to None.
        :return: Raw text list of entries from KEGG matching the query.
        """
        with REST.kegg_find(database, query, arguments) as handle:
            data: str = handle.read()
        return data

    @staticmethod
    def kegg_conv(database1: str, database2: str) -> str:
        """
        Converts identifiers between two KEGG databases using KEGG REST API.

        :param database1: Source KEGG database name or identifier list.
        :param database2: Target KEGG database name.
        :return: Conversion table in raw text format from KEGG.
        """
        with REST.kegg_conv(database1, database2) as handle:
            data: str = handle.read()
        return data

    @staticmethod
    def pdb_parse(pdb_id: str, file_format: str = "pdb", file_contents: str | None = None) -> Structure:
        """
        Parses a PDB, mmCIF, MMTF, or BinaryCIF file and returns a Bio.PDB.Structure object.

        :param pdb_id: PDB ID of the structure. Used only if file_contents is None.
        :param file_format: File format ("pdb", "mmcif", "mmtf", or "binarycif"). Defaults to "pdb".
        :param file_contents: String containing PDB/mmCIF file contents. If provided, takes precedence over pdb_id.
            Defaults to None.
        :return: A Bio.PDB.Structure object representing the parsed structure.
        :raises ValueError: if an invalid file_format is provided.
        """
        return BioPythonHelper._parse_pdb_structure(pdb_id, file_format, file_contents)

    @staticmethod
    def structure_to_pdb_str(structure: Structure, output_format: str = "pdb") -> str:
        """
        Converts a Bio.PDB.Structure object to a PDB-formatted string.

        :param structure: The Bio.PDB.Structure object to convert.
        :param output_format: The desired output format ("pdb" or "mmcif"). Defaults to "pdb".
        :return: A PDB-formatted string.
        :raises ValueError: if an invalid file_format is provided.
        """
        io = PDBIO()
        io.set_structure(structure)
        with StringIO() as out_str:
            if output_format == "pdb":
                io.save(out_str)
            elif output_format == "mmcif":
                # For outputting a string, create a stringIO object
                io = PDBIO(is_pqr=True)
                io.set_structure(structure)
                io.save(out_str)
            else:
                raise ValueError("Invalid output format.")
            pdb_string = out_str.read()
            return pdb_string

    @staticmethod
    def mmcif_parse(pdb_id: str, file_contents: str | None = None) -> dict[str, list[str]]:
        """
        Parses an mmCIF file and returns a dictionary representation.

        :param pdb_id: PDB ID of the structure (used only if file_contents is None).
        :param file_contents: mmCIF file contents as a string. If provided, takes precedence over pdb_id.
            Defaults to None.
        :return: A dictionary mapping mmCIF tags to lists of their values.
        """
        if file_contents:
            with StringIO(file_contents) as mmcif_io:
                return MMCIF2Dict(mmcif_io)

        # Download and parse using MMCIF2Dict directly
        from Bio.PDB import PDBList
        pdbl = PDBList()
        file_path = pdbl.retrieve_pdb_file(pdb_id, file_format="mmcif", overwrite=True)

        return MMCIF2Dict(file_path)

    @staticmethod
    def atom_neighbor_search(pdb_id: str, file_format: str, file_contents: str | None = None,
                             center: tuple[float, float, float] = (0.0, 0.0, 0.0),
                             radius: float = 1.0) -> list[Atom]:
        """
        Finds atom neighbors within a specified radius of a center point in a PDB structure.

        :param pdb_id: PDB ID of the structure. Used only if file_contents is None.
        :param file_format: File format ("pdb" or "mmcif").
        :param file_contents: PDB file contents as a string. If provided, takes precedence over pdb_id.
            Defaults to None.
        :param center: Coordinates of the center point (x, y, z) as a tuple. Defaults to (0.0, 0.0, 0.0).
        :param radius: Search radius in Angstroms. Defaults to 1.0.
        :return: A list of Bio.PDB.Atom objects within the radius.
        :raises ValueError: if an invalid file_format is provided.
        """
        structure = BioPythonHelper._parse_pdb_structure(pdb_id, file_format, file_contents)
        atom_list = list(structure.get_atoms())
        ns = NeighborSearch(atom_list)
        neighbors = ns.search(center, radius, level='A')
        return neighbors

    @staticmethod
    def residue_neighbor_search(pdb_id: str, file_format: str, file_contents: str | None = None,
                                center: tuple[float, float, float] = (0.0, 0.0, 0.0),
                                radius: float = 1.0) -> list[Residue]:
        """
        Finds residue neighbors within a specified radius of a center point in a PDB structure.

        :param pdb_id: PDB ID of the structure. Used only if file_contents is None.
        :param file_format: File format ("pdb" or "mmcif").
        :param file_contents: PDB file contents as a string. If provided, takes precedence over pdb_id. Defaults to None.
        :param center: Coordinates of the center point (x, y, z) as a tuple. Defaults to (0.0, 0.0, 0.0).
        :param radius: Search radius in Angstroms. Defaults to 1.0.
        :return: A list of Bio.PDB.Residue objects within the radius.
        :raises ValueError: if an invalid file_format is provided.
        """
        structure = BioPythonHelper._parse_pdb_structure(pdb_id, file_format, file_contents)
        atom_list = list(structure.get_atoms())
        ns = NeighborSearch(atom_list)
        neighbors = ns.search(center, radius, level='R')
        return neighbors

    @staticmethod
    def chain_neighbor_search(pdb_id: str, file_format: str, file_contents: str | None = None,
                              center: tuple[float, float, float] = (0.0, 0.0, 0.0),
                              radius: float = 1.0) -> list[Chain]:
        """
        Finds chain neighbors within a specified radius of a center point in a PDB structure.

        :param pdb_id: PDB ID of the structure. Used only if file_contents is None.
        :param file_format: File format ("pdb" or "mmcif").
        :param file_contents: PDB file contents as a string. If provided, takes precedence over pdb_id. Defaults to None.
        :param center: Coordinates of the center point (x, y, z) as a tuple. Defaults to (0.0, 0.0, 0.0).
        :param radius: Search radius in Angstroms. Defaults to 1.0.
        :return: A list of Bio.PDB.Chain objects within the radius.
        :raises ValueError: if an invalid file_format is provided.
        """
        structure = BioPythonHelper._parse_pdb_structure(pdb_id, file_format, file_contents)
        atom_list = list(structure.get_atoms())
        ns = NeighborSearch(atom_list)
        neighbors = ns.search(center, radius, level='C')
        return neighbors

    @staticmethod
    def model_neighbor_search(pdb_id: str, file_format: str, file_contents: str | None = None,
                              center: tuple[float, float, float] = (0.0, 0.0, 0.0),
                              radius: float = 1.0) -> list[Model]:
        """
        Finds model neighbors within a specified radius of a center point in a PDB structure.

        :param pdb_id: PDB ID of the structure. Used only if file_contents is None.
        :param file_format: File format ("pdb" or "mmcif").
        :param file_contents: PDB file contents as a string. If provided, takes precedence over pdb_id. Defaults to None.
        :param center: Coordinates of the center point (x, y, z) as a tuple. Defaults to (0.0, 0.0, 0.0).
        :param radius: Search radius in Angstroms. Defaults to 1.0.
        :return: A list of Bio.PDB.Model objects within the radius.
        :raises ValueError: if an invalid file_format is provided.
        """
        structure = BioPythonHelper._parse_pdb_structure(pdb_id, file_format, file_contents)
        atom_list = list(structure.get_atoms())
        ns = NeighborSearch(atom_list)
        neighbors = ns.search(center, radius, level='M')
        return neighbors

    @staticmethod
    def superimpose(fixed_pdb_id: str, moving_pdb_id: str, fixed_file_format: str, moving_file_format: str,
                    fixed_file_contents: str | None = None, moving_file_contents: str | None = None) \
            -> tuple[Superimposer, Structure]:
        """
        Superimposes two PDB structures and returns the Superimposer object and transformed moving PDB string.

        :param fixed_pdb_id: PDB ID of the fixed structure. Used only if fixed_file_contents is None.
        :param moving_pdb_id: PDB ID of the moving structure. Used only if moving_file_contents is None.
        :param fixed_file_format: File format of the fixed structure ("pdb" or "mmcif").
        :param moving_file_format: File format of the moving structure ("pdb" or "mmcif").
        :param fixed_file_contents: Fixed PDB/mmCIF file contents. If provided, takes precedence over fixed_pdb_id.
            Defaults to None.
        :param moving_file_contents: Moving PDB/mmCIF file contents. If provided, takes precedence over moving_pdb_id.
            Defaults to None.
        :return: A tuple containing:
             - The Bio.PDB.Superimposer object, which contains rotation/translation information.
             - The Bio.PDB.Structure object of the moving structure after transformation.
        :raises ValueError: if the fixed and moving structures have different numbers of atoms.
        :raises ValueError: if an invalid file_format is provided.
        """
        fixed_structure = BioPythonHelper._parse_pdb_structure(fixed_pdb_id, fixed_file_format, fixed_file_contents)
        moving_structure = BioPythonHelper._parse_pdb_structure(moving_pdb_id, moving_file_format, moving_file_contents)

        super_imposer = Superimposer()
        fixed_atoms = list(fixed_structure.get_atoms())
        moving_atoms = list(moving_structure.get_atoms())

        if len(fixed_atoms) != len(moving_atoms):
            raise ValueError("Fixed and moving structures must have the same number of atoms.")

        super_imposer.set_atoms(fixed_atoms, moving_atoms)
        super_imposer.apply(moving_atoms)

        return super_imposer, moving_structure

    @staticmethod
    def distance_tree(sequences: dict[str, str], method: str = "nj", distance_model: str = "blosum62") -> Tree:
        """
        Constructs a UPGMA or Neighbor Joining tree from a set of sequences.

        :param sequences: Dictionary of sequences, where keys are sequence IDs and values are sequences (strings).
        :param method: Tree construction method ('upgma' or 'nj'). Defaults to 'nj'
        :param distance_model: The distance model to use for the distance matrix. Defaults to 'blosum62'
        :return: A Bio.Phylo.BaseTree.Tree object representing the constructed tree.
        """
        # Create SeqRecord objects
        seq_records = [SeqRecord(Seq(seq), id=seq_id) for seq_id, seq in sequences.items()]

        # Calculate Distance Matrix
        from Bio.Phylo.TreeConstruction import DistanceCalculator
        calculator = DistanceCalculator(distance_model)  # distance model such as 'blosum62'
        dm: DistanceMatrix = calculator.get_distance(seq_records)

        # Construct Tree
        constructor = DistanceTreeConstructor()
        if method == "upgma":
            tree: Tree = constructor.upgma(dm)
        elif method == "nj":
            tree: Tree = constructor.nj(dm)
        else:
            raise ValueError("Invalid tree construction method. Choose 'upgma' or 'nj'.")
        return tree

    @staticmethod
    def newick_to_tree(newick_string: str) -> Tree:
        """
        Converts a newick string to a tree object.

        :param newick_string: The newick string to be converted.
        :return: The tree object.
        """
        with StringIO(newick_string) as tree_io:
            tree: Tree = Phylo.read(tree_io, "newick")
        return tree

    @staticmethod
    def tree_to_newick(tree: Tree) -> str:
        """
        Converts a tree object to a newick string.

        :param tree: The tree to be converted, in the Bio.Phylo.BaseTree.Tree format.
        :return: The newick string representing the tree.
        """
        with StringIO() as tree_io:
            Phylo.write(tree, tree_io, "newick")
            return tree_io.read()

    @staticmethod
    def clade_get_terminals(tree: TreeAlias) -> list[str]:
        """
        Gets the terminal nodes of a phylogenetic tree.

        :param tree: Tree object or Newick formatted tree string.
        :return: List of terminal clade names (strings).
        """
        tree = BioPythonAliasUtil.to_tree(tree)
        return [clade.name for clade in tree.get_terminals()]

    @staticmethod
    def clade_get_nonterminals(tree: TreeAlias) -> list[str]:
        """
        Gets the non-terminal nodes of a phylogenetic tree.

        :param tree: Tree object or Newick formatted tree string.
        :return: List of non-terminal clade names (strings).
        """
        tree = BioPythonAliasUtil.to_tree(tree)
        return [clade.name for clade in tree.get_nonterminals()]

    @staticmethod
    def clade_common_ancestor_by_targets(tree: TreeAlias, target1: str, target2: str) -> str:
        """
        Finds the common ancestor of two target clades in a tree.
        :param tree: Tree object or Newick formatted tree string.
        :param target1: Target clade name.
        :param target2: Second target clade name.
        :return: Name of the common ancestor clade (string)
        """
        tree = BioPythonAliasUtil.to_tree(tree)
        ancestor = tree.common_ancestor(target1, target2)
        return ancestor.name if ancestor else "Unnamed"

    @staticmethod
    def clade_common_ancestor_by_taxa(tree: TreeAlias, taxa: list[str]) -> str:
        """
        Finds the common ancestor of a list of taxa
        :param tree: Tree object or Newick formatted tree string.
        :param taxa: List of taxa.
        :return: Name of the common ancestor clade (string)
        """
        tree = BioPythonAliasUtil.to_tree(tree)
        ancestor = tree.common_ancestor(*taxa)
        return ancestor.name if ancestor else "Unnamed"

    @staticmethod
    def clade_distance(tree: TreeAlias, target1: str, target2: str) -> float:
        """
        Calculates the distance between two clades in a phylogenetic tree.

        :param tree: Tree object or Newick formatted tree string.
        :param target1: Target clade name.
        :param target2: Second target clade name.
        :return: Distance between two clades (float).
        :raises ValueError: If targets are not provided
        """
        tree = BioPythonAliasUtil.to_tree(tree)
        if not (target1 and target2):
            raise ValueError("Must Provide Two Targets")
        return tree.distance(target1, target2)

    @staticmethod
    def clade_total_branch_length(tree: TreeAlias) -> float:
        """
        Calculates the total branch length of a phylogenetic tree.

        :param tree: Tree object or Newick formatted tree string.
        :return: Total branch length of the tree (float).
        """
        tree = BioPythonAliasUtil.to_tree(tree)
        return tree.total_branch_length()

    @staticmethod
    def clade_depths(tree: TreeAlias, unit_branch_lengths: bool = False) -> dict[str, float]:
        """
        Calculates the depths of clades in a phylogenetic tree.

        :param tree: Tree object or Newick formatted tree string.
        :param unit_branch_lengths: If True, calculate depths using unit branch lengths. Defaults to False.
        :return: Dictionary mapping clade names to depths (float).
        """
        tree = BioPythonAliasUtil.to_tree(tree)
        depths_dict = tree.depths(unit_branch_lengths=unit_branch_lengths)
        return {(clade.name if clade.name else str(clade)): depth for clade, depth in depths_dict.items()}

    @staticmethod
    def motif_analysis(sequences: list[SeqAlias], alphabet: str = "ACGT") -> Motif:
        """
        Run a sequence motif analysis on the given sequences.

        :param sequences: A list of DNA sequences, either in the form of strings or of Bio.Seq.Seq objects.
        :param alphabet: The alphabet used in the DNA sequences. Defaults to ACGT.
        :return: The sequence motif Bio.motifs.Motif object analysing the given sequence.
        """
        alignment = Alignment([BioPythonAliasUtil.to_sequence(seq) for seq in sequences])
        return Motif(alphabet=alphabet, alignment=alignment)

    @staticmethod
    def pssm_search(pssm: PositionSpecificScoringMatrix, sequence: SeqAlias,
                    threshold: float = 0.0, both_strands: bool = True) -> list[tuple[int, float]]:
        """
        :param pssm: The position specific scoring matrix to run the search on.
        :param sequence: The sequence to search for, either as a string or already wrapped as a Bio.Seq object.
        :param threshold: The threshold above which the Position Weight Matrix score must be for a hit to be returned
            as a match. Defaults to 0.0.
        :param both_strands: Whether both sides of the DNA sequence should be searched for hits. Defaults to True.
        :return: A list of tuples for each hit in the sequence. The tuple is a pair of integers, the first being the
            position of the hit and the second being the score of the hit. Negative positions correspond to positions
            on the other side of the strand of DNA.
        """
        sequence = BioPythonAliasUtil.to_sequence(sequence)
        matches: list[tuple[int, float]] = list(pssm.search(sequence, threshold=threshold, both=both_strands))
        return matches

    @staticmethod
    def read_sequence(file_path: str, seq_format: str) -> SeqRecord:
        """
        Reads a single sequence record from a file using Bio.SeqIO.read.

        :param file_path: Path to the sequence file.
        :param seq_format: Format of the sequence file (e.g., "fasta", "genbank").
        :return: A single SeqRecord object.
        :raises: ValueError if the file contains more than one record
        """
        return SeqIO.read(file_path, seq_format)

    @staticmethod
    def parse_sequences(file_path: str, seq_format: str) -> Iterator[SeqRecord]:
        """
        Parses multiple sequence records from a file using Bio.SeqIO.parse

        :param file_path: Path to the sequence file.
        :param seq_format: Format of the sequence file (e.g., "fasta", "genbank").
        :return: An iterator yielding SeqRecord objects.
        """
        return SeqIO.parse(file_path, seq_format)

    @staticmethod
    def write_sequences(sequences: list[SeqRecord], file_path: str, seq_format: str) -> int:
        """
        Writes a list of SeqRecord objects to a file using Bio.SeqIO.write.

        :param sequences: List of SeqRecord objects to write.
        :param file_path: Output file path.
        :param seq_format: Output sequence format (e.g., "fasta", "genbank").
        :return: The number of records written.
        """
        return SeqIO.write(sequences, file_path, seq_format)

    @staticmethod
    def convert_sequence_format(input_file: str, input_format: str, output_file: str, output_format: str) -> int:
        """
        Converts a sequence file from one format to another using Bio.SeqIO.convert.

        :param input_file: Path to the input sequence file.
        :param input_format: Format of the input file (e.g., "genbank").
        :param output_file: Path to the output sequence file.
        :param output_format: Desired format of the output file (e.g., "fasta").
        :return: The number of records converted.
        """
        return SeqIO.convert(input_file, input_format, output_file, output_format)

    @staticmethod
    def reverse_complement(sequence: SeqAlias) -> Seq:
        """
        Calculates the reverse complement of a DNA sequence.

        :param sequence: The DNA sequence (string or Seq object).
        :return: The reverse complement as a Seq object.
        """
        return BioPythonAliasUtil.to_sequence(sequence).reverse_complement()

    @staticmethod
    def transcribe(dna_sequence: SeqAlias) -> Seq:
        """
        Transcribes a DNA sequence to RNA.

        :param dna_sequence: The DNA sequence (string or Seq object).
        :return: The transcribed RNA sequence as a Seq object.
        """
        return BioPythonAliasUtil.to_sequence(dna_sequence).transcribe()

    @staticmethod
    def back_transcribe(rna_sequence: SeqAlias) -> Seq:
        """
        Back-transcribes an RNA sequence to DNA.

        :param rna_sequence: The RNA sequence (string or Seq object).
        :return: The back-transcribed DNA sequence as a Seq object.
        """
        return BioPythonAliasUtil.to_sequence(rna_sequence).back_transcribe()

    @staticmethod
    def translate(sequence: SeqAlias, table: str | int = "Standard", to_stop: bool = False) -> Seq:
        """
        Translates a nucleotide sequence to a protein sequence.

        :param sequence: The nucleotide sequence (string or Seq object).
        :param table: The genetic code table to use (string or integer). Defaults to "Standard".
        :param to_stop: If True, translation stops at the first in-frame stop codon. Defaults to False.
        :return: The translated protein sequence as a Seq object.
        """
        return BioPythonAliasUtil.to_sequence(sequence).translate(table=table, to_stop=to_stop)
