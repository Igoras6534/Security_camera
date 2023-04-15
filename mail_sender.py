import smtplib
import ssl
import os
from email.message import EmailMessage


class EmailSender():
    def __init__(self):
        self.smtp_port = 465  # Standard secure SMTP port
        self.smtp_server = "smtp.gmail.com" # Google SMTP Server

        self.pswd=os.environ.get('SMTP_PASSW') #SMTP email adress password
        self.email_from= os.environ.get('SMTP_MAIL')# SMTP email adress
        
        self.simple_email_context = ssl.create_default_context()

    def send_email(self, email_to):
        message= "Someone has appeared on your camera. "
        subject = 'Security camera started recording!'
        msg = EmailMessage()
        msg['From'] = self.email_from
        msg['To'] = email_to
        msg['Subject'] = subject
        msg.set_content(message)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_from,self.pswd)
            smtp.sendmail(self.email_from, email_to, msg.as_string()) 
            print("Email has been successfully sended :-)")


    def send_video(self,email_to,path):
        message= "Here is a video of the latest activity."
        subject = 'Security camera has stopped recording.'
        msg = EmailMessage()
        msg['From'] = self.email_from
        msg['To'] = email_to
        msg['Subject'] = subject
        msg.set_content(message)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        with open(f'videos/{path}.mp4','rb') as f:
            file_data=f.read()
            file_name=f.name
        msg.add_attachment(file_data,maintype='video',subtype='mp4',filename=file_name)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_from,self.pswd)
            smtp.send_message(msg)
        print("Stopped recording")
        print("Email with video has been successfully sended :-)")

def main():
    pass

if __name__=="__main__":
    main()