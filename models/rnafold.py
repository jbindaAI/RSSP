import RNA
from Bio import SeqIO


def get_db(seq: str) -> tuple[str, float]:
    """
    Get the dot-bracket notation and minimum free energy for a given sequence using the RNAfold method.
    :param seq: A sequence to predict the secondary structure for.
    :return: The dot-bracket notation and minimum free energy.
    """
    fold_compound = RNA.fold_compound(seq)
    (secondary_structure, minimum_free_energy) = fold_compound.mfe()
    return secondary_structure, minimum_free_energy


def read_fasta(filename: str) -> list[tuple[str, str]]:
    """
    Read fasta file and return a list of tuples with header and sequence.
    :param filename: A fasta file.
    :return: List of tuples with header and sequence.
    """
    records = []
    for record in SeqIO.parse(filename, "fasta"):
        head = record.description
        seq = str(record.seq).upper()
        records.append((head, seq))
    return records


def run_rnafold(input_file: str) -> dict[str, tuple[str, str]]:
    """
    Run RNAfold on the input file and return the results as a dictionary.
    :param input_file: A file containing the sequences to predict the secondary structure for.
    :return: A dictionary containing the results in the format {header: (sequence, dot_bracket)}.
    """
    records = read_fasta(input_file)

    res_dict = {}
    for record in records:
        head, seq = record
        secondary_structure, _ = get_db(seq)
        res_dict[head] = (seq, secondary_structure)

    return res_dict
