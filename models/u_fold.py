import shutil
import subprocess

def run_ufold(input_file):

    # from UFold README: put fasta file (named input.txt) into data folder
    shutil.copy(input_file, 'models/UFold/data/input.txt')
    command = ['python', 'models/UFold/ufold_predict.py']
    subprocess.run(command, capture_output=True, text=True)

    # from UFold README: get the output ct file, bpseq file, and figures in the results folder
    sequences = open('models/UFold/results/input_dot_ct_file.txt', 'r').read().split(">")[1:]
    res_dict={}
    for seq in sequences:
        res_dict[seq.split("\n")[0]]=(seq.split("\n")[1], seq.split("\n")[2])
    
    # dict with sequence headers as keys and (sequence, dot-bracket representation) tuples as values
    return res_dict


# Example usage
# res = run_ufold('input.fasta')
# print(res)