'''
About  : Main program file. See main() function.
Author : Kevin Morley
Version: 1 (21-Mar-2023)
'''

# ------------------------------------------------------------------------------

import getopt
import logging
import sys
import traceback

from iRecordController import iRecordController     # KPM

# ------------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, 
            format='[%(module)s]-[%(funcName)s]-[%(levelname)s] - %(message)s', 
            handlers= [
                logging.FileHandler('debug.log', mode='w'), 
                logging.StreamHandler()
            ])
log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
# Main program entry point. Instantiate controller object and call methods.

def main(argv):
    '''
    Params: N/A
    Return: N/A
    '''
 
    help = 'iRecordController.py -i <INI file path>'
    try:
        opts, args = getopt.getopt(argv,'hi:',['ini='])
    except getopt.GetoptError:
        print(f'Incorrect command line option: {argv}')
        print (f'Correct options are: "{help}"')
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
        rc = iRecordController(fn_config)
        rc.process()
    except Exception as ex:
        log.error(ex)
        traceback.print_exception(*sys.exc_info())
    

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv[1:])

# ------------------------------------------------------------------------------
       
'''
End
'''