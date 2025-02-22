from typing import List, TypedDict
from colorama import Fore, Style
from input_plus.input_plus import input_plus
import Levenshtein

class Option(TypedDict):
    Option: str
    Description: str

def option(*, option: str, description: str = '') -> Option:
    return {'Option': option, 'Description': description}

def input_select(prompt: str, options: list[str | Option], *,
    list_size: int = 5, fixed_order: bool = False) -> str:
    '''
    A function that allows for selecting an option from a list of options.

    Args:
        Prompt: The prompt to display before the input.
        Options: A list of options to select from. Can be a list of strings or a list of dictionaries with the keys 'Option' and 'Description'.
        List Size: The number of options to display at once.
        Fixed Order: If True, the options will be displayed in the order they are provided and can not be searched.
    '''
    mapped_options: List[Option] = []
    for option in options:
        if isinstance(option, str): mapped_options.append({'Option': option, 'Description': ''})
        else:
            if option.get('Option') is None: raise ValueError('Option dictionary must contain key "Option"')
            if option.get('Description') is None: option['Description'] = ''
            mapped_options.append(option)

    list_size = min(list_size, len(mapped_options)) # Ensure list_size is not greater than the number of options
    height = 0
    select_index = 0
    offset = 0

    def get_options_scores(input_string):
        # get the levenstein distance of each option
        option_scores = [{
            'option': option['Option'],
            'description': option['Description'],
            'score': Levenshtein.distance(input_string, option['Option']) if not fixed_order else 0
            } for option in mapped_options]
        # sort the options by score descending
        option_scores = sorted(option_scores, key=lambda x: x['score'])
        # get the top list_size options
        option_scores = option_scores[offset:list_size + offset]
        return option_scores

    def _printer(input_string):
        nonlocal height, list_size, select_index, offset
        if fixed_order: input_string = ''

        MOVE_TO_START = '\r' # Move the cursor to the start of the line
        CURSOR_FORWARD = '\x1b[C' # Move the cursor forward one character
        CLEAR_LINE = '\033[J' # Clear the current line

        # store all text to print to remove flickering
        to_print = ''

        # Clear previous lines
        to_print += f'{MOVE_TO_START}{CLEAR_LINE}' * height
        to_print += f'{prompt}{input_string}\n'
        height = prompt.count('\n')

        option_scores = get_options_scores(input_string)

        selected_option = option_scores[select_index]
        if selected_option["description"]:
            to_print += f'{Fore.LIGHTYELLOW_EX}{selected_option["description"]}{Style.RESET_ALL}\n'
            height += selected_option["description"].count('\n') + 1

        for i, option_score in enumerate(option_scores):
            temp_text = ''
            if i < len(option_scores) - 1:
                temp_text = f'  {option_score['option']}\n'
            else:
                temp_text = f'  {option_score['option']}'

            if i == select_index:
                temp_text = f'{Fore.GREEN}{temp_text}{Style.RESET_ALL}'

            to_print += temp_text

        height += len(option_scores)

        # Move cursor back to the beginning of the input
        to_print += f'\033[A' * height
        to_print += f'{MOVE_TO_START}{CURSOR_FORWARD * len(f'{prompt.split('\n')[-1]}{input_string}')}'

        print(to_print, end='', flush=True)

    def _selector(input_string):
        nonlocal height, select_index

        MOVE_TO_START = '\r' # Move the cursor to the start of the line
        CLEAR_LINE = '\033[J' # Clear the current line

        # store all text to print to remove flickering
        to_print = ''

        # Clear previous lines
        to_print += f'{MOVE_TO_START}{CLEAR_LINE}' * height
        to_print += MOVE_TO_START

        option_scores = get_options_scores(input_string)
        return_value = option_scores[select_index]['option']

        to_print += f'{prompt}{return_value}'

        print(to_print, end='', flush=True)
        return True, return_value

    def _special_actions(char_code):
        nonlocal select_index, offset

        if char_code == b'\xc3\xa0H': # Up arrow
            if select_index > 0:
                select_index = max(select_index - 1, 0)
            else:
                offset = max(offset - 1, 0)
        elif char_code == b'\xc3\xa0P': # Down arrow
            if select_index < list_size - 1:
                select_index = min(select_index + 1, list_size - 1)
            else:
                offset = min(offset + 1, len(mapped_options) - list_size)

    if prompt.count('\n') > 0:
        prompt_lines = prompt.split('\n')
        static_prompt = '\n'.join(prompt_lines[:-1]) # Remove the last line of the prompt
        prompt = prompt_lines[-1] # Get the last line of the prompt
        print(static_prompt, flush=True)
    return input_plus(_printer, _selector, special_actions=_special_actions)