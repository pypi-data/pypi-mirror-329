import inspect
import prettytable
import docstring_parser
import sys
import ast
import types
from typing import Callable, Any, List

# functions taged by @cmdline
registered_funcs: List[Callable[..., Any]] = []
registered_func_default: Callable[..., Any] = None

# Main eval function in this module must be called only once.
_called_func = None

colors = {
    "red": 91,
    "blue": 94,
    "green": 92,
    "magenta": 95,
    "yellow": 93,
    "black": 90,
    "cyan": 96,
}

def color_begin(color):
    print('\033[{}m'.format(colors[color]), end='')
    
def color_end():
    print('\033[0m', end='')

def decode_func_args(func: callable):
    """
    (type, name, abbreviation, annotation, default, doc)
    """
    
    doc = func.__doc__
    docstring = docstring_parser.parse(doc)
    
    args_list = []
    abbrev_list = []
    
    # -h has been occupied by help command.
    abbrev_list.append('h')
    
    for name, param in inspect.signature(func).parameters.items():
        abbrev = name[0]

        desc = inspect.Signature.empty
        for param_docstring in docstring.params:
            if name == param_docstring.arg_name:
                desc = param_docstring.description
                break

        if abbrev not in abbrev_list:
            abbrev_list.append(abbrev)
        else:
            abbrev = inspect.Signature.empty
        
        args_list.append((param.kind, name, abbrev, param.annotation, param.default, desc))
    
    
    return args_list

def get_and_check_opt(args_list: list, opt_name):
    opt_name = opt_name
    opt_name_full = ''
    opt_name_abbrev = ''
    if opt_name.startswith('--'):
        opt_name_full = opt_name[2:]
    elif opt_name.startswith('-'):
        opt_name_abbrev = opt_name[1:]
        if len(opt_name_abbrev) != 1:
            raise ValueError(f'{opt_name} should be a single character abbreviation or full name beginning with --.')
    else:
        raise ValueError(f'{opt_name} is not a valid option name.')
    
    for idx, (_, name, abbrev, _, _, _) in enumerate(args_list):
        if name == opt_name_full or abbrev == opt_name_abbrev:
            return args_list.pop(idx)
        
    raise ValueError(f'{opt_name} not found.')

def decode_opts(arg_pairs, func: callable):
    """
    (type, name, annotation, value)
    """
    arg_list = decode_func_args(func)
    opt_list = []

    for (opt, val) in arg_pairs:
        typ, name, _, anno, _, _ = get_and_check_opt(arg_list, opt)
        # special case for assuming bool argument
        if type(val) == bool and anno != bool:
            raise ValueError(f'--{name} need more arguments.')
        
        try:
            if anno not in [dict, list, inspect.Signature.empty] and type(anno) != types.UnionType:
                value = anno(val)
            else:
                try: 
                    value = ast.literal_eval(val)
                except Exception:
                    value = str(val)

                anno_new = type(value)

                if anno != inspect.Signature.empty:
                    if type(anno) == types.UnionType:
                        type_list = [i.strip() for i in str(anno).split('|')]
                        if anno_new.__name__ not in type_list:
                            raise Exception(f'Type of {opt} should be one of {repr(type_list)}.')
                         
                    elif anno_new != anno:
                        print(f'{anno_new = } {anno = }')
                        raise ValueError(f'Value type of {opt} should be {anno.__name__}.')
                
                anno = anno_new

            opt_list.append((typ, name, anno, value))
            
        except ValueError:
            raise ValueError(f'Value type of {opt} should be {anno.__name__}.')
    
    for (typ, name, _, anno, default, _) in arg_list:
        if default == inspect.Signature.empty:
            raise ValueError(f'--{name} is required.')
        
        opt_list.append((typ, name, anno, default))
        
    return opt_list

def hibit_variadic(func: callable):
    arg_list = decode_func_args(func)
    for (typ, _, _, _, _, _) in arg_list:
        if typ == inspect.Parameter.VAR_POSITIONAL or typ == inspect.Parameter.VAR_KEYWORD:
            color_begin('red')
            print(f'[Autocall Error]: Function {func.__name__} annotated by @cmdline has variadic arguments.')
            color_end()
            exit(1)

def cmdline_default(func: Callable[..., Any]) -> Callable[..., Any]:
    global registered_func_default
    global registered_funcs
    
    parameters = inspect.getfullargspec(func)
    
    if registered_func_default:
        color_begin('yellow')
        print(f'[Autocall Warning]: @cmdline_default can only be used once or the last one will be used.')
        color_end()

    registered_func_default = func
    
    hibit_variadic(func)

    if func not in registered_funcs:
        registered_funcs.append(func)
    
    # globals()[funcname] = func
    return func

def cmdline(func: Callable[..., Any]) -> Callable[..., Any]:
    global registered_funcs
    if func not in registered_funcs:
        registered_funcs.append(func)

    hibit_variadic(func)
    return func

    
def cmd_help(func: Callable[..., Any], has_abbrev: bool = True):
    args_list = decode_func_args(func)
    
    func_desc = docstring_parser.parse(func.__doc__).description
    
    empty_tag = ''
    
    color_begin('blue')
    print(f'Usage: {sys.argv[0]} {func.__name__} ', end='')
    print('[OPTIONS]')
    color_end()
    print()
    
    if func_desc != None:
        print(func_desc)
    else:
        print('Help Tips Provided by Autocall.')

    print()
       
    if len(args_list) == 0:
        return
    
    print('Arguments:')

    table = prettytable.PrettyTable()
    table.field_names = ['Opt', 'Abbrev', 'Type', 'Default', 'Desc']

    for (type, name, abbrev, anno, default, desc) in args_list:
        # abbrev, anno, default, desc all may be empty
        name = '--' + name

        if abbrev == inspect.Signature.empty:
            abbrev = empty_tag
        else:
            abbrev = '-' + abbrev
        
        if anno == inspect.Signature.empty:
            anno = 'any'
        else:
            anno = anno.__name__
        
        if default == inspect.Signature.empty:
            default = empty_tag
        else:
            default = repr(default)
        
        if desc == inspect.Signature.empty:
            desc = empty_tag
            
        table.add_row([name, abbrev, anno, default, desc])
    
    if not has_abbrev:
        table.del_column('Abbrev')

    print(table)

def help(header_doc):
        """
        Give the argument \"verbose\" instead of \"notverbose\" to print detail information.
        """
        global registered_funcs

        color_begin('blue')
        print(f'Usage: {sys.argv[0]} ', end='')
        # print('[--help] ', end='')
        color_begin('green')
        print('[command] [<args>|--help]')
        color_end()
        print()
        
        print(header_doc)
        print()
        
        print('commands:')

        max_name_len = max([len(f.__name__) for f in registered_funcs]) + 5
        
        for f in registered_funcs:
            doc = f.__doc__
            color_begin('green')
            print(f'    {f.__name__:<{max_name_len}s}', end='')
            color_end()
            if f == registered_func_default:
                color_begin('yellow')
                print('[default] ', end='')
                color_end()
            if doc:
                doc_list = [d.strip() for d in doc.split('\n') if d.strip()]
                doc = doc_list[0]
                print(doc)
            else:
                print()
        
        print()

def match_and_check(name):
        """
        Match the name with the function name.
        """
        global registered_funcs
        # [::-1] ensure the order of functions with same name.
        for f in registered_funcs[::-1]:
            if f.__name__ == name:
                return f
        
        return None

def pair_argv(argv, has_abbrev = True):
    """ Support these styles:
    --arg val
    --arg=val
    --arg 
    -a val
    -aval
    -a
    """
    if len(argv) == 0:
        return []
    
    idx = 0
    arg_pairs = []
    while idx < len(argv):
        arg = argv[idx]
        if arg.startswith('--'):
            if '=' in arg:
                arg, val = arg.split('=')
                arg_pairs.append((arg, val))
            else:
                if len(argv) == idx + 1:
                    arg_pairs.append((arg, True))
                else:
                    if argv[idx+1].startswith('-'):
                        arg_pairs.append((arg, True))
                    else:
                        arg_pairs.append((arg, argv[idx+1]))
                        idx += 1 
                
        elif arg.startswith('-'):
            if not has_abbrev:
                raise ValueError(f'Unknown argument {arg}. Abbreviations are not supported.')
            
            if len(arg) != 2:
                arg_pairs.append((arg[0:2], arg[2:]))
            else:
                # bool type can be used in single character.
                if len(argv) == idx + 1: # Cmdline ended with a abbreviation, we assume it is a bool type argument.
                    arg_pairs.append((arg, True))
                else: # Next argument is belong to the next pair. We assume it is a bool type argument.
                    if argv[idx+1].startswith('-'):
                        arg_pairs.append((arg, True))
                    else: # Normal.
                        arg_pairs.append((arg, argv[idx+1]))
                        idx += 1
                
        idx += 1
    
    return arg_pairs

def called_directly():
    """Check if the function is called by optfunc2 directly.

    Returns:
        bool: True means called by optfunc2 directly.
    """
    global _called_func
    return _called_func.__name__ == inspect.currentframe().f_back.f_code.co_name



# def parse_run(argv = sys.argv[1:]):
def cmdline_start(globals = None, locals = None, *, argv = sys.argv, header_doc: str = 'Help Tips Provided by Autocall.', has_abbrev = False):
    """Begin to handle argv and execute the corresponding function.

    Args:
        globals (dict): Used to be the execution environment.
        locals (dict, optional): Used to be the execution environment.
        argv (list, optional): Advanced usage. Defaults to sys.argv.
        header_doc (str, optional): Will be printed as the header of help information.
        has_abbrev (bool, optional): Whether to support abbreviations. Defaults to False. Be careful when using this option. The abbreviation may be dynamically changed.
    """
    global _called_func
    
    # ensure only one call
    if _called_func:
        #return
        pass # This function has to be called in main program explicitly.
    
    if not globals:
        globals = inspect.currentframe().f_back.f_globals
    
    if len(argv) == 1:
        if not registered_func_default:
            return
        argv.append(registered_func_default.__name__)
    
    if argv[1] == 'help' or argv[1] == '--help' or argv[1] == '-h':
        help(header_doc)
        return
    
    if not registered_func_default and argv[1][0] == '-':
        return
    
    if argv[1][0] == '-':
        # use the default function
        argv.insert(1, registered_func_default.__name__)
    
    func = match_and_check(argv[1])
    
    if not func:
        color_begin('red')
        print(f'[Autocall Warning]: Unknown command \"{argv[1]}\". Use \"--help\" or \"help\" to get help.')
        color_end()
        return
    
    # Not exception will be raised when no more arguments are given.
    argv = argv[2:]
    if '-h' in argv or '--help' in argv:
        cmd_help(func, has_abbrev)
        return
    
    _called_func = func
    
    # parse argv
    arg_pairs = pair_argv(argv, has_abbrev)
    
    # get opt_list from arg_pairs
    opt_list = decode_opts(arg_pairs, func)

    final_args = []
    
    for (typ, name, anno, value) in opt_list:
        if typ != inspect.Parameter.POSITIONAL_ONLY:
            final_args.append(f'{name}={repr(value)}')
        else:
            final_args.append(repr(value))
    
    func_call_str = f'{func.__name__}('    
    func_call_str += ', '.join(final_args)
    func_call_str += ')'
    
    # Return the called function's return value.
    return eval(func_call_str, globals, locals)
