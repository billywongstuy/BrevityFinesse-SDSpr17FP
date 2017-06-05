# BrevityFinesse-SDSpr17FP

## Project Outline

Stuytix is a ticketing system created for the tech services department. With this service, teachers can log ITS requests online, giving notifications to our tech staff who have options to respond via the app. This gives us a simple and secure way of communicating tech issues without wasting time with unnecessary calls.

## Contributors

* Julian Atkin
* Yuxuan(Yuki) Chen
* Bily Wong
* Henry Zhang

## Prerequisites

* Python 2.6 or greater.
* The pip package management tool.
* Access to the internet and a web browser.
* A Google account with Gmail enabled.

## Setup

Step 1: Turn on the Gmail API

a. Use https://console.developers.google.com/flows/enableapi?apiid=gmail to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.

b. On the Add credentials to your project page, click the Cancel button.

c. At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.

d. Select the Credentials tab, click the Create credentials button and select OAuth client ID.

e. Select the application type Other, enter the name "Gmail API Quickstart", and click the Create button.

f. Click OK to dismiss the resulting dialog.

g. Click the file_download (Download JSON) button to the right of the client ID.

h. Move this file to the root directory and rename it client_secret.json.


Step 2: Install packages using pip

* Run the command to install google-api-client:
    pip install --upgrade google-api-python-client

* Run the command to install apscheduler:
    pip install apscheduler


Step 3

* Run the command:
      python app.py

* On your first instance of running the file on a computer:
  - A window will open, asking for Gmail sending privileges
  - Accept the prompt with the email used in Step 1
  - In terminal, a prompt to setup a superadmin will appear
  - After creating a superadmin, the application is ready to go!!!
