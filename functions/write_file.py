import os

def write_file(working_directory, file_path, content):
    
    #making absolute paths
    target = os.path.abspath(os.path.join(working_directory, file_path or ""))
    current = os.path.abspath(working_directory)
    
    # Check if the target directory is within the working directory
    if not os.path.commonpath([current, target]) == current:
        # If the target directory is not within the working directory, return an error message
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    
    try:
        # If file doesn't exist, create it
        if not os.path.exists(target):
            # Create any parent directories if they don't exist
            os.makedirs(os.path.dirname(target), exist_ok=True)
            # Create an empty file
            with open(target, "w") as f:
                pass  # just create an empty file
            
            # Check if it's now a file (not a directory)
        if not os.path.isfile(target):
            return f'Error: "{file_path}" is not a regular file'

        # Write to files
        with open(target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: Problem writing file: {e}"