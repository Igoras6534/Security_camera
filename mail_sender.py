import smtplib
import ssl
import os



class EmailSender():
    def __init__(self):
        self.smtp_port = 587  # Standard secure SMTP port
        self.smtp_server = "smtp.gmail.com" # Google SMTP Server

        self.pswd=os.environ.get('SMTP_PASSW') #SMTP email adress password
        self.email_from= os.environ.get('SMTP_MAIL')# SMTP email adress
        
        self.simple_email_context = ssl.create_default_context()

    def send_email(self, email_to):
        message= "Someone has appeared on your camera. "
        try:
            # Connect to the server
            #print("Connecting to server...")
            TIE_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            TIE_server.starttls(context=self.simple_email_context)
            TIE_server.login(self.email_from, self.pswd)
            #print("Connected to server :-)")   
            # Send the actual email
            #print(f"Sending email to - {email_to}")
            TIE_server.sendmail(self.email_from, email_to, message)
            print(f"Email successfully sent to - {email_to}")
        # If there's an error, print it out
        except Exception as e:
            print(e)

        # Close the port
        finally:
            TIE_server.quit()
    def send_video(self):
        pass







def main():
    pass






if __name__=="__main__":
    main()