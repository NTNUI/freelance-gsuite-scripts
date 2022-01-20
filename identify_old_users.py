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


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def should_delete(date, is_superuser):
    """Checks if the G Suite account should be deleted."""
    if is_superuser:
        return False

    INACTIVE_LIMIT = 12
    return diff_month(datetime.now(), datetime.fromisoformat(date)) > INACTIVE_LIMIT


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
            if should_delete(user["lastLoginTime"][:-5], user["isAdmin"]):
                f.writelines(
                    user["primaryEmail"]
                    + " - "
                    + str(user["isAdmin"])
                    + " - "
                    + str(user["lastLoginTime"])
                    + "\n"
                )
    f.close()


main()
