import os
import argparse
from pathlib import Path
from googleapiclient.discovery import build
from colorama import init, Fore, Style
from . import markgdoc

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Initialization for this global variable constant. This is the path to your OAuth2 client secrets file
CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]
MARKDOWN_FILES_COUNT = 4


def detect_credentials_file(debug=False):
    """
    Automatically detect credentials.json file in common locations.
    Returns the path if found, None otherwise.
    
    Priority order:
    1. Current working directory: ./credentials.json
    2. Environment variable: MARKGDOC_CREDENTIALS_PATH
    3. Home directory: ~/.markgdoc/credentials.json
    """
    # 1. Check current working directory
    current_dir_creds = os.path.join(os.getcwd(), "credentials.json")
    if os.path.isfile(current_dir_creds):
        if debug:
            print(f"{Fore.GREEN}[DEBUG] Found credentials.json in current directory{Style.RESET_ALL}")
        return current_dir_creds
    
    # 2. Check environment variable
    env_creds_path = os.environ.get("MARKGDOC_CREDENTIALS_PATH")
    if env_creds_path and os.path.isfile(env_creds_path):
        if debug:
            print(f"{Fore.GREEN}[DEBUG] Found credentials.json from environment variable{Style.RESET_ALL}")
        return env_creds_path
    
    # 3. Check home directory (~/.markgdoc/credentials.json)
    home_dir = Path.home()
    home_creds = home_dir / ".markgdoc" / "credentials.json"
    if home_creds.is_file():
        if debug:
            print(f"{Fore.GREEN}[DEBUG] Found credentials.json in home directory{Style.RESET_ALL}")
        return str(home_creds)
    
    # Not found
    return None


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
    print(f"{Fore.YELLOW}Note: MarkGDoc uses OAuth2 authentication.{Style.RESET_ALL}")
    print("Files will be created in YOUR Google Drive using YOUR storage quota.")
    print("On first run, a browser will open for you to authorize the application.")
    print("For more information on how to get your OAuth2 client secrets file, please checkout our documentation: https://github.com/awesomeadi00/MarkGDoc/blob/main/gcp_setup/gcp_setup_guide.md\n")
    
    # Try to auto-detect credentials.json file
    global CLIENT_SECRETS_FILE
    detected_creds = detect_credentials_file(debug=debug)
    
    if detected_creds:
        CLIENT_SECRETS_FILE = detected_creds
        # Show which location was used
        if detected_creds == os.path.join(os.getcwd(), "credentials.json"):
            print(f"{Fore.GREEN}Using credentials.json from current directory{Style.RESET_ALL}\n")
        elif detected_creds == os.environ.get("MARKGDOC_CREDENTIALS_PATH"):
            print(f"{Fore.GREEN}Using credentials.json from environment variable (MARKGDOC_CREDENTIALS_PATH){Style.RESET_ALL}\n")
        else:
            print(f"{Fore.GREEN}Using credentials.json from {detected_creds}{Style.RESET_ALL}\n")
    else:
        # No credentials found, prompt user
        credentials_path_input = input("Please provide the path for where your OAuth2 client secrets file is: ")

        # Check if the provided path is valid and accessible
        if os.path.isfile(credentials_path_input):
            CLIENT_SECRETS_FILE = credentials_path_input
            print(f"{Fore.GREEN}Client secrets file found and set successfully!{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}Error: The file path provided does not exist or is not a valid file.{Style.RESET_ALL}")
            exit(-1) 
    
    # Determine token file location (store in same directory as credentials)
    token_file = os.path.join(os.path.dirname(CLIENT_SECRETS_FILE), "token.json")
    
    print("Building...")
    print(f"{Fore.YELLOW}If this is your first time, a browser window will open for authorization...{Style.RESET_ALL}\n")

    # Attempt to build the Google Docs service using OAuth2
    try:
        from .markgdoc import get_oauth2_credentials
        creds = get_oauth2_credentials(CLIENT_SECRETS_FILE, token_file, SCOPES, debug=debug)
        docs_service = build("docs", "v1", credentials=creds)
        print(f"{Fore.GREEN}Google Docs Service Initialized Successfully!{Style.RESET_ALL}\n")
    except FileNotFoundError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        print(f"\nPlease download the OAuth2 client secrets file from Google Cloud Console.")
        print(f"See the setup guide for instructions: https://github.com/awesomeadi00/MarkGDoc/blob/main/gcp_setup/gcp_setup_guide.md")
        exit(-1)
    except Exception as e:
        print(f"{Fore.RED}Error: Google Docs service initialization failed. {e}{Style.RESET_ALL}")
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

                print(f"{Fore.YELLOW}Conversion Started! Markdown to Google Doc!{Style.RESET_ALL}")
                doc_url = markgdoc.convert_to_google_docs(md_content, document_title, docs_service, credentials_file=CLIENT_SECRETS_FILE, scopes=SCOPES, token_file=token_file, debug=debug)
                
                # if not debug: 
                print(f"{Fore.GREEN}Google Doc Link:{Style.RESET_ALL} {doc_url}\n")

            else:
                print(f"{Fore.RED}Error: The file path provided does not exist or is not a valid file.{Style.RESET_ALL}")
        
        # Example File from Local Project Directory
        elif user_input == "2":
            print(f"We currently have {MARKDOWN_FILES_COUNT} markdown file examples in our system!")
            md_example_fileno = input(f"Please input any number from 1-{MARKDOWN_FILES_COUNT} and we will send the Google Docs Link of that example: ")

            while(int(md_example_fileno) > MARKDOWN_FILES_COUNT or int(md_example_fileno) <= 0): 
                print(f"{Fore.RED}Incorrect Input!{Style.RESET_ALL}")
                md_example_fileno = input(f"Please input any number from 1-{MARKDOWN_FILES_COUNT} and we will send the Google Docs Link of that example: ")

            md_example_file = f"md_ex{md_example_fileno}"
            md_inputfile = os.path.join(os.path.dirname(__file__), 'example_markdown_files', f"{md_example_file}.md")

            try: 
                # Read the content of the markdown file
                with open(md_inputfile, 'r') as file:
                    md_content = file.read()
            except FileNotFoundError as e: 
                print(f"{Fore.RED}File could not be opened: {e}{Style.RESET_ALL}")
                exit(-1)

            document_title = "Example Markdown File"
            print(f"{Fore.YELLOW}Conversion Started! Markdown to Google Doc!{Style.RESET_ALL}")
            doc_url = markgdoc.convert_to_google_docs(md_content, document_title, docs_service, credentials_file=CLIENT_SECRETS_FILE, scopes=SCOPES, token_file=token_file, debug=debug)
            
            # if not debug: 
            print(f"{Fore.GREEN}Google Doc Link:{Style.RESET_ALL} {doc_url}\n")

        elif user_input == "q" or user_input == "Q":
            break
        
        else:
            print(f"\n{Fore.RED}Invalid Response. Please input one of the numbers for that request.{Style.RESET_ALL}")
        
        while True:
            user_cont = input("Would you like to continue? (y/n): ")
            if user_cont in ["y", "n"]:
                break
            else:
                print(f"\n{Fore.RED}Invalid Input.{Style.RESET_ALL}")

        if user_cont == "n" or user_cont == "q" or user_cont == "Q":
            break


def cli():
    """Entry point for the console script. Handles command-line arguments."""
    parser = argparse.ArgumentParser(description="Run MarkGDoc with Optional Debugging")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    args = parser.parse_args()
    main(debug=args.debug)


if __name__ == "__main__":
    cli()