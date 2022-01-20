from __future__ import print_function
import pickle
import time
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/admin.directory.orgunit"]


def main():
    print("Admin SDK Directory API script")

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("admin", "directory_v1", credentials=creds)

    # Create a new org unit
    body = {
        "name": "NTNUITest",
        "parentOrgUnitPath": "/",
    }
    results1 = service.orgunits().insert(customerId="my_customer", body=body).execute()

    print(results1)

    # List all org units
    results = service.orgunits().list(customerId="my_customer").execute()
    print("Org Units:")
    if "organizationUnits" in results:
        for unit in results["organizationUnits"]:
            print("{} ({})".format(unit["name"], unit["orgUnitPath"]))


main()
