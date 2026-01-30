import smtplib
from email.mime.text import MIMEText
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(recipient_email, otp):
    sender_email = "bharathnaikpatil22@gmail.com"
    app_password = "wjbh mwuk iiqt fvkq"

    subject = "Your OTP Code"
    body = f"Your one-time password (OTP) is: {otp}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Email sending failed:", e)
        return False
