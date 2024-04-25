'''
About  : Implements the Rules class which contains the logic to transform
         iRecord data into Swift format.
Author : Kevin Morley
Version: 1 (21-Mar-2023)
'''

# ------------------------------------------------------------------------------

import const                        # KPM
import logging
import re
import utils                        # KPM

from datetime import datetime

# ------------------------------------------------------------------------------

log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Class which performs the transformation of iRecord data into Swift format.

NO_RECORD = 'not recorded'  # iRecord standard text

class Rules:

    # --------------------------------------------------------------------------
    # Constructor.

    def __init__(self, record, crosscheck):
        '''
        Params: record (dict) = iRecord record to be assessed
                crosscheck (CrossChecker) - instance of object used for lookups
        Return: N/A
        '''
        self.crosscheck = crosscheck
        self.record = record.copy()
        self.record[const.I_IMPORTTYPE] = ''
        self.record[const.I_IMPORTNOTE] = ''        
        self.record[const.I_IMPORTCOMMENT] = ''        
        # Returned processed records in list format as one record may be cloned
        self.processed = []
        self.swift = [] 
        self.processed.append(self.record.copy())

    # --------------------------------------------------------------------------
    # Populate the swift and processed export lists.

    def get_swift(self):
        '''
        Params: N/A
        Return: (list, list)
        '''
        self.init_swift()
        self.get_swift_identity()   
        self.get_swift_recordtype()
        self.get_swift_comment()    # call second last in sequence
        self.get_swift_sexstage()   # call last in sequence - cloning of dict
        return self.swift, self.processed

    # --------------------------------------------------------------------------
    # Process the comment data. Generate comment form multiple fields.

    def get_swift_comment(self):
        '''
        Params: N/A
        Return: N/A
        '''
        # ----------------------------------------------------------------------
        # Format a sub-section of the comment string
        def format(name, value):
            v = value.strip()
            return f'[{name}: "{v}"] ' if len(v) > 0 else ''
        # ----------------------------------------------------------------------
        
        com = det_com = ''
        com += format('iRecord Key', self.processed[0][const.I_RECORDKEY])
        com += format('Source', self.processed[0][const.I_SOURCE])
        com += format('Recorder certainty', self.processed[0][const.I_RECORDER_CERTAINTY])
        com += format('Comment', self.processed[0][const.I_COMMENT])
        com += format('Sample Comment', self.processed[0][const.I_SAMPLE_COMMENT])
        v = self.processed[0][const.I_VERIFIER]
        com += format('Verifier', v)
        if len(v) > 0:
            det_com += f'Verified by {v} '
        vos = self.processed[0][const.I_VERIFIED_ON]
        if len(vos) > 0:
            dto = datetime.strptime(vos, '%d/%m/%Y %H:%M')
            dts = dto.strftime('%d/%m/%Y')
            com += format('Verified on', dts)
            det_com += dts
        com += format('Licence', self.processed[0][const.I_LICENCE])
        
        s = self.swift[0]
        p = self.processed[0]
        s[const.S_COMMENTS] = com
        p[const.I_IMPORTCOMMENT] = com
        s[const.S_DETERMINAION_COMMENT] = det_com
        if p[const.I_VERIFICATION_STATUS_2].lower() == 'not reviewed':
            s[const.S_DETERMINATION_TYPE] = 'Requires Confirmation'   
        else:
            s[const.S_DETERMINATION_TYPE] = p[const.I_VERIFICATION_STATUS_2]

    # --------------------------------------------------------------------------
    # Process the identity data. Complicated by potential use of usernames.

    def get_swift_identity(self):
        '''
        Params: N/A
        Return: N/A
        '''
        # ----------------------------------------------------------------------
        # Return the supplied name in a Swift-compatible format
        def format(name):
            if len(name) == 0:
                return name
            
            n = name.replace('.', ' ')
            # Do we have 'surname, forename'?
            p = n.split(',')
            if len(p) > 1:
                rv = ' '.join(reversed(p))
            else:
                # Do we have 'forename surname'?
                p = n.split(' ')
                if len(p) > 1:
                    rv = n
                else:
                    # Assume we have a username - ok to use real identity?
                    rv = self.crosscheck.get_user_identity(name)
                    if len(rv) == 0:
                        # Permission for identity not granted
                        s_l = self.processed[0][const.I_SOURCE].lower()
                        if 'irecord' in s_l:
                            rv = 'Anon at iRecord'
                        elif 'inaturalist' in s_l:
                            rv = 'Anon at iNaturalist'
                        else:
                            rv = name
                            log.debug(f'Unknown source: {s_l}')
            
            return rv
        # ----------------------------------------------------------------------
        # Process the 3 identities contained within iRecord.
        rec = format(self.processed[0][const.I_RECORDER])
        det = format(self.processed[0][const.I_DETERMINER])
        ver = format(self.processed[0][const.I_VERIFIER])
        
        self.processed[0][const.I_RECORDER] = rec
        self.processed[0][const.I_DETERMINER] = det
        self.processed[0][const.I_VERIFIER] = ver

        self.swift[0][const.S_OBSERVER] = rec
        self.swift[0][const.S_DETERMINER] = det    
        
    # --------------------------------------------------------------------------
    # Process the record type data. Map iRecord to Swift equivalent.

    def get_swift_recordtype(self):
        '''
        Params: N/A
        Return: N/A
        '''
        MSG = 'Record Type'
        MSG_NOTE = '[Record Type: "{}"; Comment: "{}"]'
        p = self.processed[0]
        s = self.swift[0]
        rt = self.crosscheck.get_record_type(p[const.I_SAMPLE_METHOD])
        if rt is None:
            # add unknown sample method warning
            p[const.I_IMPORTTYPE] = utils.append_comment(
                        p[const.I_IMPORTTYPE], MSG)
            s[const.S_IMPORTTYPE] = utils.append_comment(
                        s[const.S_IMPORTTYPE], MSG)
            note = MSG_NOTE.format(p[const.I_SAMPLE_METHOD], p[const.I_COMMENT])            
            p[const.I_IMPORTNOTE] = (p[const.I_IMPORTNOTE] + ' ' + note if
                len(p[const.I_IMPORTNOTE]) > 0 else note)
            s[const.S_IMPORTNOTE] = (s[const.S_IMPORTNOTE] + ' ' + note if
                len(s[const.S_IMPORTNOTE]) > 0 else note)
        else:
            s[const.S_RECORD_TYPE] = rt
    
    # --------------------------------------------------------------------------
    # Process the sex/stage data. Complicated by potential need to clone record.

    def get_swift_sexstage(self):
        '''
        Params: N/A
        Return: N/A
        '''
        MSG = 'Cloned'
        MSG_NOTE = '[Count of sex or stage: "{}"; Sex: "{}"; Stage: "{}"]'
        
        c = self.processed[0][const.I_COUNT_OF_SEX_OR_STAGE].lower()
        n = utils.word_to_num(c)
        if n is not None:
            c = str(n)    
        # If count is a number or number range, then return
        if len(c) == 0 or c.replace('-', '').isdigit():
            return

        # Extract abundance
        pattern = r">?c?\d[0-9\-+/,'s ]*"
        num = re.findall(pattern, c)
        # Extract sex/stage terms
        trm = re.split(pattern, c)
        if all(len(t) == 0 for t in trm):
            return
        if len(num) != len(trm)-1:
            log.error(f'"{const.I_COUNT_OF_SEX_OR_STAGE}" parse error: {c}')
            return
        # Prepare for cloning of records
        p_c = self.processed[0]
        s_c = self.swift[0]
        # if len(num) > 0:
        if len(num) > 1:
            sex = self.processed[0][const.I_SEX].lower()
            stage = self.processed[0][const.I_STAGE].lower()
            p_c[const.I_IMPORTTYPE] = utils.append_comment(
                    p_c[const.I_IMPORTTYPE], MSG)
            s_c[const.S_IMPORTTYPE] = utils.append_comment(
                    s_c[const.S_IMPORTTYPE], MSG)
            note = MSG_NOTE.format(c, sex, stage)
            p_c[const.I_IMPORTNOTE] = (p_c[const.I_IMPORTNOTE] + ' ' + note if
                len(p_c[const.I_IMPORTNOTE]) > 0 else note)
            s_c[const.S_IMPORTNOTE] = (s_c[const.S_IMPORTNOTE] + ' ' + note if
                len(s_c[const.S_IMPORTNOTE]) > 0 else note)
        # Process each pair of number and term
        for i in range(len(num)):                                 
            sex = ''
            stage = ''
            spec = trm[i+1].lower().strip()
            spec = re.sub(r'[(),]', '', spec)
            # Parse spec into separate words and check against sex/stage terms
            words = spec.split()
            for word in words:
                # Is this a sex/stage term?
                if word in const.STAGE_TERMS:
                    stage = const.STAGE_TERMS[word].capitalize()
                elif word in const.SEX_TERMS:
                    sex = const.SEX_TERMS[word].lower()
            # No stage found in comment - use 'Stage' field                        
            if len(stage) == 0:
                stage = p_c[const.I_STAGE]

            n = num[i].strip()
            p_c[const.I_COUNT_OF_SEX_OR_STAGE] = n
            s_c[const.S_ABUNDANCE] = n
            p_c[const.I_COUNT_OF_SEX_OR_STAGE] = n
            p_c[const.I_SEX] = sex
            p_c[const.I_STAGE] = stage
            s_c[const.S_SEXSTAGE] = f'{stage} {sex}'.strip()
            # Avoid duplicating first record
            if i > 0:
                self.processed.append(p_c)          
                self.swift.append(s_c)
            # Prepare for next loop
            p_c = self.processed[0].copy()
            s_c = self.swift[0].copy()

    # --------------------------------------------------------------------------
    # Initialise the Swift export list.

    def init_swift(self):
        '''
        Params: N/A
        Return: N/A
        '''
        self.swift.clear()
        s = {}
        c = self.record[const.I_COUNT_OF_SEX_OR_STAGE].lower()
        n = utils.word_to_num(c)
        if n is not None:
            c = str(n)    

        stage = '' if self.record[const.I_STAGE].lower() == NO_RECORD \
                    else self.record[const.I_STAGE].capitalize()
        sex = '' if self.record[const.I_SEX].lower() == NO_RECORD \
                    else self.record[const.I_SEX].lower()
        s[const.S_KEY] = self.record[const.I_KEY]
        s[const.S_IMPORTTYPE] = ''
        s[const.S_IMPORTNOTE] = ''
        s[const.S_NAME] = self.record[const.I_TAXON]
        s[const.S_DATE] = self.record[const.I_DATE_FROM]
        s[const.S_LOCATION] = self.record[const.I_SITE_NAME]
        s[const.S_GRID_REFERENCE] = self.record[const.I_OUTPUT_MAP_REF]
        s[const.S_ABUNDANCE] = c
        s[const.S_SEXSTAGE] = f'{stage} {sex}'.strip()
        s[const.S_RECORD_TYPE] = ''
        s[const.S_OBSERVER] = ''
        s[const.S_DETERMINER] = ''
        s[const.S_COMMENTS] = ''
        s[const.S_DETERMINATION_TYPE] = ''
        s[const.S_DETERMINAION_COMMENT] = ''
        self.swift.append(s)

    # --------------------------------------------------------------------------
    # Perform tests to determine whether record should be skipped.

    def is_skip(self):
        '''
        Params: N/A
        Return: (string, string) - type/note with reasons for skip, else ('','')
        '''
        rvs = []   # list of tuples returned from individual tests
        # Run tests
        rvs.append(self.is_skip_gridref())
        rvs.append(self.is_skip_licence())
        rvs.append(self.is_skip_rank())
        rvs.append(self.is_skip_region())
        rvs.append(self.is_skip_verification())
        # Process results of all tests into two strings returned as a tuple
        rv_n = rv_t = ''
        for rv in rvs:
            rv_t += rv[0]
            rv_n += rv[1]
            
        return rv_t.strip(' ;'), rv_n.strip(' ;')

    # --------------------------------------------------------------------------
    # Determine whether record should be skipped based upon its gridref.

    def is_skip_gridref(self):
        '''
        Params: N/A
        Return: (string, string) - type/note describing reason for skip, else ''
        '''
        skip_str = '[Gridref: "{}"] '
        g = self.record[const.I_OUTPUT_MAP_REF]     # gridref
        rv_n = ''
        if len(g) < 6:      # TODO - confirm correct minimum length
            rv_n = skip_str.format(g)

        rv_t = ' Gridref;' if len(rv_n) > 0 else ''
        return rv_t, rv_n

    # --------------------------------------------------------------------------
    # Determine whether record should be skipped based upon its licence.

    def is_skip_licence(self):
        '''
        Params: N/A
        Return: (string, string) - type/note describing reason for skip, else ''
        '''
        skip_str = '[Licence: "{}"] '
        l_u = self.record[const.I_LICENCE].upper()     # licence
        r_l = self.record[const.I_RECORDER].lower()    # recorder
        rv_n = ''
        if (l_u in {'CC BY', 'CC BY-NC'} and 
                not self.crosscheck.is_permission_granted(r_l)):
            rv_n = skip_str.format(l_u)

        rv_t = ' Licence;' if len(rv_n) > 0 else ''
        return rv_t, rv_n

    # --------------------------------------------------------------------------
    # Determine whether record should be skipped based upon its rank.

    def is_skip_rank(self):
        '''
        Params: N/A
        Return: (string, string) - type/note describing reason for skip, else ''
        '''
        skip_str = '[Rank: "{}"; Kingdom: "{}"; Order: "{}"; Taxon: "{}"] '
        k_l = self.record[const.I_KINGDOM].lower()  # kingdom
        o_l = self.record[const.I_ORDER].lower()    # order
        r_l = self.record[const.I_RANK].lower()     # rank
        t_l = self.record[const.I_TAXON].lower()    # taxon
        rv_n = ''
        if r_l in ['domain', 'kingdom', 'class', 'order']:
            # Not acceptable
            rv_n = skip_str.format(r_l, k_l, o_l, t_l)
        elif r_l == 'family':
            # Acceptable for insects only (possibly with some exceptions)
            if (o_l not in const.ORDERS_INSECTA or 
                    self.crosscheck.is_excluded_taxon(t_l)):
                rv_n = skip_str.format(r_l, k_l, o_l, t_l)
        elif r_l == 'genus':
            # Acceptable for insects, plants and bats only
            if (o_l not in const.ORDERS_INSECTA and k_l != 'plantae' and 
                o_l != 'chiroptera'):
                rv_n = skip_str.format(r_l, k_l, o_l, t_l)

        rv_t = ' Rank;' if len(rv_n) > 0 else ''
        return rv_t, rv_n
    
    # --------------------------------------------------------------------------
    # Determine whether record should be skipped based upon whether it is 
    # inside/outside the in-scope VC region

    def is_skip_region(self):
        '''
        Params: N/A
        Return: (string, string) - type/note describing reason for skip, else ''
        '''
        skip_str = '[Region: "{}"] '
        g = self.record[const.I_OUTPUT_MAP_REF]     # gridref
        inside = self.crosscheck.georegion.gridref_in_region(g)
        rv_n = ''
        if not inside:
            rv_n = skip_str.format(g)

        rv_t = ' Region;' if len(rv_n) > 0 else ''
        return rv_t, rv_n

    # --------------------------------------------------------------------------
    # Determine whether record should be skipped based upon its verification.

    def is_skip_verification(self):
        '''
        Params: N/A
        Return: (string, string) - type/note describing reason for skip, else ''
        '''
        skip_str = '[Verification 1: "{}"; Verification 2: "{}"] '
        v1_l = self.record[const.I_VERIFICATION_STATUS_1].lower()   # verify 1
        v2_l = self.record[const.I_VERIFICATION_STATUS_2].lower()   # verify 2
        if (v1_l in {'accepted', 'queried', 'unconfirmed'} and 
            v2_l in {'considered correct', 'correct', 'not reviewed', 
                     'plausible', 'unconfirmed', ''}):
            rv_n = ''
        else:
            rv_n = skip_str.format(v1_l, v2_l)

        rv_t = ' Verification;' if len(rv_n) > 0 else ''
        return rv_t, rv_n


# ------------------------------------------------------------------------------
# Test
# ------------------------------------------------------------------------------
# Run module-specific tests.

def do_test():
    '''
    Params: N/A
    Return: (bool) Returns True if tests succesful, else False
    '''
    log.info('-'*25)
    log.info('Beginning test [rules.py]...')
    rv = True
    log.info(f'Finished test. Test passed: {rv}')
    return rv

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
            format='[%(module)s]-[%(funcName)s]-[%(levelname)s] - %(message)s')
        
    do_test()

# ------------------------------------------------------------------------------
       
'''
End
'''