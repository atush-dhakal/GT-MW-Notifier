# Setup

## Create a virtual environment
Create a virtual environment for the python project. Run the following:
```
    python -m venv venv
    ./venv/Scripts/activate
```
This simplies the need to get the dependencies for the project.


## Install dependencies
Simply run the following:
```
    pip install -r requirements.txt
```
This will install all the dependencies used in the project. Make sure your have the `venv` enabled. This file is required by GCP for deploying.

## Adding configs
We will be adding any configuration values and API keys in `config.ini` file.

Copy `config.example.ini` to a new file `config.ini` if using for the first time.
Simple run the following command:
    `cp config.example.ini config.ini`

After creating this new file, there may be missing API keys. Contact the admins to get the API keys.

If you are adding any new values to your `config.ini` file, make sure to add it to `config.example.ini` as well and commit those changes so other developer can add those new config keys. However, do not save the API keys in `config.example.ini` file. Instead put a placeholder for the API keys.

## Version 1.0

## Features:
- Stores user email using Mailchimp
- Uses Beautiful Soup to scrape job postings on https://studentcenter.gatech.edu/campus-jobs
- Stores new job postings on remote Mongo DB
- Uses GMAIL API to send email notifications with new job posting


