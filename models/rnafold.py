import RNA
from Bio import SeqIO
import time
start_time = time.time()

def get_db(seq):
    fc = RNA.fold_compound(seq)
    (ss, mfe) = fc.mfe()
    return ss, mfe

def read_fasta(filename):
    records = []
    for record in SeqIO.parse(filename, "fasta"):
        head = record.description
        seq = str(record.seq).upper()
        records.append((head, seq))
    return records


def run_rnafold(input_file):
    records = read_fasta(input_file)

    res_dict={}
    for record in records:
        head, seq = record
        db, _ = get_db(seq)
        res_dict[head]=(seq, db)

    return res_dict
