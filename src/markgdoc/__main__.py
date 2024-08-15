import os
import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from . import markgdoc

# Initialization for this global variable constant. This is the path to your credentials.json file, you can edit it to whatever path you want 
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]
MARKDOWN_FILES_COUNT = 4


def main(debug=False):
    print("\n")
    print("███    ███  █████  ██████  ██   ██  ██████  ██████   ██████   ██████ ")
    print("████  ████ ██   ██ ██   ██ ██  ██  ██       ██   ██ ██    ██ ██      ")
    print("██ ████ ██ ███████ ██████  █████   ██   ███ ██   ██ ██    ██ ██      ")
    print("██  ██  ██ ██   ██ ██   ██ ██  ██  ██    ██ ██   ██ ██    ██ ██      ")
    print("██      ██ ██   ██ ██   ██ ██   ██  ██████  ██████   ██████   ██████ ")
    print("                                                                     ")
    print("Welcome to MarkGDoc! A Package to convert your Markdown Syntax to your very own Google Docs!\n")
    
    if(debug):
        print("------ DEBUG MODE ON ------\n")

    print("First, let's set you up!")
    credentials_path_input = input("Please provide the path for where your credentials.json file is: ")

    # Check if the provided path is valid and accessible
    if os.path.isfile(credentials_path_input):
        global SERVICE_ACCOUNT_FILE
        SERVICE_ACCOUNT_FILE = credentials_path_input
        print("Credentials file found and set successfully!\n")
    else:
        print("Error: The file path provided does not exist or is not a valid file.")
        exit(-1) 
    
    print("Building...")

    # Attempt to build the Google Docs service with the updated SERVICE ACCOUNT FILE
    try:
        docs_service = build(
            "docs",
            "v1",
            credentials=service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            ),
        )
        print("Google Docs Service Initialized Successfully!\n")
    except Exception as e:
        print(f"Error: Google Docs service initialization failed. {e}")
        exit(-1) 
    
    print("============================================ MARKGDOC MENU ============================================")
    while True: 
        print("What would you like to do today? Please type the appropriate number for the request.")
        print("1. Convert your own Markdown file to a Google Docs file")
        print("2. Convert one of our example Markdown Files to a Google Docs file")
        print("!! Type Q to quit !!\n")

        print("Enter your choice: ")
        user_input = input("> ")

        # User's Markdown File
        if user_input == "1":
            document_title = input("Please input the name you would like to name your Google Docs: ")

            markdownfile_path = input("Please enter the path for your markdown file: ")
            if os.path.isfile(markdownfile_path):                
                with open(markdownfile_path, 'r') as file:
                    md_content = file.read()

                print("Converting your Markdown to a Google Doc!")
                doc_url = markgdoc.convert_to_google_docs(md_content, document_title, docs_service, credentials_file=SERVICE_ACCOUNT_FILE, scopes=SCOPES, debug=debug)
                
                if not debug: 
                    print(f"Google Doc Link: {doc_url}\n")

            else:
                print("Error: The file path provided does not exist or is not a valid file.")
        
        # Example File from Local Project Directory
        elif user_input == "2":
            print(f"We currently have {MARKDOWN_FILES_COUNT} markdown file examples in our system!")
            md_example_fileno = input(f"Please input any number from 1-{MARKDOWN_FILES_COUNT} and we will send the Google Docs Link of that example: ")

            while(int(md_example_fileno) > MARKDOWN_FILES_COUNT or int(md_example_fileno) <= 0): 
                print("Incorrect Input!")
                md_example_fileno = input(f"Please input any number from 1-{MARKDOWN_FILES_COUNT} and we will send the Google Docs Link of that example: ")

            md_example_file = f"md_ex{md_example_fileno}"
            md_inputfile = os.path.join(os.path.dirname(__file__), 'example_markdown_files', f"{md_example_file}.md")

            try: 
                # Read the content of the markdown file
                with open(md_inputfile, 'r') as file:
                    md_content = file.read()
            except FileNotFoundError as e: 
                print(f"File could not be opened: {e}")
                exit(-1)

            document_title = "Example Markdown File"
            print("Converting your Markdown to a Google Doc!")
            doc_url = markgdoc.convert_to_google_docs(md_content, document_title, docs_service, credentials_file=SERVICE_ACCOUNT_FILE, scopes=SCOPES, debug=debug)
            if not debug: 
                print(f"Google Doc Link: {doc_url}\n")

        elif user_input == "q" or user_input == "Q":
            break
        
        else:
            print("\nInvalid Response. Please input one of the numbers for that request.")
        
        while True:
            user_cont = input("Would you like to continue? (y/n): ")
            if user_cont in ["y", "n"]:
                break
            else:
                print("\nInvalid Input.")

        if user_cont == "n" or user_cont == "q" or user_cont == "Q":
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MarkGDoc with Optional Debugging")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    args = parser.parse_args()
    main(debug=args.debug)