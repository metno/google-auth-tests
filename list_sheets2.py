#!/usr/bin/python

import os
import math
import string
import oauth2client.file
import oauth2client.client
import oauth2client.tools

import gdata.gauth
import gdata.spreadsheets.client

int2base = lambda a, b: ''.join(
    [(string.digits + string.lowercase + string.uppercase)[(a/b**i)%b] for i in xrange(int(math.log(a, b)), -1, -1)]
    )

def to_wid(gid_id):
    return int2base(gid_id ^ 31578, 36) 

if __name__ == '__main__':

    script_name = os.path.basename(__file__).split('.')[0]
    secret_file = os.path.expanduser("~/." + script_name + ".secret")

    storage = oauth2client.file.Storage(secret_file)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        flow = oauth2client.client.OAuth2WebServerFlow(
            client_id='867946856044-n8n69pnpmm3m79h6sqr7kkfgssju9lpi.apps.googleusercontent.com',
            client_secret='n0I4ljpXxzK45e6OUog5ETRX',
            scope=["https://spreadsheets.google.com/feeds"],
            redirect_uri=' urn:ietf:wg:oauth:2.0:oob'
            )

        #credentials = run(flow_from_clientsecrets("client_secrets.json", scope=["https://spreadsheets.google.com/feeds"]), storage)
        credentials = oauth2client.tools.run(flow, storage)

    gd_client = gdata.spreadsheets.client.SpreadsheetsClient()
    gd_client.auth_token = gdata.gauth.OAuth2TokenFromCredentials(credentials)

    #print gd_client.get_spreadsheets()

    spreadsheet_key = '1Ua0Ir53h12U2doayNXVBk6M6Q4fzDwaIBJGSh6jqo-Y'
    worksheet_id = to_wid(0)

    cell_query = gdata.spreadsheets.client.CellQuery(
        range="A39:A39",
        return_empty=True
        )

    cells = gd_client.GetCells(spreadsheet_key, worksheet_id, q=cell_query)
    cell_entry = cells.entry[0]
    cell_entry.cell.input_value = 'hackatron.met.no'
    gd_client.update(cell_entry) # This is the call to Google Server to update

