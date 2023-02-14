import requests
import praw

from Reddit.reddit_creds import CLIENT_ID, CLIENT_SECRET, REDDIT_USER, REDDIT_PASS

# Subreddit flair id
hbar_flair = "ec86dbe6-256b-11ec-8a02-2252f39e8fc6"

DVC_discussion_flair = "897b4ec6-7ff4-11ed-933e-72344fe53b2f"

BTE_test_flair = "18e913ba-9853-11ed-89da-46ccef05df5c"


class RedditPoster:
    def __init__(self) -> None:

        self.reddit = praw.Reddit(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET,
                                  username=REDDIT_USER,
                                  password=REDDIT_PASS,
                                  user_agent="Hedera Network Tracker")

    '''-----------------------------------'''

    def create_image_post(self, img_path: str, post_title: str, subreddit: str, reply: str = None):

        if subreddit == "Hedera":
            flair = hbar_flair
        elif subreddit == "BotTestingEnv":
            flair = BTE_test_flair

        if reply == None:
            self.reddit.subreddit(
                subreddit).submit_image(post_title, img_path, flair_id=flair, nsfw=False)
        else:

            self.reddit.subreddit(
                subreddit).submit_image(post_title, img_path, flair_id=flair, nsfw=False).reply(reply)

    '''-----------------------------------'''

    def get_subreddit_flair_id(self, subreddit: praw.Reddit, flair_text: str) -> str:
        choices = list(subreddit.flair.link_templates.user_selectable())
        template_id = next(x for x in choices if x["flair_text"] == flair_text)[
            "flair_template_id"]
        return template_id

    '''-----------------------------------'''

    def get_comment(self, url: str):
        submission = self.reddit.submission(
            url=url)
        submission.comments.replace_more(limit=5)
        for comment in submission.comments:
            comment = comment.body
            if "|Date|" in comment and "|Time (UTC)|":
                return comment
