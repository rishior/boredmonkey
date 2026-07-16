import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from config import EMAIL_ADDRESS
from config import EMAIL_APP_PASSWORD


class EmailSender:

    def send_email(self, influencer):

        if influencer["email"] == "Not specified":

            print(
                f"No email found for {influencer['username']}"
            )

            return False

        message = MIMEMultipart()

        message["From"] = EMAIL_ADDRESS

        message["To"] = influencer["email"]

        message["Subject"] = (
            "Collaboration Opportunity"
        )

        body = f"""
Hi {influencer['full_name']},

We came across your Instagram profile and loved your content.

We would love to discuss a collaboration opportunity with you.

If you're interested, please reply to this email.

Best Regards,
Rishi
"""

        message.attach(
            MIMEText(body, "plain")
        )

        try:

            server = smtplib.SMTP(
                "smtp.gmail.com",
                587
            )

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_APP_PASSWORD
            )

            server.send_message(message)

            server.quit()

            print(
                f"Email sent to {influencer['username']}"
            )

            return True

        except Exception as error:

            print(error)

            return False