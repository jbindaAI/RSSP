import subprocess


def run_mxfold2(input_file):
    # Construct the command
    command = ['mxfold2', 'predict', input_file]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    mx_fold_res = result.stdout.split(">")[1:]
    temp_dict = {}
    for elt in mx_fold_res:
        content = elt.split("\n")
        temp_dict[content[0]] = (content[1].strip(), content[2].split()[0].strip())

    return temp_dict
