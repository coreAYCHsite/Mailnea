#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import gspread                  # https://github.com/burnash/gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
import codecs

script_dir = os.path.dirname(os.path.realpath(__file__))

json_key = json.load(open( script_dir + '/../lib/Mailnesia/mailnesia-private.json'))
scope = ['https://spreadsheets.google.com/feeds']

# Obtain OAuth2 credentials from Google Developers Console (http://gspread.readthedocs.io/en/latest/oauth2.html)
credentials = SignedJwtAssertionCredentials(json_key['gspread']['client_email'], json_key['gspread']['private_key'], scope)

gs = gspread.authorize(credentials)

# open translation spreadsheet at https://docs.google.com/spreadsheets/d/1Qd6QHFWXmD-Cyz3nV3Q0DwKj3b5wkwTflcS6PKIWkoo
spreadsheet = gs.open_by_key('1Qd6QHFWXmD-Cyz3nV3Q0DwKj3b5wkwTflcS6PKIWkoo')



def save_worksheet (name):
    '''name should be the name of the worksheet, "mailnesia_translation" or "main page" or "features page"
    '''
    worksheet = spreadsheet.worksheet(name)
    list_of_lists = worksheet.get_all_values()

    tsv = ""                    # variable for storing the whole worksheet, tab separated

    for line in list_of_lists:
        for position, cell in enumerate(line):
            tsv = tsv + cell.replace("\n", " ") # ignore newlines inside cells
            if (position < len(line)-1):  # for all items except the last
                tsv = tsv + "\t"          # separate with tab
        tsv = tsv + "\n"                  # add newline


    # open .tsv for writing
    f_translation = codecs.open( script_dir + '/../translation/' + 'mailnesia_translation - ' + name + '.tsv', encoding='utf-8', mode='w')
    f_translation.write(tsv)
    f_translation.close()
    


save_worksheet("mailnesia_translation")
save_worksheet("main page")
save_worksheet("features page")

