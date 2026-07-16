from search import InstagramSearch
from scraper import InstagramScraper
from models import Influencer
from sheets import GoogleSheets


search = InstagramSearch()

scraper = InstagramScraper()

google_sheet = GoogleSheets()


# -------------------------
# STEP 1 : Search usernames
# -------------------------

usernames = search.search_profiles(
    niche="fashion",
    region="india"
)

print("\nSeed Usernames Found")
print(usernames)


# -------------------------
# STEP 2 : Scrape seed profiles
# -------------------------

profiles, related = scraper.scrape_profiles(
    usernames
)

print(f"\nRelated Profiles Found : {len(related)}")


# -------------------------
# STEP 3 : Scrape related profiles
# -------------------------

if related:

    print("\nScraping Related Profiles...\n")

    related_profiles, _ = scraper.scrape_profiles(
        related[:20]
    )

    profiles.extend(
        related_profiles
    )


# -------------------------
# STEP 4 : Remove duplicates
# -------------------------

unique_profiles = {}

for profile in profiles:

    username = profile.get("username", "").lower()

    if username:
        unique_profiles[username] = profile

profiles = list(
    unique_profiles.values()
)

print(f"\nUnique Profiles : {len(profiles)}")


# -------------------------
# STEP 5 : Filter Profiles
# -------------------------

filtered_profiles = []

for profile in profiles:

    followers = profile.get(
        "followersCount",
        0
    )

    if followers < 10000:
        continue

    if followers > 500000:
        continue

    if profile.get("private", False):
        continue

    filtered_profiles.append(
        profile
    )

print(f"Profiles After Filtering : {len(filtered_profiles)}")


# -------------------------
# STEP 6 : Save to Google Sheets
# -------------------------

for profile in filtered_profiles:

    influencer = Influencer(profile)

    google_sheet.add_influencer(
        influencer.to_dict()
    )

    print(influencer.to_dict())


print("\nCompleted Successfully!")