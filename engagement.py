class EngagementCalculator:

    @staticmethod
    def calculate(posts, followers):

        if followers == 0 or not posts:
            return 0

        total_likes = 0
        total_comments = 0

        for post in posts:
            print(post.get("likesCount"), post.get("commentsCount"))

            total_likes += post.get("likesCount", 0)
            total_comments += post.get("commentsCount", 0)

        average = (total_likes + total_comments) / len(posts)

        engagement = (average / followers) * 100

        print("Followers:", followers)
        print("Average Engagement:", average)
        print("Rate:", engagement)

        return round(engagement, 2)