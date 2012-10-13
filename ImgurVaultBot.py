import os
import requests
import random
import sys
import md5
import string
import tweepy

CONSUMER_KEY = 'xxxxxxxxxxx'
CONSUMER_SECRET = 'xxxxxxxxxxxxxxxxxxxxx'
ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
ACCESS_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'

debug = True


def main():
    getImageUrl()
    #printImageInfo()
    if not debug:
        tweepyAuthAndTweet()


# Generates a random imgur url
# Not guaranteed to be an actual image
def genRandomUrl():
    baseUrl = "http://www.imgur.com/"
    fileExt = ".jpg"
    genUrl = ""

    chars = string.letters + string.digits

    genUrl = ''.join(random.choice(chars) for X in range(5))

    url = ''.join([baseUrl, genUrl, fileExt])
    return url


# Tests the given url to check if it's a valid imgur link and not the 404 image
def testUrl(url):
    req = requests.get(url)

    if (req.status_code != 404):

        # Hash the image to later check if it's the 404 image
        image_hash = md5.new(req.content).hexdigest()

        # If the file is an image, and not imgur's 404 image, return true
        ext = req.headers['content-type']

        if ext == "image/gif" or ext == "image/jpeg" or ext == "image/png":
            if image_hash != 'eebc93350a68a64022b7482f460017ba':
                if image_hash != 'd835884373f4d6c8f24742ceabe74946':
                    return True

    # Failed somewhere - Not a real image
    return False


# Saves an image to the specified directory
def saveImage(filename, imageData, path="~/tmp/RandomImgur/"):
    if not os.path.exists(path):
        os.makedirs(path)

    outfile = open(path + filename, 'w')
    outfile.write(imageData)
    outfile.close()


# Gets a random image' url from Imgur
def getImageUrl():
    attempts = 1
    url = genRandomUrl()

    # Continuously generate urls until one succeeds
    while not testUrl(url):
        attempts += 1
        url = genRandomUrl()

    print "Success after " + str(attempts) + " attempts."

    # Set the title if it exists
    imageTitle = "Title"

    if debug:
        print url
        print imageTitle

    return [url, imageTitle]


# Prints the imgur link for debug purposes
#def printImageInfo():
    #print imageUrl
    #print imageTitle


# Authenticates the Twitter user and posts the tweet
def tweepyAuthAndTweet():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    if imageTitle == "":
        message = imageTitle + " [" + imageUrl + "]"
    else:
        message = imageUrl

    api.update_status(message)

if __name__ == "__main__":
    main()
