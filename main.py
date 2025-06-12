import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file 
from functions.write_file import write_file


# Load environment variables
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Set up the Gemini client
client = genai.Client(api_key=api_key)

# Check if prompt is provided
if len(sys.argv) < 2:
    print("Usage: python main.py \"<prompt>\" [--verbose]")
    sys.exit(1)
    

# Extract user prompt and check for verbose flag
user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

# System Prompt For Testing
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Format message
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file where content will be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)



available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content,
        schema_run_python_file, schema_write_file
    ]
)


# Make the API call
if len(sys.argv) > 1:
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions],),
    )
else:
    print("Please provide a prompt as a command line argument.")
    sys.exit(1)
    
    
prompt_token_count = response.usage_metadata.prompt_token_count
candidate_token_count = response.usage_metadata.candidates_token_count
   
        
def call_function(function_call, verbose=False):
    # Checking if the verbose flag is on and printing accordingly
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    # Setting up working directory 
    working_directory = "./calculator"
    
    # Making a function map to call the functions
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    # Extracting function name and arguments
    function_name = function_call.name
    function_args = dict(function_call.args)
    
    # Adding working directory to dict of arguments
    function_args["working_directory"] = working_directory
    
    # Checking if the function name is valid
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        function_result = function_map[function_name](**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            ],
        )
    
    
    
function_calls = response.function_calls
# Check if there are any function calls in the response
if function_calls:
    for function_call in function_calls:
        # Call the function and get the Content response
        function_result = call_function(function_call, verbose=verbose)

        # Validate function response structure
        if not function_result.parts or not hasattr(function_result.parts[0], "function_response"):
            raise RuntimeError("Fatal: Function response structure is invalid or missing.")

        # Extract response
        response_data = function_result.parts[0].function_response.response

        # Check presence of 'result' or 'error'
        if not response_data:
            raise RuntimeError("Fatal: Function response is empty.")

        # Print if verbose is set
        if verbose:
            print(f"-> {response_data}")
else: 
    # Print the response
    print(response.text)

    # Print usage metadata if verbose flag is set
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidate_token_count}")