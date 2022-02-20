# What is this

This is a tool to check that all board members have the correct aliases in gsuite

# How to use

1. Export data from medlemssystemet
2. Export data from gsuite / slack
3. Run the project
4. Check exportfiles with results

## 1. Export data

### 1.a Export all members from api.ntnui.no/admin

Export will return a CSV file. This need to be converted to JSON. Create a file called members.json and add the content.
It should look something like this:

```
[
  {
    "id": 1,
    "role": "Member",
    "name": "Billy Hansen",
    "gruppe": "Badminton"
  },
  {
    "id": 2,
    "role": "Member",
    "name": "Trond Tenåsen",
    "gruppe": "Tennis"
  },
  {
    "id": 3,
    "role": "Member",
    "name": "Theodor Thoresen",
    "gruppe": "Tennis"
  }
  ...
]
```

### 1.b Export all users from the database

Query:

```
select '{"mail":"' || contact_email || '", "name":" ' || first_name || ' ' || last_name || '"}'  from public.accounts_usermodel where contact_email is not null
```

This should also be converted to a JSON. Looking like this:

```
[
  { "mail": "sprint.sprintesen@ntnui.no", "name": "Sprint Sprintesen" },
  { "mail": "peter.pettersen@ntnui.no", "name": "Peter Pettersen" },
  { "mail": "hans.hansen@ntnui.no", "name": "Hans Hansen" }
]
```

Add this to a file called users.json

## 2 Export data from slack or gsuite (depending on what checks you are doing)

### 2.a Export from gsuite

Export all aliases from gsuite
Run this script in google scripts https://script.google.com/

```
function listUsersWithEmailAliases() {
  let pageToken
  let page
  do {
    page = AdminDirectory.Users.list({
      customer: 'my_customer',
      maxResults: 100,
      pageToken,
      fields: 'users(name/fullName,primaryEmail,aliases),nextPageToken',
    })
    let users = page.users
    if (users) {
      for (let i = 0; i < users.length; i++) {
        const user = users[i]
        if (user.aliases && user.aliases.length > 0) {
          for (let s = 0; s < user.aliases.length; s++){
            let alias = user.aliases[s]
            Logger.log(`{"name": "${user.name.fullName}","originalMail": "${user.primaryEmail}","aliasText": "${alias}"},`)
          }
        }
      }
    } else {
      Logger.log('No users found.')
    }
    pageToken = page.nextPageToken
  } while (pageToken)
}
```

Create a file called aliases.json and paste the contents from output (this might need to be modified a bit) at the end you should have a json list looking like this:

```
[
    {"name": "Sprint Sprintesen","originalMail": "sprint.sprintesen@ntnui.no","aliasText": "sprint-leder@ntnui.no"},
    {"name": "Peter Pettersen","originalMail": "peter.pettersen@ntnui.no","aliasText": "rumpeldunk-nestleder@ntnui.no"},
    {"name": "Hans Hansen","originalMail": "hans.hansen@ntnui.no","aliasText": "badminton-kasserer@ntnui.no"}
]
```

### 2.b Export from slack

Ask @xtrah (Mats)

## 3

Run the project

Make sure you have .net installed.
This script uses .net 6
Open folder in terminal and run:

```
dotnet run
```

Easy ;)

## 4. Check the output file

If you are checking slack -> the program will generate slackresult.json

If you are checking gsuite alias -> the program will generate aliasresult.json
