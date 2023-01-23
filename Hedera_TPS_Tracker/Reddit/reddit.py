import praw

from Reddit.reddit_creds import CLIENT_ID, CLIENT_SECRET, REDDIT_USER, REDDIT_PASS

# Subreddit flair id
hbar_flair = ""

class RedditPoster:
    def __init__(self) -> None:

        self.reddit = praw.Reddit(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET,
                                  username=REDDIT_USER,
                                  password=REDDIT_PASS,
                                  user_agent="Hedera")

    '''-----------------------------------'''

    def create_image_post(self, img_path: str, post_title: str, subreddit: str, reply: str = None):

        flair = hbar_flair

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
