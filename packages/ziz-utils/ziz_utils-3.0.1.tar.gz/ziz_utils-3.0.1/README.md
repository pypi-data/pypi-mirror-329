# Ziz's Utilities - Python Edition

A collection of Python function that I used in my projects.

## Contains
### Update 1.0.0
```python
isInt(input: str) #Check if input of type str is an integer or not.
clear() #Clear the terminal.
num_to_roman(input: int) #Convert input of type int into the equivalent in Roman numerals.
menu(config: Container, start: int = 1, trailing_dot: bool = True, roman_numeral_mode: bool = False) #A menu generator, consult the docstring of this function for more information. This is the pre-3.0.0 version
```

### Update 2.0.0
```python
config_manager(def_config: dict, config_folder: str, config_file_name: str) #Consult the docstring of this function.
write_config(config_path: str, config: dict, def_config: dict) #Consult the docstring of this function.
```
### Update 3.0.0
```python
menu(config: Container,
     option_prefix: str = "".strip(),
     option_suffix: str = "".strip(),
     start: int = 1,
     trailing_dot: bool = True,
     roman_numeral_mode: bool = False
) #A menu generator, consult the docstring of this function for more information. This is the 3.0.0 version
```
And more! (hopefully)

## Installation
<ol type="1">
    <li>
        Install Python 3.x from <a href="https://www.python.org/downloads/" target="_blank">here</a>. (Ignore if you already have Python 3.x installed)
    </li>
    <li>
    Open terminal, run:
    
```terminal
pip install ziz_utils
```
</li>
</ol>

## Usage
In a Python file:
```python
import ziz_utils
```
Or:
```python
from ziz_utils import <function_name> #With function_name as the, well, function name.
```

## Requirement(s)
1. Python 3.x

## License
This project is licensed under the GNU General Public License 3.0, check [LICENSE](LICENSE) for more details.
