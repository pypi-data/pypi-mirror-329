from input_plus.input_plus import input_plus
from colorama import Fore, Style
import re

def input_regex(prompt: str, regex: str, *, force_match: bool = False, warn_error: bool = True, placeholder: str = None) -> str:
    '''
    Use a regular expression to validate input.

    Args:
        prompt: The prompt to display to the user.
        regex: The regular expression to validate the input.
        force_match: If True, the input will be ignored if it does not match the regex.
        warn_error: If True, the input will be displayed in red if it does not match the regex.
        placeholder: String to show as a gray text to show the expected format.
    '''
    cursor_offset = 0
    print_string_length = 0

    # Printer function
    def _printer(input_string):
        nonlocal cursor_offset, print_string_length

        WARNING_COLOR = Fore.RED
        WARNING_RESET = Style.RESET_ALL
        CURSOR_BACK = '\b' # Move the cursor back one character
        CURSOR_FORWARD = '\x1b[C' # Move the cursor forward one character
        REMOVE_ANSI_ESCAPES = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

        # Move the cursor to the beginning of the line
        print(CURSOR_FORWARD * cursor_offset, end='', flush=True)
        cursor_offset = 0

        # Create the string to print
        print_string = input_string
        if not force_match and warn_error:
            # replace all matches with the warning color
            print_string = re.sub(regex, WARNING_RESET + r'\g<0>' + WARNING_COLOR, input_string)
            print_string = f'{WARNING_COLOR}{print_string}{WARNING_RESET}'

        # Add a placeholder if needed in gray
        if placeholder is not None:
            string_to_add = f'     {Fore.LIGHTBLACK_EX}{placeholder}{Style.RESET_ALL}'
            cursor_offset += len(REMOVE_ANSI_ESCAPES.sub('', string_to_add)) # remove ANSI escape codes
            print_string += string_to_add

        # Erase the previous input and print the new one
        erase = '\b' * print_string_length + ' ' * print_string_length + '\b' * print_string_length
        print_string_length = len(REMOVE_ANSI_ESCAPES.sub('', print_string)) # remove ANSI escape codes
        print(erase + print_string, end='', flush=True)

        # Move the cursor back to the correct position
        print(CURSOR_BACK * cursor_offset, end='', flush=True)

    def _selector(input_string):
        is_valid = re.fullmatch(regex, input_string) is not None
        return is_valid, input_string

    def _validator(input_string):
        if force_match:
            return re.fullmatch(regex, input_string) is not None
        return True

    print(prompt, end='', flush=True)
    return input_plus(_printer, _selector, validator=_validator)

#region Common Regex Patterns

def input_integer(prompt: str) -> int:
    '''
    A function that takes a prompt and returns an integer.

    Args:
        Prompt: The prompt to display to the user.
    '''
    value = input_regex(prompt, r'\-?\d*', force_match=True)
    if value == '' or value == '-':
        return 0
    return int(value)

def input_float(prompt: str) -> float:
    '''
    A function that takes a prompt and returns a float.

    Args:
        prompt: The prompt to display to the user.
    '''
    value = input_regex(prompt, r'\-?\d*\.?\d*?', force_match=True)
    if value == '' or value == '-' or value == '.':
        return 0
    return float(value)

def input_email(prompt: str) -> str:
    '''
    A function that takes a prompt and returns an email address.

    Args:
        prompt: The prompt to display to the user.
    '''
    return input_regex(prompt, r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def input_phone(prompt: str) -> str:
    '''
    A function that takes a prompt and returns a phone number.

    Args:
        prompt: The prompt to display to the user.
    '''
    return input_regex(prompt, r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}')

def input_url(prompt: str) -> str:
    '''
    A function that takes a prompt and returns a URL.

    Args:
        prompt: The prompt to display to the
    '''
    return input_regex(prompt, r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

def input_hex(prompt: str) -> str:
    '''
    A function that takes a prompt and returns a hexadecimal number.

    Args:
        prompt: The prompt to display to the user.
    '''
    return input_regex(prompt, r'[0-9a-fA-F]+')

#endregion