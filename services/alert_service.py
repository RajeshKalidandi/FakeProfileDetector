import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class AlertService:
    def __init__(self):
        self.sender_email = os.getenv('ALERT_EMAIL')
        self.sender_password = os.getenv('ALERT_EMAIL_PASSWORD')
        self.admin_email = os.getenv('ADMIN_EMAIL')

    def send_alert(self, subject: str, body: str):
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = self.admin_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(message)

alert_service = AlertService()
