#!/usr/bin/python

# Do OAuth2 stuff to create credentials object
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run

storage = Storage("creds.dat")
credentials = storage.get()
if credentials is None or credentials.invalid:
  credentials = run(flow_from_clientsecrets("client_secrets.json", scope=["https://spreadsheets.google.com/feeds"]), storage)

# Use it within gdata
import gdata.spreadsheets.client
import gdata.gauth

gd_client = gdata.spreadsheets.client.SpreadsheetsClient()
gd_client.auth_token = gdata.gauth.OAuth2TokenFromCredentials(credentials)
print gd_client.get_spreadsheets()
