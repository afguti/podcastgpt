import tiktoken
# If tiktoken not installed. Install with pip install --upgrade tiktoken

# Source: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

code = "cl100k_base"

encoding = tiktoken.get_encoding(code)

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def counter(texto: str, model: str):
    #here we define the model
    result = num_tokens_from_string(texto, code)
    return result