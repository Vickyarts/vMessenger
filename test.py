import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




def sendEmail():
    sender_email = 'vickyippsec24@gmail.com'
    recipient_email = 'vignesharplayboyvicky@gmail.com'
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'Test Email via SendPulse API'
    body = 'This is a test email sent via SendPulse SMTP service.'
    message.attach(MIMEText(body, 'plain'))
    smtp_server = None
    try:
        smtp_server = smtplib.SMTP('smtp-pulse.com', 587)
        smtp_server.starttls()
        smtp_server.login('vigneshar-bca@srmasc.ac.in', 'mAf5qG7TpAoqS')
        smtp_server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))
    finally:
        smtp_server.quit()


sendEmail()