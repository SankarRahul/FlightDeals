import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class NotificationManager:
    """This class is responsible for sending email notifications."""
    
    def __init__(self):
        self.email_user = os.environ["EMAIL_USER"]
        self.email_password = os.environ["EMAIL_PASSWORD"]
        self.recipient_email = os.environ["RECIPIENT_EMAIL"]

    def send_email(self, message_body):
        """Sends an email notification with specified message body."""
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = self.email_user
        msg['To'] = self.recipient_email
        msg['Subject'] = "Low Price Flight Alert"
        
        # Attach email body
        msg.attach(MIMEText(message_body, 'plain'))

        try:
            # Establish connection to Gmail server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls() 
            server.login(self.email_user, self.email_password) 

            # Send email
            text = msg.as_string()
            server.sendmail(self.email_user, self.recipient_email, text)
            print(f"Email sent successfully to {self.recipient_email}.")
            server.quit()

        except Exception as error:
            print(f"Failed to send email: {error}")
