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

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-quickstart.json')

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
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  if cc != None:
      message['cc'] = cc
  return {'raw': base64.b64encode(message.as_string())}


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

def message_helper(sender, recipient, subj, body, serv, cc=None):
    message = create_message(sender, recipient, subj, body, cc)
    send = send_message(serv, sender, message)
    return send

#send to one user, one cc
#args: recipient is string, cc is string
def send_msg_one(recipient,subj,body, cc=None):
    if recipient == None:
        return 'Error: Email is not valid'
    return message_helper('me', recipient, subj, body, service, cc)

#send to 1+ user, 1+ cc
#args: recipients is list, cc is list
def send_msg_multi(recipients,subj,body,cc=None):
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


def getUpdateBody(t_name, full_status, urgency):
    return '''
    %s,

    Your ticket status has changed to %s

    The Technical Issues Department
    ''' % (t_name, full_status)

#me = 'me'
#rec = ['bwong5@stuy.edu','billywong118@gmail.com']
#subj2 = 'Hello World!'
#body2 = 'Are you doing well today?\nI\'m having a fine day\n\nGoodbye!'

#send_msg_one(rec[0],subj2,body2,rec[1])
#send_msg_multi([rec[0]],subj2,body2,[rec[1]])

