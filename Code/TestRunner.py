'''
About  : Run suite of tests against all modules. Calls the do_test() function of
         all in-scope modules. Those functions return True if local test passed,
         else False.
Version: 1 (21-Mar-2023)
Author : Kevin Morley
'''

# ------------------------------------------------------------------------------

import logging
import const, config, crosscheck, georegion, iRecordController, iRecordParser, \
        utils

# ------------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO,
                format='%(module)s-%(funcName)s-%(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Run tests.

def run_tests(tests):
    '''
    Params: tests (list of functions) - list of test functions to be called
    Return: (bool) - True if all tests passed, else False
    '''
    log.info('='*60)
    log.info('Beginning tests')
    pass_count = 0
    for test in tests:
        if test():
            pass_count += 1

    log.info('-'*60)
    log.info('Finished tests')
    if pass_count == len(tests):
        log.info('Successful. All tests passed.')
        rv = True
    else:
        log.warning(f'Unsuccessful. \
                    Number of tests failed: {len(tests)-pass_count}')
        rv = False

    return rv

# ------------------------------------------------------------------------------
# Define and call list of test functions.

def main():
    '''
    Params: N/A
    Return: N/A
    '''
    tests = []
    tests.append(const.do_test)
    tests.append(config.do_test)
    tests.append(crosscheck.do_test)
    tests.append(georegion.do_test)
    tests.append(iRecordController.do_test)
    tests.append(iRecordParser.do_test)
    tests.append(utils.do_test)
    run_tests(tests)

# ------------------------------------------------------------------------------

main()

# ------------------------------------------------------------------------------
       
'''
End
'''