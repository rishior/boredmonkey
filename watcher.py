import time

from sheets import GoogleSheets
from mailer import EmailSender


class ApprovalWatcher:

    def __init__(self):

        self.google_sheet = GoogleSheets()

        self.mailer = EmailSender()

    def start(self):

        print("Watching Google Sheet...")

        while True:

            influencers = self.google_sheet.get_all_influencers()

            for index, influencer in enumerate(influencers, start=2):

                approval = influencer["Approval Status"]

                contacted = influencer["Contacted"]

                if (
                    approval == "Approved"
                    and contacted == "No"
                ):

                    print(
                        f"Approved : {influencer['Username']}"
                    )

                    success = self.mailer.send_email(
                        {
                            "username": influencer["Username"],
                            "full_name": influencer["Full Name"],
                            "email": influencer["Email"]
                        }
                    )

                    if success:

                        self.google_sheet.update_cell(
                            index,
                            11,
                            "Yes"
                        )

                        print(
                            f"Marked {influencer['Username']} as contacted."
                        )

            time.sleep(30)


if __name__ == "__main__":

    watcher = ApprovalWatcher()

    watcher.start()