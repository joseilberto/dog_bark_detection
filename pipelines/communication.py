from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename


import email
import smtplib
import ssl


def create_body(files, message):
    """
        Create the body of the e-mail from the keys in message and 
    """
    pattern_message = message["pattern"]
    bark_messages = message["body_start"]
    for file in files:
        filename = basename(file)
        name, date, hour, minute, seconds = "".join(filename.split(".")[0]).split("_")
        bark_messages += pattern_message(hour, minute, seconds, date)
    return bark_messages + message["body_end"] + message["signature"]


def send_files(files, sender, receiver, message):
    """
        Parameters:
        files (list of strings): All the files that will be sent to the receiver.
        sender (dict): Dictionary with the data from sender (email, password, port and smtp server).
        receiver (dict): Dictionary with the data from receiver (email).
        message (dict): Dict containing the data to be used in the body of the text.
    """
    context = ssl.create_default_context()
    email_msg = MIMEMultipart()
    
    email_msg["From"] = sender["email"]
    email_msg["To"] = receiver["email"]
    email_msg["Subject"] = message["subject"]    

    email_msg.attach(MIMEText(message["body"], "plain"))
    
    for file in files:
        with open(file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-disposition", 
                        f"attachment; filename= {basename(file)}",)
        email_msg.attach(part)
    text = email_msg.as_string()    
    
    with smtplib.SMTP_SSL(sender["smtp_server"], sender["port"], 
                            context = context) as server:
        server.login(sender["email"], sender["password"])
        server.sendmail(sender["email"], receiver["email"], text)
    print("{} File(s) sent from {} to {}".format(len(files), sender["email"], receiver["email"]))




