![Workflow Status](https://github.com/awesomeadi00/MarkGDoc/actions/workflows/ci-cd.yml/badge.svg)

# MarkGDoc: Converting Markdown to Google Docs

[MarkGDoc GitHub Link](https://github.com/awesomeadi00/MarkGDoc)

```
pip install markgdoc
```

Don't you just love to use Markdown to take your notes or store information? But what if you want to convert those notes into a Google Docs File? 

As a programmer and dealing with Google Docs API requests, it can seem frustrating to figure out how to structure your request for inputting content in a Google Docs file properly without errors. 

In this Python Package, you can now convert your markdown files into your very own Google Docs file with ease! We have streamlined every Markdown Syntax to match a properly formatted Google Docs API Request, saving you the nitty gritty time of worrying on how to structure a request, ensuring everything is now automated!


# Key Features

# Running the __main__.py file 

### **Important Note:**
Before you go ahead and run your this program, please make sure that: 
- You have setup a Google Cloud Project with Google Docs API enabled. 

- You have a valid and active `credentials.json` key for your Google Cloud Console Project. 

The above steps are required for you to run this main as these are the steps needed to connect to the API and create a Google Docs through Python. 

If you don't have any of these setup, checkout our documentation on how to setup a a Google Cloud Console Project: [Guide on How to Setup Your Google Cloud Console Project](./gcp_setup/gcp_setup_guide.md)

Once properly setup, you can run the command: 

```
python -m src.markgdoc
```

Additionally you can also run the program as the following for Debugging Print Statements of all the requests to show in your terminal
```
python -m src.markgdoc --debug
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
    cd markgdoc
    ```

3. **Install pipenv**:

    First make sure you have pipenv installed

    ```shell    
    pip install pipenv
    ```

4. **Locking Pipfile if Pipfile.lock not present**:

   If the Pipfile.lock file is not present or updated, use the following command to lock the pipfile

    ```shell
    pipenv lock
    ```

5. **Install Dependencies**: 
   
    In order to install the dependencies, first create an empty folder and rename it as `.venv`. After this step is done, then you can install your dependencies through the following command: 
    
    ```shell
    pipenv install
    ```
    > Note that `pipenv install --dev` install dev-packages as well.

6. **Activate the virtual environment**:

    Enter the virtual environment using:

    ```shell
    pipenv shell
    ```

7. **Make your changes**:

    Make the changes you want to contribute to the project.

8. **Run tests**:

    Ensure your changes pass all tests using pytest:

    ```shell
    pipenv run python -m pytest
    ```

8. **Submit a Pull Request**:

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
