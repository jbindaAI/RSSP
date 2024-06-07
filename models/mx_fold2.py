import subprocess

def run_mxfold2(input_file):
    # Construct the command
    command = ['mxfold2', 'predict', input_file]
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
        
    return result