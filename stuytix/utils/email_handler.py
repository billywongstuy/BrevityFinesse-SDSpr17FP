from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from httplib2 import Http

from apiclient import errors
from apiclient.discovery import build


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

DIR = os.path.dirname(__file__) or "."
DIR += "/"


SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = DIR + 'client_secret.json'
APPLICATION_NAME = 'StuyTix'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    #credential_dir = os.path.join(home_dir, '.credentials')
    #credential_dir = os.path.join(os.getcwd(), '.credentials')
    credential_dir = os.path.join(DIR, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                       'stuytix-credentials.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
            print ('Storing credentials to ' + credential_path)
    return credentials


def create_message(sender, to, subject, message_text, cc=None):
    """Create a message for an email.

    Args:
sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64 encoded email object.
    """
    message = MIMEText(message_text,'html')
    #message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if cc != None:
        message['cc'] = cc
    #return {'raw': base64.b64encode(message.as_string())}
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                 .execute())
        print ('Message Id: %s' % message['id'])
        return message
    except errors.HttpError, error:
        print ('An error occurred: %s' % error)



credentials = get_credentials()
service = build('gmail', 'v1', http=credentials.authorize(Http()))


# CC DOESN'T WORK


def message_helper(sender, recipient, subj, body, serv, cc=None):
    message = create_message(sender, recipient, subj, body, cc)
    #print ('done creating')
    send = send_message(serv, sender, message)
    #print ('done sending')
    return send

#send to one user, one cc
#args: recipient is string, cc is string
def send_msg_one(recipient,subj,body, cc=None):
    if recipient == None:
        return 'Error: Email is not valid'
    return message_helper('me', recipient, subj, body, service, cc)

#send to 1+ user, 1+ cc
#args: recipients is list, cc is list
def send_msg_multi(recipients,subj,body,cc=[None]):
    if len(recipients) < 1:
        return 'No recipients specified'
    if recipients[0] == None:
        return 'Error: Email is not valid'
    if len(recipients) > 1:
        r = ", ".join(recipients)
    else:
        r = recipients[0]
    if len(cc) > 1:
        cc = ", ".join(cc)
    else:
        cc = cc[0]
    return message_helper('me', r, subj, body, service, cc)


def get_update_body(t_name, full_status, urgency, key):
    return '''
%s,

<p>
Your ticket status has changed to %s <br>
Urgency: %s
</p>


<p>
Click <a href="stuytix.stuycs.org/ticket/%d">here</a> to view the whole ticket
</p>

<p>
The Tech Services Department
</p>
''' % (t_name, full_status, urgency, key)



def get_new_tix_body(issue, room, teacher, key):
    return '''
Hello techs,

<p>
A new ticket has been submitted!
</p>

<p>
Issue: %s <br>
Room: %d <br>
Teacher: %s
</p>

<p>
Click <a href="stuytix.stuycs.org/ticket/%d">here</a> to view the whole ticket
</p>

<p>
The Tech Services Department
</p>
''' % (issue, room, teacher, key)



### CHANGE THE LINK 
## 127.0.0.1:5000/ticket/%d
