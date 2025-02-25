import json
from os import makedirs, path, system
from sys import platform
from collections.abc import Container

def isInt(input: str) -> bool:
    """
    Check if input(of type str) an integer or not. Return True if yes, else return False.
    """
    if isinstance(input, int):
        raise ValueError("Already an int.")
    if not isinstance(input, str):
        raise TypeError(f"Parameter 'input' expect str, got {type(input).__name__} instead.")
    
    try:
        int(input)
        return True
    except ValueError:
        return False

def clear():
    """
    Clear the terminal, that's all.
    """
    if platform == "win32":
        system("cls")
    else:
        system("clear")

def num_to_roman(input: int) -> str:
    """
    Convert input (of type int), into Roman numerals.
    """
    if not isinstance(input, int):
        raise TypeError(f"Parameter 'input' expects type int, got {type(input).__name__} instead.")

    roman: str = ""
    number_map: dict[str, int] = {
        1000: "M", 900: "CM", 500: "D", 400: "CD",
        100: "C", 90: "XC", 50: "L", 40: "XL", 
        10: "X", 9: "IX", 5: "V", 4: "IV", 1: "I"
    }

    for value in number_map:
        while input >= value:
            roman += number_map[value]
            input -= value

    return roman

def menu(config: Container, start: int = 1, trailing_dot: bool = True, roman_numeral_mode: bool = False) -> str:
    """
    Generate the options in a menu.

    :type config: Container
    :param config:
    + Accept any container type
    + For any container but dict, the items in the said container will be the option for the menu.
    + For dict, the keys in the dict will the options and the value.
    + Do note that whitespace in str will also count into the option.
    :type start: int
    :param start: Accept int. Specify where to start generate a menu. Default is 1.
    :type trailing_dot: bool
    :param trailing_dot: Accept bool. Decide whether option should end with a dot. Default is True.
    :type roman_numeral_mode: bool
    :param roman_numeral_mode: Decide whether or not to use Roman numerals instead of integer. Default is False.
    """
    if not isinstance(config, Container):
        raise TypeError(f"Parameter 'config' expect container type (e.g list, str, dict,...), got {type(config).__name__} instead.")
    if not isinstance(start, int):
        raise TypeError(f"Parameter 'start' expect int, got {type(start).__name__} instead.")
    if not isinstance(trailing_dot, bool):
        raise TypeError(f"Parameter 'trailing_dot' expect bool, got {type(trailing_dot).__name__} instead.")
    if not isinstance(roman_numeral_mode, bool):
        raise TypeError(f"Parameter 'roman_numeral_mode' expect bool, got {type(trailing_dot).__name__} instead.")
    if isinstance(config, dict):
        config = [x for x in config.keys()]

    output = ""
    for i in range(start, len(config) + start):
        if not roman_numeral_mode:
            if trailing_dot:
                output += f"{i}. {config[i - start]}."
            else:
                output += f"{i}. {config[i - start]}"
        else:
            if trailing_dot:
                output += f"{num_to_roman(i)}. {config[i - start]}."
            else:
                output += f"{num_to_roman(i)}. {config[i - start]}"
        
        if i - start + 1 < len(config):
            output += "\n"
    return output

def write_config(def_config: dict, config: dict, config_folder: str, config_file_name: str):
    """
    Write config to its file, automatically generate new config file (from def_config) if config doesn't exist or corrupted.

    :type def_config: dict
    :param def_config: The default config.
    :type config: dict
    :param def_config: Config that.
    :type config_folder: str
    :param config_folder: The path to the folder contains the config file.
    :type config_file_name: str
    :param config_file_name: The name of the config file.
    """
    if not isinstance(config, dict):
        raise TypeError(f"Parameter 'config' expect type dict, got {type(config).__name__} instead.")
    if not isinstance(def_config, dict):
        raise TypeError(f"Parameter 'def_config' expect type dict, got {type(def_config).__name__} instead.")
    if not isinstance(config_folder, str):
        raise TypeError(f"Parameter 'config_path' expect type str, got {type(config_folder).__name__} instead.")
    if not isinstance(config_file_name, str):
        raise TypeError(f"Parameter 'config_file_name' expect type str, got {type(config_file_name).__name__} instead.")

    config_path = fr"{config_folder}\{config_file_name}"
    try:
        with open(config_path, "w") as temp:
            json.dump(config, temp, ensure_ascii = False, indent = 4)
    except FileNotFoundError:
        config_manager(def_config, config_folder, config_file_name)
        write_config(config_path, config, config_folder, config_file_name)

def config_manager(def_config: dict, config_folder: str, config_file_name: str) -> None:
    """
    Check the config file to see if it's valid or not. Create new config folder if not exist, write new config file if config doesn't exist or corrupted.

    :type def_config: dict
    :param def_config: The default config.
    :type config_folder: str
    :param config_folder: The path to the folder contains the config file.
    :type config_file_name: str
    :param config_file_name: The name of the config file.
    """
    if not isinstance(def_config, dict):
        raise TypeError(f"Parameter 'def_config' expect type dict, got {type(def_config).__name__} instead.")
    if not isinstance(config_folder, str):
        raise TypeError(f"Parameter 'config_path' expect type str, got {type(config_folder).__name__} instead.")
    if not isinstance(config_file_name, str):
        raise TypeError(f"Parameter 'config_file_name' expect type str, got {type(config_file_name).__name__} instead.")

    makedirs(config_folder, exist_ok=True)
    config_path = fr"{config_folder}\{config_file_name}"

    if not path.exists(config_path):
        with open(config_path, "w") as temp:
            json.dump(def_config, temp, ensure_ascii=False, indent=4)
        return
    
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
    except json.JSONDecodeError:
        with open(config_path, "w") as file:
            json.dump(def_config, file, ensure_ascii=False, indent=4)
        return
    
    if def_config.keys() != config.keys():
        with open(config_path, "w") as file:
            json.dump(def_config, file, ensure_ascii=False, indent=4)
        return
    
    for key in def_config.keys():
        if isinstance(config.get(key), dict):
            config[key] = config.get(key, {})
        elif type(config.get(key)) != type(def_config[key]):
            with open(config_path, "w") as file:
                json.dump(def_config, file, ensure_ascii=False, indent=4)
            return