import os

def get_files_info(working_directory, directory=None):
    
    #making absolute paths
    target = os.path.abspath(os.path.join(working_directory, directory or ""))
    current = os.path.abspath(working_directory)

    
    # Check if the target directory is within the working directory
    if not os.path.commonpath([current, target]) == current:
        # If the target directory is not within the working directory, return an error message
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target):
        return f'Error: "{directory}" is not a directory'
    
    try:
        contents = os.listdir(target)
        result = []  
        if not contents:
            return f'Error: "{directory}" is empty'
        for item in contents:
            file_info = item + ": file_size=" + str(os.path.getsize(os.path.join(target, item))) + " bytes, is_dir=" + str(os.path.isdir(os.path.join(target, item)))   
            result.append(file_info)
        return "\n".join(result)
    except Exception as e:
        return f"Error listing files: {e}"
    
    
    