import random
import string

def generate_tool_call_id() -> str:
    """
    Generate a unique tool call ID.

    The ID consists of a fixed prefix "call_" followed by a randomly 
    generated alphanumeric string of length 24.

    Returns:
        str: A unique tool call ID in the format "call_<random_string>".
    """
    prefix = "call_"
    characters = string.ascii_letters + string.digits
    length = 24
    random_string = ''.join(random.choices(characters, k=length))
    
    return prefix + random_string
