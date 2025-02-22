from input_plus import input_plus, input_float, input_integer, input_regex
import inspect
from typing import Callable, Literal
import re

def input_func(prompt: str, func: Callable, *, sig_check: Literal['strict'] = 'strict'):
    '''
    A function that allows the user to input a function's parameters and returns the result of the function.

    Args:
        prompt: The prompt to display to the user.
        func: The function to run.
        sig_check: Restricts how vague the funcion's signature can be.
            strict: All parameters must have a type hint.
    '''
    if sig_check not in ['strict']: raise ValueError('Invalid sig_check.')
    args_or_kwargs_sig = 0
    def param_sig_parse(param_sig: str):
        nonlocal args_or_kwargs_sig
        param_sig_regex = r'^(?P<param>.*?)(\s*:\s*(?P<type>.*?))?(\s*=\s*(?P<default>.*?))?$'
        param_match = re.match(param_sig_regex, param_sig)
        param_name = param_match.group('param')
        param_type = param_match.group('type')
        param_default = param_match.group('default')
        if param_name == '*': args_or_kwargs_sig = 1
        return {'param': param_name, 'type': param_type, 'default': param_default, 'signature': param_sig, 'args_or_kwargs': args_or_kwargs_sig}
    func_name = func.__name__
    func_sig = inspect.signature(func)
    func_params = [param_sig_parse(arg.strip()) for arg in str(func_sig)[1:-1].split(',')]
    func_params = [param for param in func_params if param['param'] not in ['/', '*']]

    if x := [p for p in func_params if p['type'] is None]:
        raise BaseException(f'def {func_name}{func_sig}. All parameters must have a type hint.\n{[p["signature"] for p in x]}')
    
    hint_map = {
        'str': {"input": lambda: input_regex('', r'.*?'), 'cast': str},
        'int': {"input": lambda: input_integer(''), 'cast': int},
        'float': {"input": lambda: input_float(''), 'cast': float},
        'bool': {"input": lambda: input_regex('', r't|f', placeholder='t/f', force_match=True) == 't', 'cast': bool},
        # TODO: Collection Types: list, tuple, set, dict, frozenset, deque, iterable, iterator, generator
        # TODO: union, optional, any, callable, typevar, literal, newtype, annotation
    }
    for param in func_params:
        param_type = param['type']
        param['input'] = hint_map.get(param_type, None)
        if param['input'] is None:
            raise BaseException(f'No input function for type \'{param_type}\'.')
        param_default = param['default']
        param['value'] = param['input']['cast'](param_default)
    
    SHOW_CURSOR = '\033[?25h'
    HIDE_CURSOR = '\033[?25l'
    CLEAR_LINE = '\033[K'
    MOVE_UP = '\033[F'
    prt_hieght = 0
    par_index = 0
    def _printer(user_input: str):
        nonlocal prt_hieght
        to_print = HIDE_CURSOR
        to_print += (CLEAR_LINE+MOVE_UP) * prt_hieght; prt_hieght = 0
        to_print += f"{prompt}[{func_name}{func_sig}]\n"; prt_hieght += 1
        for i, param in enumerate(func_params):
            txt_color = '\033[92m' if i == par_index else '\033[0m'  # Green for current param, reset for others
            to_print += f"{txt_color}- {param['param']}: {param['type']} = {param['value']}\n"; prt_hieght += 1
        txt_color = '\033[92m' if par_index == len(func_params) else '\033[0m'
        to_print += f"{txt_color}- Run\033[0m\n"; prt_hieght += 1
        print(to_print, end='', flush=True)

    def _special_actions(char_code: str):
        nonlocal par_index

        if char_code == b'\xc3\xa0H': # Up arrow
            if par_index > 0: par_index -= 1
        elif char_code == b'\xc3\xa0P': # Down arrow
            if par_index < len(func_params): par_index += 1

    def run_func():
        nonlocal func_params
        v = func(
            *[func_params[i]['value'] for i in range(len(func_params)) if func_params[i]['args_or_kwargs'] == 0],
            **{func_params[i]['param']: func_params[i]['value'] for i in range(len(func_params)) if func_params[i]['args_or_kwargs'] == 1}
            )
        print(CLEAR_LINE+prompt+str(v), end='', flush=True)
        return v

    def _selector(input_string: str):
        nonlocal prt_hieght
        if par_index == len(func_params): # Run
            print((CLEAR_LINE+MOVE_UP)*(prt_hieght)+SHOW_CURSOR, end='', flush=True)
            return True, run_func()
        param = func_params[par_index]
        print(f'\n{param["param"]}: {SHOW_CURSOR}', end='', flush=True); prt_hieght += 1
        param['value'] = param['input']['cast'](param['input']['input']()); prt_hieght += 1
        return False, ''
        
    if prompt.count('\n') > 0:
        prompt_lines = prompt.split('\n')
        static_prompt = '\n'.join(prompt_lines[:-1]) # Remove the last line of the prompt
        prompt = prompt_lines[-1] # Get the last line of the prompt
        print(static_prompt, flush=True)
    return input_plus(printer=_printer, special_actions=_special_actions, selector=_selector)