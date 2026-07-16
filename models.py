import re

from engagement import EngagementCalculator


class Influencer:

    def __init__(self, profile):

        self.username = profile.get("username", "")

        self.full_name = profile.get("fullName", "")

        self.followers = profile.get("followersCount", 0)

        self.posts = profile.get("postsCount", 0)

        business_email = profile.get("businessEmail")

        biography = profile.get("biography", "")

        if business_email:
            self.email = business_email

        else:
            email_match = re.search(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                biography
            )

            if email_match:
                self.email = email_match.group()

            else:
                self.email = "Not specified"

        business_phone = profile.get("businessPhoneNumber")

        if business_phone:
            self.phone_number = business_phone
        else:
            self.phone_number = "Not specified"

        self.profile_url = profile.get(
            "url",
            f"https://www.instagram.com/{self.username}/"
        )

        urls = profile.get("externalUrls", [])

        if urls:

            first_url = urls[0]

            if isinstance(first_url, dict):
                self.external_url = first_url.get(
                    "url",
                    "Not specified"
                )

            else:
                self.external_url = first_url

        else:

            self.external_url = "Not specified"

        self.engagement_rate = EngagementCalculator.calculate(
            profile.get("latestPosts", []),
            self.followers
        )

        self.approval_status = "Pending"

        self.contacted = "No"

    def to_dict(self):

        return {

            "username": self.username,

            "full_name": self.full_name,

            "followers": self.followers,

            "posts": self.posts,

            "email": self.email,

            "phone_number": self.phone_number,

            "engagement_rate": self.engagement_rate,

            "profile_url": self.profile_url,

            "external_url": self.external_url,

            "approval_status": self.approval_status,

            "contacted": self.contacted
        }