import os
import subprocess

def run_python_file(working_directory, file_path): 
     #making absolute paths
    target = os.path.abspath(os.path.join(working_directory, file_path or ""))
    current = os.path.abspath(working_directory)
    
    # Check if the target directory is within the working directory
    if not os.path.commonpath([current, target]) == current:
        # If the target directory is not within the working directory, return an error message
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target):
        return f'Error: File "{file_path}" not found.'
    
    if not target.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python3",target], capture_output=True, timeout=30)
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        exit_code = result.returncode

        # Build output message
        if not stdout and not stderr:
            print("No output produced.")
        else:
            if stdout:
                print(f"STDOUT:\n{stdout}")
            if stderr:
                print(f"STDERR:\n{stderr}")
            if exit_code != 0:
                print(f"Process exited with code {exit_code}")
    
    except subprocess.TimeoutExpired as e:
        return f"Error: executing Python file: {e}"