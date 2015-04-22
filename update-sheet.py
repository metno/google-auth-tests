#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import httplib2

# Import authentication libraries
import oauth2client.file
import oauth2client.client
import oauth2client.tools

# Import editing  libraries
import gdata.gauth
import gdata.spreadsheets.client

if __name__ == '__main__':

    # Just create ~/.scriptname.secret for oauth2 credentials
    script_name = os.path.basename(__file__).split('.')[0]
    secret_file = os.path.expanduser("~/." + script_name + ".secret")

    # Create empty or get oauth2 credentials
    storage = oauth2client.file.Storage(secret_file)
    credentials = storage.get()

    # If no credentials exists authenticate with google 
    if credentials is None or credentials.invalid:

        # Create Oauth flow
        flow = oauth2client.client.OAuth2WebServerFlow(
            client_id='867946856044-n8n69pnpmm3m79h6sqr7kkfgssju9lpi.apps.googleusercontent.com',
            client_secret='n0I4ljpXxzK45e6OUog5ETRX',
            scope=["https://spreadsheets.google.com/feeds"],
            redirect_uri=' urn:ietf:wg:oauth:2.0:oob'
            )

        # Alternative method with client_id and client_secret in json
        #credentials = oauth2client.tools.run(
        #    flow_from_clientsecrets("client_secrets.json", scope=["https://spreadsheets.google.com/feeds"]), 
        #    storage
        #    )
        
        # Get and store the credentials
        credentials = oauth2client.tools.run(flow, storage)

    # Force refresh of access token
    # Hopfully stores new token to disk
    if credentials.access_token_expired:
        credentials.refresh(httplib2.Http())

    # Get a spreadsheet client object
    gd_client = gdata.spreadsheets.client.SpreadsheetsClient()

    # Authenticate 
    gd_client.auth_token = gdata.gauth.OAuth2TokenFromCredentials(credentials)

    # List all spreadsheets
    #print gd_client.get_spreadsheets()

    # Our Hackaton spreadsheet
    spreadsheet_key = '1slih48v4Fr7uaZDwFZRQ3U0_KlOhr2IHP1URzTx9ECM'

    # Sheet number one
    worksheet_id = 1
    
    # Create the range we're working on
    #   range = A1:B20 equals with range = R1C1:R20C2
    cell_query = gdata.spreadsheets.client.CellQuery( range="A1",  return_empty=True )

    # Get the cell range from the sheet
    cells = gd_client.GetCells(spreadsheet_key, worksheet_id, q=cell_query)

    # We're working on the only cell in our range
    cell_entry = cells.entry[0]

    # Set cell value
    cell_entry.cell.input_value = 'HACKATON!'

    # Update spreadsheet
    gd_client.update(cell_entry) 

    #
    # Example how to use gdata.spreadsheet.service with oauth2
    #
    # Use it within old gdata
    #import gdata.spreadsheet.service
    #import gdata.service
    #
    #client = gdata.spreadsheet.service.SpreadsheetsService(
    #additional_headers={'Authorization' : 'Bearer %s' % credentials.access_token})
    #
    #entry = client.GetSpreadsheetsFeed(spreadsheet_key)
    #print entry.title
