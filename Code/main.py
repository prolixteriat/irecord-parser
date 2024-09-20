'''
About  : Program entry point. See main() function.
'''

# ------------------------------------------------------------------------------

import getopt
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
    helpstr = 'main.py -i <INI file path>'
    try:
        argv = sys.argv[1:]
        opts, _ = getopt.getopt(argv,'hi:',['ini='])
    except getopt.GetoptError:
        print(f'Incorrect command line option: {argv}')
        print(f'Correct options are: "{helpstr}"')
        sys.exit(2)

    # Process command line options
    fn_config = None
    for opt, arg in opts:
        if opt == '-h':
            print('help')
            sys.exit()
        elif opt in ('-i', '--ini'):
            fn_config = arg
        else:
            print(f'Unknown option: {opt}')
            sys.exit(2)

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
