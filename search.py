import requests

from config import SERP_API_KEY


class InstagramSearch:

    def __init__(self):

        self.base_url = "https://serpapi.com/search.json"

    def build_queries(self, niche, region):

        return [

            # Core
            f"{niche} influencer {region}",
            f"{niche} creator {region}",
            f"{niche} blogger {region}",

            # Long tail
            f"micro {niche} influencer {region}",
            f"nano {niche} influencer {region}",
            f"rising {niche} creator {region}",
            f"emerging {niche} influencer {region}",

            # Cities
            f"{niche} influencer mumbai",
            f"{niche} influencer delhi",
            f"{niche} influencer bangalore",
            f"{niche} influencer pune",
            f"{niche} influencer hyderabad",

            # Different wording
            f"best {niche} instagram creators india",
            f"top {niche} content creators india",
            f"{niche} reels creator india",
            f"{niche} collaboration instagram india",

            # Related niches
            f"streetwear influencer india",
            f"sustainable {niche} india",
            f"luxury {niche} india",
            f"ethnic wear influencer india",
            f"fashion stylist india"
        ]

    def search_profiles(self, niche, region):

        queries = self.build_queries(
            niche,
            region
        )

        usernames = set()

        blocked = {
            "",
            "explore",
            "explore-tags",
            "tags",
            "reel",
            "reels",
            "stories",
            "accounts",
            "p",
            "tv",
            "popular"
        }

        for query in queries:

            print(f"\nSearching -> {query}")

            for start in [0, 10, 20]:

                params = {
                    "engine": "google",
                    "q": f"site:instagram.com {query}",
                    "api_key": SERP_API_KEY,
                    "start": start
                }

                try:

                    response = requests.get(
                        self.base_url,
                        params=params,
                        timeout=30
                    )

                    response.raise_for_status()

                    data = response.json()

                    for result in data.get(
                        "organic_results",
                        []
                    ):

                        link = result.get(
                            "link",
                            ""
                        )

                        if "instagram.com/" not in link:
                            continue

                        username = (
                            link
                            .replace(
                                "https://www.instagram.com/",
                                ""
                            )
                            .replace(
                                "https://instagram.com/",
                                ""
                            )
                            .split("/")[0]
                            .strip()
                            .lower()
                        )

                        if username in blocked:
                            continue

                        usernames.add(username)

                except Exception as error:

                    print(error)

        usernames = sorted(list(usernames))

        print(
            f"\nTotal Unique Usernames Found : {len(usernames)}"
        )

        return usernames