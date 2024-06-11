import subprocess
import torch
import os


def run_knotfold(input_file: str, output_directory: str = "file_cache") -> dict[str, tuple[str, str]]:
    """
    Run KnotFold on the input file and return the results as a dictionary.
    :param input_file: A file containing the sequences to predict the secondary structure for.
    :param output_directory: The directory to save the temporary output files.
    :return: A dictionary containing the results in the format {header: (sequence, dot_bracket)}.

    Example:
    >>> results = run_knotfold('test.fasta')
    """
    # Read the input file
    with open(input_file, "r") as file:
        sequences = file.read().split(">")[1:]

    res_dict = {}
    temp_file = os.path.join(output_directory, "KF_temp")
    temp_result = os.path.join(output_directory, "KF_temp_res.bpseq")

    for SEQ in sequences:
        # Write the sequence to a temporary file
        with open(temp_file, "w") as temp:
            temp.write(SEQ)
        header = SEQ.split("\n")[0]
        sequence = SEQ.split("\n")[1]

        # Construct the command
        command1 = ['python', 'models/KnotFold/KnotFold.py', '-i', temp_file, '-o', output_directory]

        # Add the --cuda option if GPU is available
        if torch.cuda.is_available():
            command1.append('--cuda')

        # Run the command
        subprocess.run(command1)

        # Convert bpseq file into dot-bracket string
        command2 = ['rnaConvert.py', temp_result, '-T', 'dotbracket']
        dot_bracket = subprocess.run(command2, capture_output=True, text=True)

        # Add results to the final dict
        res_dict[header] = (sequence, dot_bracket.stdout.strip())

    os.remove(temp_file)
    os.remove(temp_result)

    return res_dict
