import gspread

from google.oauth2.service_account import Credentials

from config import CREDENTIALS_FILE
from config import SHEET_NAME


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


class GoogleSheets:

    def __init__(self):

        credentials = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=SCOPES
        )

        client = gspread.authorize(credentials)

        self.sheet = client.open(
            SHEET_NAME
        ).sheet1

    def add_influencer(self, influencer):

        records = self.sheet.get_all_records()

        row_number = None

        for index, record in enumerate(records, start=2):

            if record["Username"] == influencer["username"]:

                row_number = index
                break

        row = [
            influencer["username"],
            influencer["full_name"],
            influencer["followers"],
            influencer["posts"],
            influencer["email"],
            influencer["phone_number"],
            influencer["engagement_rate"],
            influencer["profile_url"],
            influencer["external_url"],
            influencer["approval_status"],
            influencer["contacted"]
        ]

        if row_number:

            cell_range = f"A{row_number}:K{row_number}"

            self.sheet.update(
                cell_range,
                [row]
            )

            print(
                f"Updated : {influencer['username']}"
            )

        else:

            self.sheet.append_row(
                row
            )

            print(
                f"Inserted : {influencer['username']}"
            )

    def get_all_influencers(self):

        return self.sheet.get_all_records()

    def update_cell(
        self,
        row,
        column,
        value
    ):

        self.sheet.update_cell(
            row,
            column,
            value
        )