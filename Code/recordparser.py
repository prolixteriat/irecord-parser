'''
About  : Implements the RecordParser class which performs the data input, 
         parsing and output processes for a single iRecord data file.
'''

# ------------------------------------------------------------------------------

import csv
import logging
import os
import threading
import time
from typing import Any

import pandas as pd
from progress import spinner
from progress.bar import Bar

import const
import utils
from configmgr import ConfigMgr
from crosscheck import Crosschecker
from rules import DupeDict, Records, Rules

# ------------------------------------------------------------------------------

log: logging.Logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

class RecordParser:
    '''Class which orchestrates the data input, parsing and output processes.'''

    # --------------------------------------------------------------------------

    def __init__(self, config: ConfigMgr) -> None:
        '''Constructor.
        Args: 
            config (ConfigMgr) - instance of class containing INI file
        Returns: 
            N/A
        '''
        self.config: ConfigMgr = config   # instance of ConfigMgr class
        self.crosscheck: Crosschecker = Crosschecker(self.config)
        self.filename: str = ''           # input filename
        self.key_processed: Records = []  # Previously processed records
        self.key_new: Records = []        # New records
        self.records: Records = []        # Records read from file
        self.skipped: Records = []        # Records skipped in Swift format
        self.swift: Records = []          # Records to be exported in Swift format

    # --------------------------------------------------------------------------

    def check_columns(self) -> bool:
        '''Check that the input file has the correct columns.
        Args: 
            N/A
        Returns:
            (bool) - True if all required columns are present, else False
        '''
        rv: bool = True
        extra = [col for col in self.records[0] if col not in const.I_COLUMNS]
        if len(extra) > 0:
            log.warning('Input file has unused columns: %s', extra)
            # Remove the unused keys from each dictionary
            for col in extra:
                for record in self.records:
                    record.pop(col, None)

        missing = [col for col in const.I_COLUMNS if col not in self.records[0]]
        if len(missing) > 0:
            log.error('Input file does not contain all required columns: %s', missing)
            rv = False

        return rv

    # --------------------------------------------------------------------------

    def output_excel(self):
        '''Output results to multitab Excel workbook.
        Args: 
            N/A
        Returns: 
            N/A 
        See: 
            https://xlsxwriter.readthedocs.io/
        '''
        # ----------------------------------------------------------------------
        #
        def add_sheet(writer: pd.ExcelWriter, name: str, data: Records,
                      cols: list[str], formatxls: Any, freeze_col: int) -> None:
            '''Add new sheet to workbook, populate and format as required.
            Args: 
                writer (pandas ExcelWriter) - writer object
                name (string) - name of sheet
                data (list of dicts) - data to be written to sheet
                cols (list) - columns names in correct order
                formatxls (xlsxwriter format) - sheet formatting
                freeze_col (int) - column at which to freeze scrolling
            Returns: 
                N/A 
            '''
            log.debug('Writing tab: %s', name)
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
            if len(cols) == 1:
                sheet.set_column(0, 0, 20)
            for col_num, value in enumerate(df.columns.values):
                sheet.write(0, col_num, value, formatxls)
        # ----------------------------------------------------------------------
        # Get filename
        fb = os.path.basename(self.filename)
        fb = os.path.splitext(fb)[0]
        fn = os.path.join(self.config.dir_data_out, fb + '.xlsx')
        log.info('Writing Excel file: %s', fn)
        with pd.ExcelWriter(fn, engine='xlsxwriter') as writer:
            # Create format for header row of each sheet - uses xlsxwriter
            workbook = writer.book
            formatxls = workbook.add_format({ # type: ignore
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'bg_color': '#F6F4F4'})

            formatxls.set_border(1)
            formatxls.set_border_color('silver')
            # Create sheets
            add_sheet(writer, 'Key', self.records, const.I_COLUMNS, formatxls, 1)
            add_sheet(writer, 'Swift', self.swift, const.S_COLUMNS, formatxls, 3)
            add_sheet(writer, 'Skipped', self.skipped, const.S_COLUMNS, formatxls, 3)
            add_sheet(writer, 'Processed', self.key_processed, [const.I_RECORDKEY], formatxls, 0)

    # --------------------------------------------------------------------------

    def output_results(self) -> None:
        '''Output results to files.
        Args: 
            N/A
        Returns: 
            N/A 
        '''
        # ----------------------------------------------------------------------
        # Write a single CSV file
        def write_file(fn_txt: str, data: Records, fields: list[str]):
            fb = os.path.basename(self.filename)
            fn = os.path.join(self.config.dir_data_out,
                              utils.append_filename(fb, fn_txt))
            log.info('Writing %s file: %s', fn_txt, fn)
            with open(fn, 'w', encoding='utf-8') as out_file:
                writer = csv.DictWriter(out_file, lineterminator='\r',
                                        quoting=csv.QUOTE_NONNUMERIC,
                                        fieldnames=fields,
                                        extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data)
        # ----------------------------------------------------------------------

        log.info('Writing results to CSV files')
        write_file('_key', self.records, const.I_COLUMNS)
        write_file('_skip', self.skipped, const.S_COLUMNS)
        write_file('_swift', self.swift, const.S_COLUMNS)
        write_file('_processed', self.key_processed, [const.I_RECORDKEY])
        # Update the processed records file
        self.update_processed()
        # Only produce Excel workbook if config flag set
        if self.config.excel is True:
            # Use threading to allow spinner animation
            thread = threading.Thread(target=self.output_excel)
            thread.start()
            with spinner.Spinner('Writing Excel file...') as spin:
                while thread.is_alive():
                    spin.next()
                    time.sleep(0.1)
            thread.join()
    # --------------------------------------------------------------------------

    def process_records(self) -> None:
        '''Process each of the iRecord records.
        Args: 
            N/A
        Returns: 
            N/A 
        '''
        log.info('Processing records')
        # Maintain a set of created records for de-duping
        dupechecks: DupeDict = dict()
        with Bar('Processing records...', max=len(self.records)) as progbar:
            for rec in self.records:
                progbar.next()
                rules = Rules(rec, self.crosscheck)
                res = rules.get_swift()
                # Determine whether record should be skipped
                itype, inote = rules.is_skip(res, dupechecks)
                if len(itype) > 0:
                    # Handle cloned results
                    for r in res:
                        r[const.S_IMPORTTYPE] = itype
                        r[const.S_IMPORTNOTE] = inote
                    self.skipped += res
                else:
                    self.swift += res
                # Determine whether the record has been previously processed
                if self.crosscheck.is_processed(rec[const.I_RECORDKEY]):
                    self.key_processed.append(rec)
                else:
                    self.key_new.append(rec)
        log.info('Number of iRecord records: %s', f'{len(self.records):,}')
        log.info('Number of skipped records: %s', f'{len(self.skipped):,}')
        log.info('Number of Swift records: %s', f'{len(self.swift):,}')
        log.info('Number of previously processed records: %s', f'{len(self.key_processed):,}')
        self.crosscheck.georegion.plot(self.filename)
        _, outside = self.crosscheck.georegion.count()
        log.info('Number of gridrefs outside region: %s', f'{outside:,}')
        self.output_results()

    # --------------------------------------------------------------------------

    def read_file(self, fn: str) -> bool:
        '''Read the contents of a given CSV file.
        Args: 
            fn (string) - CSV filename
        Returns: 
            (bool) - True if successful, else False
        '''
        log.info('Reading file: %s', fn)
        # Initialise
        self.filename = fn
        self.key_new.clear()
        self.key_processed.clear()
        self.records.clear()
        self.skipped.clear()
        self.swift.clear()
        rv: bool = True
        self.crosscheck.georegion.reset()
        self.records.clear()
        # Read file
        with open(fn, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for ix, dct in enumerate(reader):
                dct[const.I_KEY] = ix + 1
                self.records.append(dct)

        # Check that the input file has the correct columns
        rv = self.check_columns()
        if rv is True:
            log.debug('Number of records read from file: %i', len(self.records))
            self.process_records()

        return rv
    # --------------------------------------------------------------------------

    def update_processed(self):
        '''Update the processed records file.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        fn = self.config.file_processed
        if len(fn) == 0:
            log.debug('No processed file to update')
            return
        log.info('Updating processed file: %s', fn)
        df = utils.read_csv_robust(fn)
        # Extract RecordKey from each object
        record_keys = [obj[const.I_RECORDKEY] for obj in self.key_new]
        new_df = pd.DataFrame(record_keys, columns=[df.columns[0]])
        df = pd.concat([df, new_df], ignore_index=True).drop_duplicates()
        df.to_csv(fn, index=False, encoding='utf-8-sig')

# ------------------------------------------------------------------------------

'''
End
'''
