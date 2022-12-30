import imghdr
import smtplib
from email.message import EmailMessage


def email_sender(content, email, password):
    """Sending email with the attached picture"""

    email_msg = EmailMessage()
    email_msg["Subject"] = "New object detected"
    email_msg.set_content("Hey, check this out !")

    # open the picture in binary format
    with open(content, "rb") as file:
        cont = file.read()

    email_msg.add_attachment(cont, maintype='image', subtype=imghdr.what(None, cont))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, email_msg.as_string())
    server.quit()
