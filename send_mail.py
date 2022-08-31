import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from user_info import from_email, to_email, app_pass


def create_mail(from_email, to_email, subject, msg):
    message = MIMEMultipart()

    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email

    text = MIMEText(msg, "plain", "utf-8")
    message.attach(text)

    return message


def send_gmail(account, password, mail):
    smtp_server = "smtp.gmail.com"
    port = 587

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()

    login_address = account
    login_password = password

    server.login(login_address, login_password)

    server.send_message(mail)
    server.quit()


if __name__ == "__main__":
    mail = create_mail(from_email, to_email, "subject", "text")
    send_gmail(account=from_email, password=app_pass, mail=mail)
