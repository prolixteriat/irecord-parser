'''
About  : Implements the iRecordParser class which performs the data input, 
         parsing and output processes for a single iRecord data file.
Author : Kevin Morley
Verion : 1 (21-Mar-2023)
'''

# ------------------------------------------------------------------------------

import const                                # KPM
import csv
import logging
import os
import pandas as pd
import progress.spinner as spinner
import threading
import time
import utils                                # KPM

from crosscheck import Crosschecker         # KPM
from progress.bar import Bar
from rules import Rules                     # KPM

# ------------------------------------------------------------------------------

log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Class which orchestrates the data input, parsing and output processes.

class iRecordParser:

    # --------------------------------------------------------------------------
    # Constructor.

    def __init__(self, config):
        '''
        Params: config (ConfigMgr) - instance of class containing INI file
        Return: N/A
        '''
        self.config = config    # instance of ConfigMgr class
        self.crosscheck = Crosschecker(self.config)
        self.filename = None    # input filename
        self.records = []       # Records read from file
        self.processed = []     # Processed records
        self.skipped = []       # Records skipped
        self.swift = []         # Records to be exported in Swift format

    # --------------------------------------------------------------------------
    # Output results to multitab Excel workbook.

    def output_excel(self):
        '''
        Params: N/A
        Return: N/A 
        See: https://xlsxwriter.readthedocs.io/
        '''    
        # ----------------------------------------------------------------------
        # Add new sheet to workbook, populate and format as required.
        def add_sheet(writer, name, data, cols, format, freeze_col):
            '''
            Params: writer (pandas ExcelWriter) - writer object
                    name (string) - name of sheet
                    data (list of dicts) - data to be written to sheet
                    cols (list) - columns names in correct order
                    format (xlsxwriter format) - sheet formatting
                    freeze_col (int) - column at which to freeze scrolling
            Return: N/A 
            '''
            log.debug(f'Writing {name} tab')
            # Check whether we have any data to write
            if len(data) > 0:
                # Create a (dict of lists) dataframe from a (list of dicts)
                d = {key: [i[key] for i in data] for key in data[0]}
                df = pd.DataFrame(d) 
                # Reorder columns
                df = df[cols]
            else:
                # Create empty dataframe
                df = pd.DataFrame(columns=cols)
            df.to_excel(writer, sheet_name=name, index=False)
            # Apply formatting to the sheet
            sheet = writer.sheets[name]
            sheet.freeze_panes(1, freeze_col)
            for col_num, value in enumerate(df.columns.values):
                sheet.write(0, col_num, value, format)
        # ----------------------------------------------------------------------
        # Get filename
        fb = os.path.basename(self.filename)
        fb = os.path.splitext(fb)[0]
        fn = os.path.join(self.config.dir_data_out, fb + '.xlsx')
        log.info(f'Writing Excel file: {fn}')        
        # Prepare columns headers
        fields = const.I_COLUMNS.copy()
        fields.insert(0, const.I_IMPORTNOTE)
        fields.insert(0, const.I_IMPORTTYPE)
        with pd.ExcelWriter(fn, engine='xlsxwriter') as writer:
            # Create format for header row of each sheet - uses xlsxwriter
            workbook = writer.book
            format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'bg_color': '#F6F4F4'})
            
            format.set_border(1)
            format.set_border_color('silver')
            # Create sheets
            add_sheet(writer, 'Key', self.records, const.I_COLUMNS, format, 1)
            add_sheet(writer, 'Swift', self.swift, const.S_COLUMNS, format, 3)
            add_sheet(writer, 'Skipped', self.skipped, fields, format, 3)

    # --------------------------------------------------------------------------
    # Output results to files.

    def output_results(self):
        '''
        Params: N/A
        Return: N/A 
        '''    
        # ----------------------------------------------------------------------
        # Write a single CSV file
        def write_file(fn_txt, data, fields):
            fb = os.path.basename(self.filename)
            fn = os.path.join(self.config.dir_data_out, 
                              utils.append_filename(fb, fn_txt))
            log.info(f'Writing {fn_txt} file: {fn}')
            with open(fn, 'w', encoding='utf-8') as out_file:
                writer = csv.DictWriter(out_file, lineterminator='\r',
                                        quoting=csv.QUOTE_NONNUMERIC,
                                        fieldnames=fields)
                writer.writeheader()
                writer.writerows(data)   
        # ----------------------------------------------------------------------

        log.info('Writing results to CSV files')
        fields = const.I_COLUMNS.copy()
        fields.insert(0, const.I_IMPORTNOTE)
        fields.insert(0, const.I_IMPORTTYPE)
        write_file('_key', self.records, const.I_COLUMNS)
        write_file('_skip', self.skipped, fields)
        # fields.insert(2, const.I_IMPORTCOMMENT)
        # write_file('_wf', self.processed, fields)
        write_file('_swift', self.swift, const.S_COLUMNS)
        # Only produce Excel workbook if config flag set
        if self.config.excel == True:
            # Use threading to allow spinner animation
            thread = threading.Thread(target=self.output_excel)
            thread.start()
            with spinner.Spinner('Writing Excel file...') as spin:
                while thread.is_alive():
                    spin.next()
                    time.sleep(0.1)
            thread.join()            

    # --------------------------------------------------------------------------
    # Process each of the iRecord records.

    def process_records(self):
        '''
        Params: N/A
        Return: N/A 
        '''
        log.info('Processing records')
        with Bar('Processing records...', max=len(self.records)) as bar:
            for rec in self.records:
                bar.next()
                rules = Rules(rec, self.crosscheck)
                # Determine whether record should be skipped
                sn = rules.is_skip()
                if len(sn[0]) > 0:
                    # Skip record
                    skip = rec.copy()
                    skip[const.I_IMPORTTYPE] = sn[0]
                    skip[const.I_IMPORTNOTE] = sn[1]
                    self.skipped.append(skip)
                    '''
                    # TODO: Next 3 lines should be deleted following testing
                    s, p = rules.get_swift()
                    self.processed += p
                    self.swift += s
                    '''
                else:
                    # Map record to Swift
                    s, p = rules.get_swift()
                    self.processed += p
                    self.swift += s

        log.info(f'Number of iRecord records: {len(self.records)}')
        log.info(f'Number of skipped records: {len(self.skipped)}')
        log.info(f'Number of Swift records: {len(self.swift)}')
        self.crosscheck.georegion.plot(self.filename)
        i, o = self.crosscheck.georegion.count()
        log.info(f'Number of gridrefs outside region: {o}')
        self.output_results()

    # --------------------------------------------------------------------------
    # Read the contents of a given CSV file.

    def read_file(self, fn):
        '''
        Params: fn (string) - CSV filename
        Return: (bool) - True if successful, else False
        '''
        log.info(f'Reading file: {fn}')
        self.filename = fn
        rv = True
        self.crosscheck.georegion.reset()
        self.records.clear()
        with open(fn, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for ix, dict in enumerate(reader):
                dict[const.I_KEY] = ix
                self.records.append(dict)

        log.debug(f'Number of records read from file: {len(self.records)}')
        self.process_records()
        return rv


# ------------------------------------------------------------------------------
# Test
# ------------------------------------------------------------------------------
# Run module-specific tests.

def do_test():
    '''
    Params: N/A
    Return: (bool) Returns True if tests succesful, else False
    '''
    log.info('-'*50)
    log.info('Beginning test [iRecordParser.py]...')
    et = utils.ElapsedTime()
    config = ConfigMgr()
    fn = 'Data_In/iRecord Data 09-01-2020 - 31-01-2020_original.csv'
    rp = iRecordParser(config)
    rv = rp.read_file(fn)
    et.log_elapsed_time()  
    log.info(f'Finished test. Test passed: {rv}')
    return rv

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
            format='[%(module)s]-[%(funcName)s]-[%(levelname)s] - %(message)s')
    from config import ConfigMgr

    do_test()

# ------------------------------------------------------------------------------
       
'''
End
'''