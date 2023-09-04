import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')  # it checks if its a num or a dot

def is_num_or_dot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))

def is_empty(string: str):
    return len(string) == 0

def is_valid_number(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False   
    return valid    
    
def conver_to_number(string: str):
    number = float(string)

    if number.is_integer():
        number = int(number)

    return number