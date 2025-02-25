# Call function directly in cmd line

### Features
1. Allow user call functions directly in command line.
2. Generate help tips automatically.
3. Add default called functions if not function was specific.

### Notice
1. It's better to add argument type for each autocall functions.
2. Function with @optfunc_default has @optfunc implicitly.
3. Not support two type of variadic arguments.

### Code example1 -- calculator
``` python
from optfunc2 import cmdline, cmdline_default, cmdline_start

@cmdline_default
def add(a: float, b: float):
    """add two numbers

    Args:
        a (float): The First number
        b (float): The Second number
    """
    print(f"{a} + {b} = {a + b}")

@cmdline
def multiply(x: int|float, y: int = 5):
    """multiply two numbers. The second number is optional.

    Args:
        x (int): The First number
        y (int, optional): The Second number. Defaults to 5.
    """
    print(f"{x} × {y} = {x * y}")

@cmdline
def stats(numbers: list):
    """statistics of numbers in list

    Args:
        numbers (list): Target List.
    """ 
    print(f"sum: {sum(numbers)}")
    print(f"average: {sum(numbers)/len(numbers):.2f}")

if __name__ == "__main__":
    cmdline_start(header_doc="✨ calc CLI", has_abbrev=True)
```

### Generate help tips automatically
``` bash
~/optfunc2$ python src/example_calc.py help
Usage: src/example_calc.py [command] [<args>|--help]

✨ calc CLI

commands:
    add          [default] add two numbers
    multiply     multiply two numbers. The second number is optional.
    stats        statistics of numbers in list

~/optfunc2$ python src/example_calc.py add -h
Usage: src/example_calc.py add [OPTIONS]

add two numbers


Arguments:
+-----+--------+-------+---------+-------------------+
| Opt | Abbrev |  Type | Default |        Desc       |
+-----+--------+-------+---------+-------------------+
| --a |   -a   | float |         |  The First number |
| --b |   -b   | float |         | The Second number |
+-----+--------+-------+---------+-------------------+


~/optfunc2$ python src/example_calc.py stats -h
Usage: src/example_calc.py stats [OPTIONS]

statistics of numbers in list


Arguments:
+-----------+--------+------+---------+--------------+
|    Opt    | Abbrev | Type | Default |     Desc     |
+-----------+--------+------+---------+--------------+
| --numbers |   -n   | list |         | Target List. |
+-----------+--------+------+---------+--------------+
```

### Usage
``` bash
~/optfunc2$ python src/example_calc.py add -a 2.3 -b 3
2.3 + 3.0 = 5.3
~/optfunc2$ python src/example_calc.py -a 2.3 -b 3
2.3 + 3.0 = 5.3
~/optfunc2$ python src/example_calc.py multiply -x 3
3 × 5 = 15
~/optfunc2$ python src/example_calc.py multiply -x 2.3
2.3 × 5 = 11.5
~/optfunc2$ python src/example_calc.py stats --numbers '[1, 2, 3, 4, 5]'
sum: 15
average: 3.00
```

### Code example2 -- list files
``` python
from optfunc2 import cmdline, cmdline_default, cmdline_start
import os

@cmdline_default
def list_files(directory: str = ".", show_size: bool = False):
    """List files in a directory.

    Args:
        directory (str, optional): Target directory. Defaults to ".".
        show_size (bool, optional): Whether to show size of file. Defaults to False.
    """
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if show_size and os.path.isfile(path):
            print(f"{f} ({os.path.getsize(path)} bytes)")
        else:
            print(f)

if __name__ == "__main__":
    cmdline_start(header_doc="📁 file manager", has_abbrev=True)
```

### Usage
``` bash
$ python src/example_file_operator.py -h
Usage: src/example_file_operator.py [command] [<args>|--help]

📁 file manager

commands:
    list_files     [default] List files in a directory.

$ python src/example_file_operator.py list_files -h
Usage: src/example_file_operator.py list_files [OPTIONS]

List files in a directory.


Arguments:
+-------------+--------+------+---------+--------------------------------------------------+
|     Opt     | Abbrev | Type | Default |                       Desc                       |
+-------------+--------+------+---------+--------------------------------------------------+
| --directory |   -d   | str  |   '.'   |        Target directory. Defaults to ".".        |
| --show_size |   -s   | bool |  False  | Whether to show size of file. Defaults to False. |
+-------------+--------+------+---------+--------------------------------------------------+
$ python src/example_file_operator.py
LICENSE.txt
.gitignore
pyproject.toml
$ python src/example_file_operator.py -s
LICENSE.txt (1081 bytes)
.gitignore (132 bytes)
pyproject.toml (719 bytes)
```