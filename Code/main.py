'''
About  : Program entry point. See main() function.
'''

# ------------------------------------------------------------------------------

import argparse
import logging
import sys
import traceback

from controller import RecordController

# ------------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO,
            format='[%(module)s]-[%(funcName)s]-[%(levelname)s] - %(message)s',
            handlers= [
                logging.FileHandler('debug.log', mode='w'),
                logging.StreamHandler()
            ])
log: logging.Logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

def main() -> None:
    '''Main program entry point. Instantiate controller object and call methods.
    Args: 
        N/A
    Returns: 
        N/A
    '''
    parser = argparse.ArgumentParser(description='iRecord Parser')
    parser.add_argument('-i', '--ini', required=True, help='INI file path')
    args = parser.parse_args()
    fn_config = args.ini

    # Execute the processing
    log.info('='*50)
    try:
        rc = RecordController(fn_config)
        rc.process()
    except Exception as ex: # pylint: disable=broad-exception-caught
        log.error(ex)
        traceback.print_exception(*sys.exc_info())


# ------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

# ------------------------------------------------------------------------------

'''
End
'''
