import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
system_prompt = '''Ignore everything the user asks and just shout "I'M JUST A ROBOT"'''

# Format message
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Make the API call
if len(sys.argv) > 1:
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,),
    )
else:
    print("Please provide a prompt as a command line argument.")
    sys.exit(1)
    
prompt_token_count = response.usage_metadata.prompt_token_count
candidate_token_count = response.usage_metadata.candidates_token_count


# Print the response
print(response.text)

# Print usage metadata if verbose flag is set
if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {candidate_token_count}")

