# Guide on using Google Cloud Platform

In this guide, you will learn how to setup a project on the Google Cloud Platform (GCP) and how to retrieve your credentials.json file which will authenticate your python programs to connect to the API. This way you will be able to create Google Docs from Python, and control what to insert/delete from the Google Docs. 

For more information about Google Docs API Requests and how to make them yourself, visit: [Google Docs API Documentation](https://developers.google.com/docs/api/reference/rest)


## Setting up a Project on Google Cloud Platform (GCP) - Retrieving credentials.json file

### 1. Create a New Project on the Google Cloud Console (GCP)

- Click on the following Link: [Google Cloud Console]("https://console.cloud.google.com/")

- Create a new projecet by clicking on the dropdown menu on the top left and then on `New Project`

- Name your project to whatever you like. 

### 2. Enable the Google Docs API

- Firstly make sure your project is appearing on the drop-down menu on the top left (this means you are currently on it)

- On the search bar at the top, search for `Google Docs API` by Google Enterprise API. Then press `Enable API`

- Do the same process for `Google Drive API` by Google Enterprise API

### 3. Create a Service Account

- Click on the Navigation Bar at the very top left and click on `View Products`. 

- Search for `APIs and services` as well as `IAM and admin` and pin both of these products. These two should now appear on your Navigation Bar.

- Click on `APIs and services` and then on `Credentials`

- At the bottom where it says Service Accounts, on the right side click on `Manage Service Accounts`

- Create a new Service Account by clicking on the button at the very top. You can choose the name and access rights for this project. 

### 4. Retrieve credentials.json file

- Once you have created a new service account, it should show under `Service Accounts` of the `IAM and admin` tab. 

- Click on the three-dots on the right side of this service account labeled as `Actions`

- Click on `Manage Keys`

- Click on `Add Key` > `Create Key` > `JSON Format` and then Create. 

- This will download your **`credentials.json`** file onto your Downloads. Simply add this file onto your project directory to connect to this project on the GCP.


## Creating a Google Doc using the GCP API

In order to create a Google Doc using the API, take a look at this python file example as to how to set it up! 
> [Google Doc Creation Python File](./gcp_example.py)