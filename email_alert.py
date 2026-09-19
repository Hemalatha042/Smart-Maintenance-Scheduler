import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
def send_email_alert(to_email, machines_count):
    from_email = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    subject = "Maintenance Alert: Attention Required"
    body = f"{machines_count} machine(s) need maintenance according to the latest report."

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Email failed:", e)
        return False
