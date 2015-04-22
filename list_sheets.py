#!/usr/bin/python

# Do OAuth2 stuff to create credentials object
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run
import time

storage = Storage("creds.dat")
credentials = storage.get()
if credentials is None or credentials.invalid:
  credentials = run(flow_from_clientsecrets("client_secrets.json", scope=["https://spreadsheets.google.com/feeds"]), storage)

# Use it within gdata
import gdata.spreadsheets.client
import gdata.gauth
import gdata.spreadsheets.data.Table


gd_client = gdata.spreadsheets.client.SpreadsheetsClient()
gd_client.auth_token = gdata.gauth.OAuth2TokenFromCredentials(credentials)

#print gd_client.get_spreadsheets()


# Find this value in the url with 'key=XXX' and copy XXX below
# This is spreadsheet with title:  Network change for ALB bonding
spreadsheet_key = '1Ua0Ir53h12U2doayNXVBk6M6Q4fzDwaIBJGSh6jqo-Y'
# All spreadsheets have worksheets. I think worksheet #1 by default always
# has a value of 'od6'
worksheet_id = '1'

cell_query = gdata.spreadsheets.client.CellQuery(
min_row=39, max_row=39, min_col=1, max_col=1, return_empty=True)
cells = gd_client.GetCells(spreadsheet_key, worksheet_id, q=cell_query)
cell_entry = cells.entry[0]
cell_entry.cell.input_value = 'hackatron.met.no'
gd_client.update(cell_entry) # This is the call to Google Server to update


#Batch update
#range = "A6:D1113"
#cellq = gdata.spreadsheets.client.CellQuery(range=range, return_empty='true')
#cells = gd_client.GetCells(sprd_key, wrksht_key, q=cellq)
#batch = gdata.spreadsheets.data.BuildBatchCellsUpdate(sprd_key, wrksht_key)
#n = 1
#for cell in cells.entry:
#cell.cell.input_value = str(n)
#batch.add_batch_entry(cell, cell.id.text, batch_id_string=cell.title.text, operation_string='update')
#n = n + 1
#gd_client.batch(batch, force=True) # A single call to Google Server to update all cells.
