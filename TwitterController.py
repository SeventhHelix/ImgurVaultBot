import tweepy
import time

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''


def main():
    tc = TwitterController()
    dms = tc.get_direct_messages()
    for item in dms:
        print item.sender_screen_name
        print item.text


class TwitterController(object):
    """docstring for TwitterController"""

    def __init__(self):
        super(TwitterController, self).__init__()
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def tweet_messages(self, messages):
        """Tweet a list of messages"""
        for msg in messages:
            self.tweet_message(msg)

    def tweet_message(self, message):
        """Tweet a given message"""
        try:
            self.api.update_status(message)

        except twitter.TwitterError, e:
            print "Twitter failed. %s" % e

    def get_direct_messages(self, minutesAgo=10):
        """Return a list of DirectMessage objects created less than minutesAgo prior to the call"""
        try:
            secondsAgo = minutesAgo * 60
            timeSinceEpoch = int(time.time()) - secondsAgo

            # return self.api.GetDirectMessages(since=time)
            msgs = self.api.direct_messages
            #msgs = self.api.GetDirectMessages()
            #recentMsgs = [msg for msg in msgs if msg.GetCreatedAtInSeconds() >= timeSinceEpoch]
            return recentMsgs

        except twitter.TwitterError, e:
            print "Twitter failed. %s" % e
            return []


if __name__ == "__main__":
    main()
