from __future__ import print_function
import pickle
import re
import time
import os.path
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/admin.directory.user"]


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

    f = open("output.csv", "w")

    response = (
        service.users()
        .list(
            customer="my_customer",
            maxResults=500,
            orderBy="email",
        )
        .execute()
    )

    responses = []
    responses.append(response["users"])

    while response.get("nextPageToken") is not None:
        response = (
            service.users()
            .list(
                customer="my_customer",
                maxResults=500,
                orderBy="email",
                pageToken=response["nextPageToken"],
            )
            .execute()
        )
        responses.append(response["users"])

    for response in responses:
        for user in response:
            try:
                print(user["primaryEmail"] + " - " + user["recoveryEmail"])
            except KeyError as err:
                print(err)
                if err.args[0] == "recoveryEmail":
                    try:
                        f.writelines("Setting recovery email for " + user["primaryEmail"] + " to " + user["emails"][0]["address"] + "\n")
                        service.users().patch(userKey=user["primaryEmail"], body={"recoveryEmail": user["emails"][0]["address"]}).execute()
                    except KeyError:
                        f.writelines("No email found for " + user["primaryEmail"] + ", skipping..." + "\n")
            try:
                print(user["primaryEmail"] + " - " + user["recoveryPhone"])
            except KeyError as err:
                print(err)
                if err.args[0] == "recoveryPhone":
                    try:
                        f.writelines("Setting recovery phone for " + user["primaryEmail"] + " to " + user["phones"][0]["value"] + "\n")
                        service.users().patch(userKey=user["primaryEmail"], body={"recoveryPhone": user["phones"][0]["value"]}).execute()
                    except KeyError:
                        f.writelines("No phone number found for " + user["primaryEmail"] + ", skipping..." + "\n")
    f.close()
                


main()
