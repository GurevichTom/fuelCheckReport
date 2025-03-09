import os
import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import SMTP_SERVER, SENDER_EMAIL

logger = logging.getLogger(__name__)

def send_email(subject, body, attachment_path, recipient_emails):
    """
    Sends an email with the specified subject, body, and attachment.
    """
    sender_email = SENDER_EMAIL
    receiver_emails = [r.strip() for r in recipient_emails.split(";") if r.strip()]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ', '.join(receiver_emails)
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        filename = os.path.basename(attachment_path)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")
        message.attach(part)
        text = message.as_string()
    except (FileNotFoundError, OSError):
        logger.exception(f"Failed to attach file: {attachment_path}")
        return

    try:
        server = smtplib.SMTP(SMTP_SERVER)
        server.sendmail(sender_email, receiver_emails, text)
        server.quit()
        logger.info(f"Email sent successfully to {receiver_emails} with attachment {attachment_path}")
    except Exception:
        logger.exception(f"Failed to send email to {receiver_emails}")
