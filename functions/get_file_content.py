import os


MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
     #making absolute paths
    target = os.path.abspath(os.path.join(working_directory, file_path or ""))
    current = os.path.abspath(working_directory)

    
    # Check if the target directory is within the working directory
    if not os.path.commonpath([current, target]) == current:
        # If the target directory is not within the working directory, return an error message
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == MAX_CHARS:
            file_content_string = file_content_string + "  " + file_path + " truncated at 10000 characters"
        return file_content_string  # Keep line endings
    except Exception as e:
        return f"Error: Problem reading file: {e}"