import subprocess


def run_mxfold2(input_file: str) -> dict[str, tuple[str, str]]:
    """
    Run mxfold2 on the input file and return the results as a dictionary.
    :param input_file: A file containing the sequences to predict the secondary structure for.
    :return: A dictionary containing the results in the format {header: (sequence, dot_bracket)}.
    """
    # Construct the command
    command = ['mxfold2', 'predict', input_file]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    mx_fold_res = result.stdout.split(">")[1:]
    res_dict = {}
    for elt in mx_fold_res:
        content = elt.split("\n")
        res_dict[content[0]] = (content[1].strip(), content[2].split()[0].strip())

    return res_dict
