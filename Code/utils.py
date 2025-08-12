'''
About  : Utility classes and functions.
'''

# ------------------------------------------------------------------------------

import logging
import re
import shutil
import time
import pandas as pd
from datetime import datetime
from pathlib import Path
from word2number import w2n

import const

# ------------------------------------------------------------------------------

log: logging.Logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

def alpha_count(txt: str) -> int:
    '''Returns number of alpha characters in a given string.
    Args: 
        txt (string) - text to count
    Returns: 
        (int) number of alpha characters
    '''
    rv = len([c for c in txt if c.isalpha()])
    return rv

# ------------------------------------------------------------------------------

def append_comment(comment: str, txt: str, sep: str='; ') -> str:
    '''Append text to a comment and return concatenated string (e.g. 'comment; txt').
    Args: 
        comment (string)  - current comment
        txt (string) - text to be added
        sep (string) - separator text
    Returns: 
        (string) - concatenated text
    '''
    return comment + sep + txt if len(comment) > 0 else txt

# ------------------------------------------------------------------------------

def append_note(note: str, key: str, value: str, sep: str=' ') -> str:
    '''Append text to a note and return concatenated string (e.g. '[key: "value"]').
    Args: 
        note (string)  - current note
        key (string) - key to be added
        value (string) - value to be added
        sep (string) - separator text
    Returns: 
        (string) - concatenated text
    '''
    n = f'[{key}: "{value}"]'
    return note + sep + n if len(note) > 0 else n

# ------------------------------------------------------------------------------

def append_filename(fn: str, txt: str) -> str:
    '''Append text to a filename ahead of the extension (e.g. <fn><txt>.csv).
    Args: 
        fn (string)  - filename
        txt (string) - text to be added
    Returns:
        (string) - new filename
    '''
    i = fn.rfind('.')
    if i < 0:
        # No file extension so just add to end of string
        rv = fn + txt
    else:
        rv = fn[:i] + txt + fn[i:]

    return rv

# ------------------------------------------------------------------------------

def dict_add(to_dict: dict, from_dict: dict) -> None:
    '''Add one dictionary to another, summing values {text, int}.
    Args: 
        to_dict (dict: string, int) - target to add from from_dict
        from_dict (dict: string, int) - source to add to to_dict
    Returns:
        N/A
    '''
    for key, value in from_dict.items():
        if key not in to_dict:
            to_dict[key] = value
        else:
            to_dict[key] += value

# ------------------------------------------------------------------------------

def is_order_insect(order: str) -> bool:
    '''Returns True if a given order is a member of the Insecta class.
    Args: 
        order (string) - text to search
    Returns: 
        (bool) - True if Insecta, else False
    '''
    return order.lower() in const.ORDERS_INSECTA

# ------------------------------------------------------------------------------

def make_file_backup(file_path: str) -> None:
    '''Make a backup of a file.
    Args: 
        file_path (string) - path to file to 
    Returns: 
        N/A
    '''
    src = Path(file_path)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_folder = src.parent / 'Backup'
    backup_folder.mkdir(exist_ok=True)
    dst = backup_folder / f'{src.stem}_{timestamp}{src.suffix}'
    shutil.copy2(src, dst)

# ------------------------------------------------------------------------------

def read_csv_robust(file_path: str) -> pd.DataFrame:
    '''Robustly read a CSV file, trying multiple encodings and delimiters.
    Args: 
        file_path (string) - path to CSV file to read
    Returns: 
        (DataFrame) - Pandas data frame containing CSV file contents
    '''
    # Try multiple encodings and delimiters
    encodings = ['utf-8-sig', 'utf-8', 'ISO-8859-1']
    delimiters = [',', ';']

    for enc in encodings:
        for delim in delimiters:
            try:
                df = pd.read_csv(file_path, encoding=enc, delimiter=delim)
                return df
            except UnicodeDecodeError:
                continue
            except pd.errors.ParserError:
                continue
    raise ValueError(f'Could not read CSV file: {file_path}')

# ------------------------------------------------------------------------------

def strip_string(txt: str) -> str:
    '''Returns string having removed non-letter chars and multiple spaces..
    Args: 
        txt (string) - text to strip
    Returns: 
        (string) - stripped text
    '''
    txt_s = re.sub(r'[^a-zA-Z ]', ' ', txt)
    txt_s = re.sub(r'\s+', ' ', txt_s)
    return txt_s.strip().lower()

# ------------------------------------------------------------------------------

def word_to_num(txt: str) -> int|None:
    '''Convert text representation of number to numeric value, else None.
    Args: 
        txt (string) - text to convert
    Returns: 
        (int|None) - converted value
    '''
    try:
        rv = int(w2n.word_to_num(txt))
    except ValueError:
        rv = None

    return rv

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------

class ElapsedTime:
    '''Class which tracks and logs elapsed time.'''
    # --------------------------------------------------------------------------

    def __init__(self) -> None:
        '''Constructor.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        self.start = None
        self.reset()

    # --------------------------------------------------------------------------

    def log_elapsed_time(self):
        '''Write elapsed time to log.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        if self.start is None:
            log.error('Timer not started')
            return
        secs = time.perf_counter() - self.start
        log.info('Elapsed time: %s mins /  %s seconds',
                 f'{(secs/60):,.1f}', f'{int(secs):,}')

    # --------------------------------------------------------------------------

    def reset(self):
        '''Reset timer.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        log.info('Timer start')
        self.start = time.perf_counter()

# ------------------------------------------------------------------------------

'''
End
'''
