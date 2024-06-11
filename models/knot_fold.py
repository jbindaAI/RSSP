import subprocess
import torch
import os


def run_knotfold(input_file, output_directory="file_cache"):
    with open(input_file, "r") as file:
        sequences = file.read().split(">")[1:]
    res_dict = {}
    for SEQ in sequences:
        with open("file_cache/KF_temp", "w") as temp:
            temp.write(SEQ)
        header = SEQ.split("\n")[0]
        sequence = SEQ.split("\n")[1]

        # Construct the command
        command1 = ['python', 'models/KnotFold/KnotFold.py', '-i', "file_cache/KF_temp", '-o', output_directory]

        # Add the --cuda option if GPU is available
        if torch.cuda.is_available():
            command1.append('--cuda')

        # Run the command
        subprocess.run(command1, capture_output=False)
        os.remove("file_cache/KF_temp")

        # Convert bpse file into dot-bracket string
        command2 = ['rnaConvert.py', 'file_cache/KF_temp_res.bpseq', '-T', "dotbracket"]
        dot_bracket = subprocess.run(command2, capture_output=True, text=True)
        os.remove("file_cache/KF_temp_res.bpseq")

        # Add results to the final dict
        res_dict[header] = (sequence, dot_bracket.stdout.strip())

    return res_dict

# Example usage
#input_file = 'file_cache/cache.fasta'

#res = run_knotfold(input_file)
#print(res)
