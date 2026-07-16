import os

from dotenv import load_dotenv

load_dotenv()


CREDENTIALS_FILE = "credentials.json"

SHEET_NAME = os.getenv("SHEET_NAME")

APIFY_TOKEN = os.getenv("APIFY_TOKEN")

APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID")

SERP_API_KEY = os.getenv("SERP_API_KEY")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")

EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")