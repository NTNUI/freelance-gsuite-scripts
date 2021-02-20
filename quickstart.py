# test script, please ignore

from __future__ import print_function
import pickle
import time
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

def main():
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)

    ### Let's goooo
    print('Admin SDK Directory API script')
    
    # Get list of user full names seperated by newline
    data = open('users.csv', 'r', encoding='utf-8')
    fullNamesDirty = data.readlines()
    data.close()
    fullNames = []
    for name in fullNamesDirty:
        fullNames.append(name.strip("\n"))
    print(fullNames)

    # Call the Admin SDK Directory API
    results = service.users().list(customer='my_customer', maxResults=200, # pylint: disable=maybe-no-member
                                orderBy='email').execute()
    users = results.get('users', [])

    # created_account = self.get_service().users().insert(body=body).execute()

    if not users:
        print('No users in the domain.')
    else:
        print('Users:')
        for user in users:
            # print(u'{0} ({1})'.format(user['primaryEmail'], user['name']['fullName']))
            try:
                print(user['aliases'])
            except KeyError:
                pass
            time.sleep(0.2)
            

if __name__ == '__main__':
    main()