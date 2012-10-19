import twitter

from email.utils import formatdate
from datetime import datetime
from time import mktime

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
        self.api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                                access_token_key=ACCESS_KEY, access_token_secret=ACCESS_SECRET)

    def tweet_message(self, message):
        try:
            self.api.PostUpdate(message)

        except twitter.TwitterError, e:
            print "Twitter failed. %s" % e

    def get_direct_messages(self, minutesAgo=10):
        try:
            now = datetime.datetime.now() - datetime.timedelta(minutes=minutesAgo)
            stamp = mktime(now.timetuple())
            time = formatdate(timeval=stamp, localtime=False, usegmt=True)

            return self.api.GetDirectMessages(since=time)

        except twitter.TwitterError, e:
            print "Twitter failed. %s" % e


if __name__ == "__main__":
    main()
