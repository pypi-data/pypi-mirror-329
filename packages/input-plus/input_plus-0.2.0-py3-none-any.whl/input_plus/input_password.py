import hashlib
from input_plus.input_plus import input_plus

def _input_password_default_hash(input_string):
    hash_object = hashlib.sha256()
    hash_object.update(input_string.encode())
    hex_digest = hash_object.hexdigest()
    return hex_digest

def input_password(prompt: str, *, mask: str = '', hash_function = _input_password_default_hash) -> str:
    '''
    A function that allows for password input with a custom mask and hash function.

    Args:
        Prompt: The prompt to display to the user.
        Mask: The character to display instead of the input.
        Hash Function: The function to hash the password with.
            Uses SHA-256 by default.
    '''
    # cursor_offset = 0
    print_string_length = 0

    def _printer(input_string):
        nonlocal print_string_length

        # Create the string to print
        print_string = mask * len(input_string)

        # Erase the previous input and print the new one
        erase = '\b' * print_string_length + ' ' * print_string_length + '\b' * print_string_length
        print_string_length = len(print_string) # remove ANSI escape codes
        print(erase + print_string, end='', flush=True)

    def _selector(input_string):
        return True, input_string

    print(prompt, end='', flush=True)
    password = input_plus(_printer, _selector)
    return hash_function(password)