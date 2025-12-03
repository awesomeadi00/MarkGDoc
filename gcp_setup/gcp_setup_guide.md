# Guide on using Google Cloud Platform with OAuth2

In this guide, you will learn how to setup a project on the Google Cloud Platform (GCP) and how to retrieve your OAuth2 client secrets file which will authenticate your python programs to connect to the API. This way you will be able to create Google Docs from Python, and control what to insert/delete from the Google Docs. 

**Important:** MarkGDoc uses OAuth2 authentication, which means:
- Files will be created in **YOUR** Google Drive (not a service account's Drive)
- Files will use **YOUR** storage quota (typically 15GB free)
- On first run, a browser will open for you to authorize the application
- After authorization, a `token.json` file will be saved for future use

For more information about Google Docs API Requests and how to make them yourself, visit: [Google Docs API Documentation](https://developers.google.com/docs/api/reference/rest)


## Setting up a Project on Google Cloud Platform (GCP) - Retrieving OAuth2 Client Secrets

### 1. Create a New Project on the Google Cloud Console (GCP)

- Click on the following Link: [Google Cloud Console](https://console.cloud.google.com/)

- Create a new project by clicking on the dropdown menu on the top left and then on `New Project`

- Name your project to whatever you like. 

### 2. Enable the Google Docs API

- Firstly make sure your project is appearing on the drop-down menu on the top left (this means you are currently on it)

- On the search bar at the top, search for `Google Docs API` by Google Enterprise API. Then press `Enable API`

- Do the same process for `Google Drive API` by Google Enterprise API

### 3. Configure OAuth Consent Screen

- Click on the Navigation Bar at the very top left and click on `View Products`. 

- Search for `APIs and services` and pin it. It should now appear on your Navigation Bar.

- Click on `APIs and services` and then on `OAuth consent screen`

- Click on `Get Started` if not configured

- Fill in the required information:
  - **App name**: Enter a name (e.g., "MarkGDoc")
  - **User support email**: Select your email address
  - **Developer contact information**: Enter your email address
  - Select **"External"** (unless you have a Google Workspace account, then you can use "Internal")
  - Click **"Create"**

- After creating, you'll see the OAuth overview page. In the left navigation menu, click on **"Audience"**:
  - Look for the **"Test users"** section
  - Click **"Add Users"**
  - Add your own email address (the exact email you'll use to sign in to Google)
  - You can add multiple email addresses if needed
  - Click **"Save"**
  

### 4. Create OAuth2 Client ID Credentials

- Still in `APIs and services`, click on **"Credentials"** in the left sidebar

- Click **"+ CREATE CREDENTIALS"** at the top

- Select **"OAuth client ID"**

- If prompted, select **"Desktop app"** as the application type

- Give it a name (e.g., "MarkGDoc Desktop Client")

- Click **"Create"**

- A dialog will appear with your **Client ID** and **Client Secret**

- Click **"DOWNLOAD JSON"** - this will download your OAuth2 client secrets file

- **Rename this file to `credentials.json`** and save it in your project directory

> **Note:** The downloaded file contains your OAuth2 client credentials. Keep it secure and don't share it publicly.

### 5. First Run Authorization

When you run MarkGDoc for the first time:

1. The program will ask for the path to your `credentials.json` file
2. A browser window will automatically open
3. You'll be asked to sign in to your Google account
4. You'll see a consent screen asking for permissions to access Google Docs and Drive
5. Click **"Allow"** or **"Continue"**
6. The browser will show "The authentication flow has completed"
7. A `token.json` file will be created in the same directory as your `credentials.json`
8. Future runs will use this token automatically (no browser needed)

> **Note:** The `token.json` file stores your authorization. If you delete it, you'll need to authorize again on the next run.


## Creating a Google Doc using the GCP API

In order to create a Google Doc using the API, take a look at this python file example as to how to set it up! 

In here it includes: 

- How to authenticate your google drive api 

- How to create an empty google docs file

- How to set permissions on your google docs file

- How to set up your google docs build service 

> [Google Doc Creation Python File](./gcp_example.py)
