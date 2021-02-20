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
    """test script, please ignore"""
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
    
    ### Steps: 
    ### 1. Get list of full names of all users of which aliases should be deleted and append to a list
    ### 2. Call Google API/user accounts, match names and find all aliases to delete, add to a list
    ### 3. Add exceptions if alias includes words
    ### 4. Call Google API/user aliases, delete aliases from a list

    # Get list of user full names seperated by newline
    data = open('users.csv', 'r', encoding='utf-8')
    fullNamesDirty = data.readlines()
    data.close()
    fullNames = []
    for name in fullNamesDirty:
        fullNames.append(name.strip("\n"))
    print(fullNames)

    # Call the Admin SDK Directory API
    results = service.users().list(customer='my_customer', maxResults=10, # pylint: disable=maybe-no-member
                                orderBy='email').execute()
    users = results.get('users', [])

    # Examples
    # Send a request - created_account = self.get_service().users().insert(body=body).execute()
    # Format output - print(u'{0} ({1})'.format(user['primaryEmail'], user['name']['fullName']))
    #                 print(user['aliases'])

    if not users:
        print('No users in the domain!')
    else:
        print('---- Output: ----')
        for user in users:
            try:
                print(u'{0} - {1}'.format(user['name']['fullName'], user['aliases']))
                print(u'{0}'.format(user['aliases']).strip("[']"))
            except KeyError:
                pass
            time.sleep(0.2) # to avoid rate limit
            

if __name__ == '__main__':
    main()