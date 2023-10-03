from email.mime.text import MIMEText
from time import sleep
import sys
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
import os
import time

ID_COUNTER = dict()

def add(x:int):
    try:
        file = open("counter.txt", "r")
        num = int(file.read().split("\n")[0])
        num += x
    except Exception as E:
        num = x
    print(num, file=open("counter.txt", "w"))

def printf(*args):
    print(*args, file=open("All_Print_Logs.txt", "a"))

def verifying2(recipient_email, id_num):

    to = recipient_email
    subject = "Test email"
    message_text = "This is a test email."

    # Set up the Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    # Load credentials
    creds = None
    if os.path.exists(f'Credentials/cred{id_num}.json'):
        creds = Credentials.from_authorized_user_file(
            f'Credentials/cred{id_num}.json', SCOPES)

    # Create message object
    msg = MIMEMultipart()
    msg['to'] = to
    msg['subject'] = subject

    # Create text part
    text_part = MIMEText(message_text, 'plain')
    msg.attach(text_part)

    try:
        service = build('gmail', 'v1', credentials=creds)
        raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        send_message = service.users().messages().send(userId='me', body={'raw': raw_msg}).execute()

    except HttpError as error:
        
        if "Invalid To header" in str(error):
            printf(f"TIME:: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}", "HTTP 400 --- ", to, f"FROM ID => {id_num}")
        else:
            printf(f"TIME:: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}", "---", error, f"FROM ID => {id_num}")
        return False
    
    except Exception as E:

        if 'invalid_grant: Bad Request' in str(E):
            printf(f"TIME:: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}", "400 :::: ", to, f"FROM ID= > {id_num}")

        else:
            printf(f"TIME:: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}", "___> ", E, f"FROM ID= > {id_num}")
        return False
    
    add(1)
    sleep(0.1)
    knkt = receive(recipient_email, 11, id_num)
    return knkt

def receive(recipient_email, count, id_num):
    sleep(1)

    if count == 0:
        current_time = time.time()
        # Convert the current time to a human-readable format
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
        printf(f"{recipient_email}: EXIST {formatted_time} FROM ID:::: {id_num}")
        return True
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    # Load the credentials
    creds = None
    if os.path.exists(f'Credentials/cred{id_num}.json'):
        creds = Credentials.from_authorized_user_file(f'Credentials/cred{id_num}.json', SCOPES)

    # Build the Gmail API client
    service = build('gmail', 'v1', credentials=creds)

    # Recursive function to extract the message body from a payload
    def get_message_body(payload):
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    body = part['body']
                    data = body.get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
                elif part['mimeType'] == 'multipart/alternative':
                    return get_message_body(part)
                elif part['mimeType'] == 'multipart/mixed':
                    return get_message_body(part)
                else:
                    return get_message_body(part)
        else:
            body = payload['body']
            data = body.get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')
    # Fetch the latest message
    try:
        response = service.users().messages().list(
            userId='me', q='is:inbox', maxResults=1).execute()
        message = None
        if 'messages' in response:
            message = response['messages'][0]
            msg = service.users().messages().get(
                userId='me', id=message['id']).execute()
            payload = msg['payload']
            content = get_message_body(payload)
            mnEmail = recipient_email
            if content.splitlines()[0:1][0] == "" or content.splitlines()[0:1][0] == "\n" or content.splitlines()[0:1][0] == " ":
                pass
            else:
                # printf(content.splitlines()[0:1][0], f" FROM ID=== {id_num}")
                pass
            if "You have reached a limit for sending mail" in str(content):
                # printf("You have reached a limit for sending mail. Your message was not sent.")
                raise Exception("You have reached a limit for sending mail. Your message was not sent.")
            if mnEmail in content:
                current_time = time.time()
                # Convert the current time to a human-readable format
                formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                printf(f'{mnEmail} == Not EXIST {formatted_time} FROM ID==> {id_num}')
                return False
            else:
                return receive(recipient_email, count-1, id_num)
    except HttpError as error:
        printf('An error occurred: %s' % error, f"FROM ID==> {id_num}")

def getVars(index):
    data = []
    with open('patterns.txt', 'r') as f:
        for l in f:
            data.append(l.split("\n")[0])
    
    return data[index]
        
def PatternCheck(first_name, last_name, domain,_idnum):
    global ID_COUNTER
  
    if "//" in domain:
        domain = ".".join(" ".join(domain.split("//")[1:]).replace("/","").replace("www.","").replace("-", "").split(".")[0:2])
    else:
        domain = domain.replace("www.","").replace("-", "").replace("/", "")



    for i in range(16):
        
        ptrn = getVars(i).replace('firstname', first_name).replace('lastname', last_name).replace('firstinitial', first_name[0]).replace('lastinitial', last_name[0]).lower()
        email = f'{ptrn}@{domain}'
            
        if _idnum not in ID_COUNTER.keys(): ID_COUNTER[_idnum] = 1
        else: ID_COUNTER[_idnum] += 1
        
        try:
            if verifying2(email,_idnum):
                print(ID_COUNTER, file=open("credentials_log.txt", "w"))
                return (getVars(i), email, ID_COUNTER[_idnum])
            
        except Exception as e:
            printf(sys.exc_info()[0].__traceback__, e)
            raise Exception("Email Verification Error", str(e))
        
        print(ID_COUNTER, file=open("credentials_log.txt", "w"))
    return (None, None, ID_COUNTER[_idnum])



if __name__ == "__main__":
    PatternCheck("savya", "sachi","acadecraft.net/", 50)