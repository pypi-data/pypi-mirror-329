from input_plus.input_plus import input_plus
from datetime import datetime
from typing import Literal
import re

def input_date(prompt: str, *,
               type: Literal["date", "time", "datetime"] = "datetime",
               default_datetime: datetime | None = datetime.now(),
               hours: Literal["12", "24"] = "24",
               step_with_enter: bool = False) -> datetime:
    '''
    A function that allows the user to input a date using a strptime format string.

    Args:
        prompt: The prompt to display to the user.
        default_datetime: The default date and time to display to the user.
        type: The type of input to get from the user. (date, time, datetime)
        hours: The hour format to use. (12, 24)
        step_with_enter: If True, the user will have to press enter to move to the next field.
    '''
    if type not in ['date', 'time', 'datetime']: raise ValueError('Invalid type.')
    if hours not in ['12', '24']: raise ValueError('Invalid hours.')

    year = default_datetime.year
    month = default_datetime.month
    day = default_datetime.day
    hour = default_datetime.hour
    minute = default_datetime.minute
    second = default_datetime.second

    GREEN_FONT = '\033[92m'
    RED_FONT = '\033[91m'
    RESET_FONT = '\033[0m'
    HIDE_CURSOR = '\033[?25l'
    UNHIDE_CURSOR = '\033[?25h'
    CLEAR_LINE = '\033[K'
    selection_index = 0

    def print_forward(text: str): # Print text and move cursor back to the start of the line
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')  # Regex for ANSI codes
        clean_text = ansi_escape.sub('', text)  # Remove ANSI codes
        return text + '\b' * len(clean_text)  # Move cursor back to the start of the line

    def print_date_time():
        to_print = CLEAR_LINE
        if type == 'date' or type == 'datetime':
            to_print += f'{GREEN_FONT}{str(year).zfill(4)}{RESET_FONT}' if selection_index == 0 else str(year).zfill(4)
            to_print += '-'
            to_print += f'{GREEN_FONT}{str(month).zfill(2)}{RESET_FONT}' if selection_index == 1 else str(month).zfill(2)
            to_print += '-'
            to_print += f'{GREEN_FONT}{str(day).zfill(2)}{RESET_FONT}' if selection_index == 2 else str(day).zfill(2)
        if type == 'datetime':
            to_print += ' ' # Add a space between date and time
        if type == 'time' or type == 'datetime':
            p_hour = (hour % 12 or 12) if hours == '12' else hour
            to_print += f'{GREEN_FONT}{str(p_hour).zfill(2)}{RESET_FONT}' if selection_index == 3 else str(p_hour).zfill(2)
            to_print += ':'
            to_print += f'{GREEN_FONT}{str(minute).zfill(2)}{RESET_FONT}' if selection_index == 4 else str(minute).zfill(2)
            to_print += ':'
            to_print += f'{GREEN_FONT}{str(second).zfill(2)}{RESET_FONT}' if selection_index == 5 else str(second).zfill(2)
            if hours == '12':
                period = f' {"AM" if hour < 12 else "PM"}'
                to_print += f'{GREEN_FONT}{period}{RESET_FONT}' if selection_index == 6 else period
        to_print += HIDE_CURSOR
        return to_print

    def _printer(input_string: str):
        nonlocal year, month, day, hour, minute, second, selection_index
        if input_string.isdigit():
            if selection_index == 0: # Year
                year = int((str(year) + input_string)[-4:])
            elif selection_index == 1: # Month
                month = int((str(month) + input_string)[-2:])
            elif selection_index == 2: # Day
                day = int((str(day) + input_string)[-2:])
            elif selection_index == 3: # Hour
                hour = int((str(hour) + input_string)[-2:])
            elif selection_index == 4: # Minute
                minute = int((str(minute) + input_string)[-2:])
            elif selection_index == 5: # Second
                second = int((str(second) + input_string)[-2:])

        try: # Validate the date
            datetime(year, month, day, hour, minute, second)
            print(print_forward(print_date_time()), end='', flush=True)
        except ValueError as e:
            print(print_forward(f'{print_date_time()} {RED_FONT}\'{str(e)}\'{RESET_FONT}'), end='', flush=True)
        return ''

    def _selector(input_string: str) -> tuple[bool, datetime]:
        nonlocal year, month, day, hour, minute, second, selection_index
        try: # Validate the date
            date_time = datetime(year, month, day, hour, minute, second)
        except ValueError as e:
            return False, None
        
        if step_with_enter:
            _c = selection_index
            add_selection_index(1)
            if selection_index > _c: return False, None # Selection did increase, don't submit

        # Reset the cursor
        selection_index = -1
        print(f'{print_date_time()}{UNHIDE_CURSOR}', end='', flush=True)

        # Return the correct type
        if type == 'datetime':
            return True, date_time
        elif type == 'date':
            return True, date_time.date()
        elif type == 'time':
            return True, date_time.time()
        else:
            raise ValueError('Invalid type.') # This should never happen
    
    def get_month_max_day(month:int, year:int) -> int:
        max_day = 31
        if month in [3, 5, 8, 10]: # April, June, September, November
            max_day = 30
        elif month == 1: # February
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0): # Leap year
                max_day = 29
            else:
                max_day = 28
        return max_day
    
    def add_date_time(*, _year:int = 0, _month:int = 0, _day:int = 0, _hour:int = 0, _minute:int = 0, _second:int = 0) -> datetime:
        nonlocal year, month, day, hour, minute, second
        year += _year
        month = month - 1 + _month # month - 1 to make it 0-indexed
        max_day = get_month_max_day(month, year)
        day = min(day, max_day) - 1 + _day # day - 1 to make it 0-indexed
        hour += _hour
        minute += _minute
        second += _second

        month = (month % 12) + 1 # convert back to 1-indexed
        day = (day % max_day) + 1 # convert back to 1-indexed
        hour = hour % 24
        minute = minute % 60
        second = second % 60
    
    def add_selection_index(offset:int):
        nonlocal selection_index
        selection_index = (selection_index + offset)
        if type == 'datetime':
            if hours == '12': selection_index = selection_index % 7
            else: selection_index = selection_index % 6
        elif type == 'date':
            selection_index = selection_index % 3
        elif type == 'time':
            selection_index -= 3
            selection_index = max(0, selection_index)
            if hours == '12': selection_index = selection_index % 4 + 3
            else: selection_index = selection_index % 3 + 3
        else:
            raise ValueError('Invalid type.') # This should never happen

    def _special_actions(input_string: str):
        nonlocal selection_index
        if   input_string == b'\xc3\xa0H':
            # Up arrow key pressed
            if selection_index == 0:
                add_date_time(_year=1)
            elif selection_index == 1:
                add_date_time(_month=1)
            elif selection_index == 2:
                add_date_time(_day=1)
            elif selection_index == 3:
                add_date_time(_hour=1)
            elif selection_index == 4:
                add_date_time(_minute=1)
            elif selection_index == 5:
                add_date_time(_second=1)
            elif selection_index == 6: # AM/PM
                add_date_time(_hour=12)
        elif input_string == b'\xc3\xa0P':
            # Down arrow key pressed
            if selection_index == 0:
                add_date_time(_year=-1)
            elif selection_index == 1:
                add_date_time(_month=-1)
            elif selection_index == 2:
                add_date_time(_day=-1)
            elif selection_index == 3:
                add_date_time(_hour=-1)
            elif selection_index == 4:
                add_date_time(_minute=-1)
            elif selection_index == 5:
                add_date_time(_second=-1)
            elif selection_index == 6: # AM/PM
                add_date_time(_hour=-12)
        elif input_string == b'\xc3\xa0K':
            # Left arrow key pressed
            if step_with_enter: return
            add_selection_index(-1)
        elif input_string == b'\xc3\xa0M':
            # Right arrow key pressed
            if step_with_enter: return
            add_selection_index(1)
        
    add_selection_index(0)
    if prompt.count('\n') > 0:
        prompt_lines = prompt.split('\n')
        static_prompt = '\n'.join(prompt_lines[:-1]) # Remove the last line of the prompt
        prompt = prompt_lines[-1] # Get the last line of the prompt
        print(static_prompt, flush=True)
    print(prompt, end='', flush=True)
    return input_plus(printer=_printer, selector=_selector, special_actions=_special_actions)