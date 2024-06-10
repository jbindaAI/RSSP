import os.path
import subprocess


def run_rnastructure_fold(
        input_file: str,
        output_directory: str = "file_cache",
        rnastructure_path: str = "/home/jbinda/RSSP/models/RNAstructure") -> dict[str, tuple[str, str]]:
    """
    Run RNAstructure Fold on the input file and return the results as a dictionary.
    :param input_file: A file containing the sequences to predict the secondary structure for.
    :param output_directory: The directory to save the temporary output files.
    :param rnastructure_path: The path to the RNAstructure installation directory.
    :return: A dictionary containing the results in the format {header: (sequence, dot_bracket)}.

    Example:
    >>> results = run_rnastructure_fold('test.fasta')
    """
    # Check if the DATAPATH environment variable is set
    if not os.environ.get('DATAPATH') and not rnastructure_path:
        raise ValueError(
            "Please set the DATAPATH environment variable to the path of the RNAstructure/data_tables directory"
        )
    elif not os.environ.get('DATAPATH'):
        os.environ['DATAPATH'] = os.path.join(rnastructure_path, 'data_tables')
    # Set the RNAstructure path to the parent directory of the data_tables directory
    rnastructure_path = os.path.dirname(os.environ['DATAPATH'])
    fold_command = os.path.join(rnastructure_path, 'exe/Fold')
    ct2dot_command = os.path.join(rnastructure_path, 'exe/ct2dot')

    # Read the input file
    with open(input_file, "r") as file:
        sequences = file.read().split(">")[1:]

    res_dict = {}
    temp_file = os.path.join(output_directory, "temp_rnastructure")
    temp_result = os.path.join(output_directory, "result.ct")

    for i, seq in enumerate(sequences):
        # Write the sequence to a temporary file
        with open(temp_file, "w") as temp:
            temp.write('>' + seq)

        header = seq.split("\n")[0]
        sequence = seq.split("\n")[1]

        # run Fold
        command = [fold_command, temp_file, temp_result]
        subprocess.run(command)

        # convert to dot-bracket string
        command2 = [ct2dot_command, temp_result, '-1', '-']
        dot_bracket = subprocess.run(command2, capture_output=True, text=True)
        dot_bracket = dot_bracket.stdout.splitlines()[-1]

        # Add results to the final dict
        res_dict[header] = (sequence, dot_bracket)

    os.remove(temp_file)
    os.remove(temp_result)

    return res_dict


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Please provide an input file as an argument")
        sys.exit(1)
    example_file = sys.argv[1]

    res = run_rnastructure_fold(example_file)
    print(res)
