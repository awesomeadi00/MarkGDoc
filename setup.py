from setuptools import setup, find_packages

setup(
    name='markgdoc',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client",
    ]
)