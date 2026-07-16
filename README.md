# BOREDMONKEY 

An Instagram influencer discovery and outreach automation project. It searches for influencer profiles by niche and region, scrapes profile data from Instagram using Apify, saves structured records to Google Sheets, and can automatically send outreach emails for approved influencers.

## Repository Structure

- `.env` - Environment variables and secret configuration (not included in source control normally).
- `credentials.json` - Google service account credentials used by `gspread` to access Google Sheets.
- `config.py` - Loads environment variables and exposes configuration constants used by the app.
- `search.py` - Builds search queries and extracts Instagram usernames from SerpApi Google search results.
- `scraper.py` - Runs an Apify Instagram profile scraper actor and collects profile data and related usernames.
- `models.py` - Defines the `Influencer` model that normalizes profile fields, extracts contact details, and computes engagement rate.
- `engagement.py` - Provides engagement rate calculation logic.
- `sheets.py` - Provides Google Sheets interaction methods for inserting, updating, and retrieving influencer records.
- `mailer.py` - Sends outreach emails via Gmail SMTP using account credentials from `config.py`.
- `watcher.py` - Continuously polls the Google Sheet for approved influencers and sends outreach emails to newly approved profiles.
- `main.py` - Example workflow script that performs search, profile scraping, filtering, and saving to Google Sheets.
- `utils.py` - Empty placeholder module.
- `requirements.txt` - Python dependency list.

## File Documentation

### `config.py`
Loads environment variables from `.env` and exposes constants for:
- `CREDENTIALS_FILE` - Service account JSON file path.
- `SHEET_NAME` - Google Sheet name.
- `APIFY_TOKEN` - Apify API token.
- `APIFY_ACTOR_ID` - Apify actor identifier for the Instagram profile scraper.
- `SERP_API_KEY` - SerpApi key for Google search.
- `EMAIL_ADDRESS` - Gmail address used to send emails.
- `EMAIL_APP_PASSWORD` - App password for SMTP authentication.

### `search.py`
Defines the `InstagramSearch` class.
- `build_queries(niche, region)` returns a list of search query strings for the target niche and region.
- `search_profiles(niche, region)` calls SerpApi, parses Google search results, extracts Instagram usernames, and returns a unique sorted username list.

### `scraper.py`
Defines the `InstagramScraper` class.
- Initializes an Apify client with `APIFY_TOKEN`.
- `scrape_profiles(usernames)` calls the configured Apify actor with a list of usernames.
- Processes the returned dataset and yields raw profile items plus a list of related profile usernames.

### `models.py`
Defines the `Influencer` class used to normalize raw profile data.
- Extracts core fields such as `username`, `full_name`, `followers`, `posts`, and profile URLs.
- Extracts email from `businessEmail` or finds it inside biography text.
- Extracts business phone number if available.
- Computes `engagement_rate` using `EngagementCalculator.calculate()`.
- Exposes `to_dict()` to generate a normalized dictionary suitable for spreadsheets.

### `engagement.py`
Defines `EngagementCalculator`.
- `calculate(posts, followers)` computes average engagement as `(average likes + comments) / followers * 100`.
- Returns `0` if there are no posts or followers count is zero.

### `sheets.py`
Defines the `GoogleSheets` class.
- Uses `gspread` and Google service account credentials to open the configured sheet and access the first worksheet.
- `add_influencer(influencer)` appends a new row or updates an existing row when the influencer username already exists.
- `get_all_influencers()` returns all sheet records.
- `update_cell(row, column, value)` updates an individual cell.

### `mailer.py`
Defines the `EmailSender` class.
- `send_email(influencer)` sends a collaboration outreach email using Gmail SMTP.
- If the influencer email is not specified, it logs a message and returns `False`.
- Uses `EMAIL_ADDRESS` and `EMAIL_APP_PASSWORD` from configuration.

### `watcher.py`
Defines `ApprovalWatcher`.
- Periodically polls the Google Sheet every 30 seconds.
- Checks records for `Approval Status == "Approved"` and `Contacted == "No"`.
- Sends an email via `EmailSender` and updates the sheet to mark the influencer as contacted.
- Runs indefinitely when executed.

### `main.py`
Example script demonstrating the main pipeline:
1. Search for influencer usernames using `InstagramSearch`.
2. Scrape profiles and related profiles using `InstagramScraper`.
3. Remove duplicate profiles.
4. Filter profiles by follower count and privacy status.
5. Convert profiles into `Influencer` objects and save them to Google Sheets.

### `utils.py`
An empty module included as a placeholder.

### `requirements.txt`
Lists required external Python packages, including:
- `pandas`
- `instaloader`
- `gspread`
- `google-auth`
- `schedule`
- `python-dotenv`
- `apify-client`
- `requests`

## Setup

1. Install Python 3 and create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Provide a Google service account credentials file at the path referenced by `config.py` (`credentials.json`).
4. Create a `.env` file with the following variables:
   - `SHEET_NAME`
   - `APIFY_TOKEN`
   - `APIFY_ACTOR_ID`
   - `SERP_API_KEY`
   - `EMAIL_ADDRESS`
   - `EMAIL_APP_PASSWORD`
5. Ensure the Google Sheet named by `SHEET_NAME` exists and is shared with the service account email.

## Usage

Run the main discovery pipeline:
```bash
python main.py
```

Run the approval watcher to send outreach emails for approved influencers:
```bash
python watcher.py
```

## Expected Google Sheet Columns

The project assumes the sheet contains the following headers in the first row:
- `Username`
- `Full Name`
- `Followers`
- `Posts`
- `Email`
- `Phone Number`
- `Engagement Rate`
- `Profile URL`
- `External URL`
- `Approval Status`
- `Contacted`

## Notes

- Do not commit `.env` or `credentials.json` to public repositories.
- The code relies on external services: SerpApi for search, Apify for scraping, Google Sheets API, and Gmail SMTP.
- The current `watcher.py` loop runs forever until interrupted.
