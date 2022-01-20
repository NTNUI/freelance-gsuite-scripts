# Freelance GSuite scripts

To use any scripts, you need credentials for Google APIs. Create and download OAuth 2.0 credentials at [Google Developer Console](https://console.developers.google.com/apis/credentials). Store the `credentials.json` in the same directory as the script files. 

When running a script the first time, it will require account authorization to access the Google API. This will create a `token.pickle` file in the same directory as the script files. Once created, the script will automatically use the credentials stored in the `token.pickle` file for subsequent runs.