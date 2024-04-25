'''
About  : Utility functions.
Author : Kevin Morley
Version: 1 (21-Mar-2023)
'''

# ------------------------------------------------------------------------------

import const                    # KPM
import logging
import re
import time

from word2number import w2n

# ------------------------------------------------------------------------------

log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Returns number of alpha characters in a given string.

def alpha_count(txt):
    '''
    Params: txt (string) - text to count
    Return: (int) number of alpha characters
    '''
    rv = len([c for c in txt if c.isalpha()])
    return rv

# ------------------------------------------------------------------------------
# Append text to a comment and return concatenated string (e.g. 'comment; txt')

def append_comment(comment, txt, sep='; '):
    '''
    Params: comment (string)  - current comment
            txt (string) - text to be added
            sep (string) - separator text
    Return: (string) - concatenated text
    '''
    return comment + sep + txt if len(comment) > 0 else txt

# ------------------------------------------------------------------------------
# Append text to a note and return concatenated string (e.g. '[key: "value"]')

def append_note(note, key, value, sep=' '):
    '''
    Params: note (string)  - current note
            key (string) - key to be added
            value (string) - value to be added
            sep (string) - separator text
    Return: (string) - concatenated text
    '''
    n = f'[{key}: "{value}"]'
    return note + sep + n if len(note) > 0 else n

# ------------------------------------------------------------------------------
# Append text to a filename ahead of the extension (e.g. <fn><txt>.csv)

def append_filename(fn, txt):
    '''
    Params: fn (string)  - filename
            txt (string) - text to be added
    Return: (string) - new filename
    '''
    i = fn.rfind('.')
    if i < 0:
        # No file extension so just add to end of string
        rv = fn + txt
    else:
        rv = fn[:i] + txt + fn[i:]

    return rv
    
# ------------------------------------------------------------------------------
# Add one dictionary to another, summing values {text, int}.

def dict_add(to_dict, from_dict):
    '''
    Params: to_dict (dict: string, int) - target to add from from_dict
            from_dict (dict: string, int) - source to add to to_dict
    Return: N/A
    '''
    for key, value in from_dict.items():
        if key not in to_dict:
            to_dict[key] = value
        else:
            to_dict[key] += value

# ------------------------------------------------------------------------------
# Returns True if a given order is a member of the Insecta class

def is_order_insect(order):
    '''
    Params: order (string) - text to search
    Return: (bool) - True if Insecta, else False
    '''    
    return order.lower() in const.INSECTA_ORDERS

# ------------------------------------------------------------------------------
# Returns string having removed non-letter chars and multiple spaces.

def strip_string(txt):
    '''
    Params: txt (string) - text to strip
    Return: (string) - stripped text
    '''    
    txt_s = re.sub(r'[^a-zA-Z ]', ' ', txt)
    txt_s = re.sub(r'\s+', ' ', txt_s)
    return txt_s.strip().lower()

# ------------------------------------------------------------------------------
# Convert text representation of number to numeric value, else None

def word_to_num(txt):
    '''
    Params: txt (string) - text to convert
    Return: (int) - converted value
    '''    
    try:
        rv = w2n.word_to_num(txt)
    except ValueError:
        rv = None

    return rv

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------
# Class which tracks and logs elapsed time

class ElapsedTime:

    # --------------------------------------------------------------------------
    # Constructor.

    def __init__(self):
        '''
        Params: N/A
        Return: N/A
        '''
        self.start = None
        self.reset()
        
    # --------------------------------------------------------------------------
    # Write elapsed time to log.

    def log_elapsed_time(self):
        '''
        Params: N/A
        Return: N/A
        '''
        secs = time.perf_counter() - self.start
        log.info(f'Elapsed time: {(secs/60):,.1f} mins /  {int(secs):,} seconds')
    
    # --------------------------------------------------------------------------
    # Reset timer.

    def reset(self):
        '''
        Params: folder (string) - path to folder containing files to parse
        Return: (list of strings) - filenames to be parsed
        '''
        log.info('Timer start')
        self.start = time.perf_counter()


# ------------------------------------------------------------------------------
# Test
# ------------------------------------------------------------------------------

def do_test():
    log.info('-'*50)
    log.info('Beginning test [utils.py]...')

    et = ElapsedTime()
    time.sleep(3.7)
    et.log_elapsed_time()
    rv = True
    log.info(f'Finished test. Test passed: {rv}')
    return rv

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s-%(module)s-%(funcName)s-%(levelname)s - %(message)s', 
        datefmt='%H:%M:%S')    
    do_test()

# ------------------------------------------------------------------------------
       
'''
End
'''