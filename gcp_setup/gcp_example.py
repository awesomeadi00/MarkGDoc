from google.oauth2 import service_account
from googleapiclient.discovery import build

# ===========================================================================================================================
# This Python File serves as an example of how to create a Google Doc using your the APIs setup on your Google Cloud Platform 
# In this example, you will learn how to: 
# - Setup your Google Docs Service
# - Retrieve your Google Docs ID
# ===========================================================================================================================

# Path to the service account key file and scopes
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]

def authenticate_google_drive():
    """
    This function is used to authenticate your connection to your google drive 
    through your Google Drive API setup on your GCP Project
    """
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)


def create_empty_google_doc(document_title):
    """
    This function is used to create an empty google doc file and get the doc_id.
    - It requires a str input of a document title
    - The output will be the doc_id and the doc_url which you can access on a web broswer
    """

    # Authenticates a google drive and setups metadata
    drive_service = authenticate_google_drive()
    doc_metadata = {
        "name": document_title,
        "mimeType": "application/vnd.google-apps.document",
    }

    # Creates the google doc and retrieves the google doc id
    doc = drive_service.files().create(body=doc_metadata).execute()
    doc_id = doc["id"]

    # Set permissions to allow user to view and edit immediately
    permission_body = {"type": "anyone", "role": "writer"}
    drive_service.permissions().create(fileId=doc_id, body=permission_body).execute()

    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
    return doc_id, doc_url


def generate_google_docs():
    """
    This function is an example of how you can instantiate your create_empty_google_docs function
    - You can retrieve the doc_id
    
    This also shows you how to instantiate your docs_service build. 
    - This is important for making batchUpdate requests to the API to insert content into your Google Docs
    - In essence, this is important for the Python Package (MarkGDoc) to operate effectively
    """
    document_title = "Example Google Doc"
    doc_id, doc_url = create_empty_google_doc(document_title)

    # # This is how you build the google docs service build
    # docs_service = build(
    #     "docs",
    #     "v1",
    #     credentials=service_account.Credentials.from_service_account_file(
    #         SERVICE_ACCOUNT_FILE, scopes=SCOPES
    #     ),
    # )

    # # This is an example function which would need to send Google Doc Requests. In order to do this, you need to send both these variables
    # example_function(docs_service, doc_id)   
    return doc_url