import smtplib
from email.message import EmailMessage
from backend.baseConfig.config import EMAIL_ADDRESS
from backend.engine.helpers import logger


contacts = [EMAIL_ADDRESS, "servier.network.in@capgemini.com"]
#contacts = [EMAIL_ADDRESS]

def send_notification_email(password, subject, html_content=None, attachment=None, filename=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = contacts

    if html_content is not None:
        msg.add_alternative(html_content, subtype='html')

    if attachment is not None:
        with open(attachment, "rb") as file:
            email_attachment = file.read()
            msg.add_attachment(email_attachment, maintype="application", subtype="octet-stream",
                               filename=filename)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, password)
        smtp.send_message(msg)
    logger.info("Email notification sent.")


def send_error_notification(subject, content, password):

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = contacts
    msg.add_alternative(content, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, password)
        smtp.send_message(msg)


if __name__ == "__main__":
    pass
    # send_error_notification()
