import msvcrt
import re
from typing import Callable, Tuple

_DPP = 0
def _default_printer(input_string: str) -> None:
    global _DPP
    print(f'{'\b \b'*_DPP}{input_string}', end='', flush=True)
    _DPP = len(input_string)
def _default_selector(input_string: str) -> Tuple[bool, str]:
    return True, input_string

def input_plus(printer: Callable[[str], str | None] = _default_printer,
               selector: Callable[[str], Tuple[bool, str]] = _default_selector,
               validator: Callable[[str], bool] = None,
               special_actions: Callable[[bytes], None] = None) -> str:
    '''
    A function that allows for more advanced input handling than the built-in input function.

    Args:
        Printer: A function that renders visual feedback to the user.
            str: This is the string that the user has typed so far.
            returns: str | None, If non None is returned, the input string will be replaced with the returned string.
        Selector: A function that runs when the input is submitted.
            str: This is the final string that the user has typed.
            returns: A tuple containing a boolean indicating if the input is valid and the final input string.
                bool: Indicates if the input is valid. If not true, the input will be blocked and user will keep control.
                str: The final input string.
        Validator: A function that validates each character as it is typed.
            str: This is the string that the user has typed so far.
            returns: bool, If not true, the character will be blocked. (Not added/removed from the input string)
        Special Actions: A function that takes user input string as bytes and performs a special action based on the input.
            bytes: The special key input.
            returns: None
    '''
    input_string = ''
    _p = printer(input_string)
    if _p is not None: input_string = _p
    while True:
        input_char = msvcrt.getwch() # Get the input character
        is_special_key = False

        # Special actions
        if input_char == '\x00' or input_char == '\xe0':
            is_special_key = True
            input_char += msvcrt.getwch()

        char_code = input_char.encode()
        # Control characters
        if char_code == b'\x03': # Ctrl+C
            print()
            raise KeyboardInterrupt
        elif char_code == b'\x0d': # Enter key
            is_valid, value = selector(input_string)
            if is_valid:
                print()
                return value
        elif char_code == b'\x08': # Backspace
            input_string = input_string[:-1]
        elif char_code == b'\x17': # Ctrl+Backspace
            input_string = re.sub(r'((?<=\s)|(?<=^))\w*\s?$', '', input_string)
        elif char_code == b'\x1b': # Escape key
            raise Exception('User escaped input')

        # User inputs
        elif is_special_key and special_actions is not None: # Special keys
            special_actions(char_code)
        else: # Regular characters
            if validator is None or validator(f'{input_string}{input_char}'):
                input_string += input_char

        _p = printer(input_string)
        if _p is not None: input_string = _p