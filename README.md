![Workflow Status](https://github.com/awesomeadi00/MarkGDoc/actions/workflows/ci-cd.yml/badge.svg)
[![PyPI Version](https://badge.fury.io/py/markgdoc.svg)](https://badge.fury.io/py/markgdoc)
# MarkGDoc: Converting Markdown to Google Docs

[MarkGDoc GitHub Link](https://github.com/awesomeadi00/MarkGDoc)

[PyPi Package Link](https://pypi.org/project/markgdoc/)
```
pip install markgdoc
```

Don't you just love to use Markdown to take your notes or store information? But what if you want to convert those notes into a Google Docs File? 

As a programmer and dealing with Google Docs API requests, it can seem frustrating to figure out how to structure your request for inputting content in a Google Docs file properly without errors. 

In this Python Package, you can now convert your markdown files into your very own Google Docs file with ease! We have streamlined every Markdown Syntax to match a properly formatted Google Docs API Request, saving you the nitty gritty time of worrying on how to structure a request, ensuring everything is now automated!


# Key Functions

###  convert_to_google_docs(): 
This is the main function to convert your markdown content into your very own google docs file. This will output your very own **Google Docs URL** to your google docs file: 

```
google_docs_url =  convert_to_google_docs(content_markdown, document_title, docs_service, credentials_file, scopes, debug=False)
```

You need to ensure to pass: 
- `content_markdown` : A string of your markdown content

- `document_title` : A string of the title of your google docs

- `docs_service` : Your google docs build service

- `credentials_file` : The path to your OAuth2 client secrets JSON file 

- `scopes` : Scopes to define the access for the application. 
    
    - You can declare this constant as a default but feel free to add more: 

    ```
    SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    ]
    ```

To learn how to create your own google docs build service and how to setup your own credentials file from Google Cloud Platform, please checkout our tutorial here: 

[Guide on How to Setup Your Google Cloud Console Project](https://github.com/awesomeadi00/MarkGDoc/blob/main/gcp_setup/gcp_setup_guide.md)

--- 

###  create_empty_google_doc(): 
You can even use the `create_empty_google_doc` function if required to help you quickly create an empty google doc: 
```
doc_id, doc_url = create_empty_google_doc(document_title, credentials_file, scopes)
```

You need to ensure to pass: 
- `document_title` : A string of the title of your google docs

- `credentials_file` : The path to your OAuth2 client secrets JSON file 

- `scopes` : Scopes to define the access for the application.

This will output the google docs id as well as the overall complete google docs URL. 

## Specific Google Doc Request Functions:  

In our package we have dissolved your long and complex google docs requests into single line functions catered for every common markdown syntax used: 

### get_header_request(text, level, index, debug=False)

This function will return a google docs request for any header. All you need to do is specify the text you want, the header level (which heading size), and the index at which you would like to place the header in the google docs. 

Example: 
```
header_request = markgdoc.get_header_request("This is a large heading", 1, 1)
```

### get_paragraph_request(text, index, debug=False)

This function will return a google docs request for paragraphs, basically any regular body of text. All you need to do is specify the text you want, and the index at which you would like to place the paragraph in the google docs. 

Example: 
```
paragraph_request = markgdoc.get_paragraph_request("This is a paragraph", 20)
```

### get_horizontal_line_request(index, debug=False)

This function will return a google docs request for horizontal line. All you need to do is insert the index at which you would like to place it. 

Example: 
```
horizontal_line_request = markgdoc.get_horizontal_line_request(10)
```

### get_style_request(text, style, index, debug=False)

This function will return a google docs request for styling a section of your already inserted text. This includes styling marks such as: bolding, italics, strikethrough. You need to specify the text you want to style (text should already be inserted through another request), styling method, index at where the text was inserted in the doc. 

Example: 
```
style_request = markgdoc.get_style_request("This is a styled text", bold, 23)
```

### get_hyperlink_request(text, url, index, debug=False)

This function will return a google docs request for hyperlinks. You need to specify the text (name of the link you want to click), url of the link, index you want to place the link. 

Example: 
```
Link structure: [Google](https://www.google.com/)

link_request = markgdoc.get_hyperlink_request("Google", "https://www.google.com/", 145)
```

### get_unordered_list_request(text, index, debug=False)

This function will return a google docs request for a single bullet point line. You need to spcify the text of the bullet point line and the index you want to place it. 
> - Note 1: This is only one line of the bullet point. To add several bullet points from an overall list, you would probably need to do a for loop with this function. 

Example: 
```
ul_request = markgdoc.get_unordered_list("This is a bullet point", 33)
```

### get_ordered_list_request(text, index, debug=False)

This function will return a google docs request for a single numbered line. You need to spcify the text of the bullet point line and the index you want to place it. 
> - Note 1: This is only one line of the numbered line. To add several numberlines from into an overall numbered line list, you would probably need to do a for loop with this function. 

> - Note 2: The numbered line list should be together with no gaps (empty lines) between the numbered lines to avoid them from being identified as new numbered lists.

Example: 
```
ol_request = markgdoc.get_ordered_list("This is a numbered line", 40)
```

### get_empty_table_request(rows, cols, index, debug=False)

This function will return a google docs request to create an empty table on the google docs. You need to specify the number of rows and columns and the index to place it on. 

Example: 
```
table_request = markgdoc.get_empty_table_request(2, 3, 39)
```


### get_table_content_request(table_data, index, debug=False):

This function will return a google docs request to insert your table content into an empty table in the google docs. You need to specify a 2D list vector of your table data in the form of `table_data = [rows][column]` as well as the index to place it on.  


Example: 
```
table_content_request = markgdoc.get_table_content_request(table_data, 255)
```


# Running the __main__.py file 

### **Important Note:**
Before you go ahead and run this program, please make sure that: 
- You have setup a Google Cloud Project with Google Docs API enabled. 

- You have a valid OAuth2 `credentials.json` client secrets file from your Google Cloud Console Project. 

The above steps are required for you to run this main as these are the steps needed to connect to the API and create a Google Docs through Python. 

**OAuth2 Authentication:**
- MarkGDoc uses OAuth2 authentication, which means files will be created in **YOUR** Google Drive
- Files will use **YOUR** storage quota (typically 15GB free)
- On first run, a browser will open for you to authorize the application
- After authorization, a `token.json` file will be saved for future use

If you don't have any of these setup, checkout our documentation on how to setup a Google Cloud Console Project: [Guide on How to Setup Your Google Cloud Console Project](https://github.com/awesomeadi00/MarkGDoc/blob/main/gcp_setup/gcp_setup_guide.md)

Once properly setup, you can run the command: 

```shell
python -m markgdoc

# Debug mode
python -m markgdoc --debug
```

If installed properly, you can just run it by itself: 
```shell
markgdoc 

# Debug mode
markgdoc --debug
```


# Contributing

Contributions are definitely accepted and we are open to growing this package. By participating in this project, you agree to abide by the [code of conduct](https://github.com/eads/generic-code-of-conduct.git).

### Setting Up the Development Environment

1. **Clone the repository**:

    Use the following command to clone the repository:

    ```shell
    git clone https://github.com/awesomeadi00/MarkGDoc.git
    ```

2. **Navigate to the project directory**:

    Change into the cloned directory:

    ```shell
    cd MarkGDoc
    ```

3. **Install pipenv**:

    First make sure you have pipenv installed

    ```shell    
    pip install pipenv
    ```

4. **Install Dependencies**: 
   
    Install all dependencies (including dev dependencies):
    
    ```shell
    pipenv install --dev
    ```
    
    > Note: pipenv will automatically create a virtual environment (`.venv`) and lock the Pipfile for you. You don't need to do this manually.

5. **Install the package in editable mode**:

    This step is crucial! It allows you to test your local changes immediately:
    
    ```shell
    pipenv install -e .
    ```
    
    This installs your local package code so that when you run `python -m markgdoc`, it uses your local changes instead of the installed version.

6. **Activate the virtual environment** (optional but recommended):

    Enter the virtual environment using:

    ```shell
    pipenv shell
    ```

    > **Note:** If you skip this step, you'll need to prefix commands with `pipenv run` (e.g., `pipenv run python -m markgdoc` instead of `python -m markgdoc`).

7. **Make your changes**:

    Make the changes you want to contribute to the project.

8. **Run tests**:

    Ensure your changes pass all tests using pytest:

    ```shell
    pipenv run python -m pytest
    ```

    > **Note:** If you activated the virtual environment in step 6, you can use `python -m pytest` directly.

9. **Test your changes locally**:

    Test that your changes work by running the main program:

    ```shell
    python -m markgdoc
    ```

    Or with debug mode:

    ```shell
    python -m markgdoc --debug
    ```

    > **Note:** If you didn't activate the virtual environment in step 6, use `pipenv run python -m markgdoc` instead.

10. **Submit a Pull Request**:

    After making your changes and verifying the functionality, commit your changes and push your branch to GitHub. Then, submit a pull request to the main branch for review.

### Reporting Bugs

Report bugs at [Issues](https://github.com/awesomeadi00/Markdoc/issues).

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Submitting Enhancements

If you're proposing enhancements or new features:

* Open a new issue [here](https://github.com/awesomeadi00/Markdoc/issues), describing the enhancement.
* Include the 'enhancement' label on the issue.

Thank you for your interest!
