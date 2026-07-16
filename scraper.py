from apify_client import ApifyClient

from config import APIFY_TOKEN
from config import APIFY_ACTOR_ID


class InstagramScraper:

    def __init__(self):

        self.client = ApifyClient(APIFY_TOKEN)

    def scrape_profiles(self, usernames):

        print(f"\nScraping {len(usernames)} profiles...\n")

        run_input = {
            "usernames": usernames,
            "resultsLimit": len(usernames)
        }

        run = self.client.actor(
            APIFY_ACTOR_ID
        ).call(
            run_input=run_input
        )

        # Compatible with different Apify SDK versions
        if hasattr(run, "default_dataset_id"):
            dataset_id = run.default_dataset_id
        elif isinstance(run, dict):
            dataset_id = run["defaultDatasetId"]
        else:
            dataset_id = run.default_dataset_id

        dataset = self.client.dataset(dataset_id)

        profiles = []

        related_usernames = set()

        blocked = {
            "",
            None,
            "explore",
            "reel",
            "reels",
            "stories",
            "accounts",
            "p",
            "tv",
            "popular",
            "https:"
        }

        for item in dataset.iterate_items():

            profiles.append(item)

            related = item.get("relatedProfiles", [])

            for profile in related:

                if isinstance(profile, dict):
                    username = profile.get("username", "")
                else:
                    username = str(profile)

                username = username.strip().lower()

                if username not in blocked:
                    related_usernames.add(username)

        print(f"Profiles Scraped : {len(profiles)}")
        print(f"Related Profiles Found : {len(related_usernames)}")

        return profiles, list(related_usernames)