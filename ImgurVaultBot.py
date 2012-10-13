import os
import requests
import random
import sys
import hashlib
import string
import tweepy
import pycurl
import cStringIO
import untangle

CONSUMER_KEY = '----------------------'
CONSUMER_SECRET = '---------------------------------------'
ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
ACCESS_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

debug = False


def main():
    if debug:
        printImageInfo()
    else:
        tweepyAuthAndTweet()


# Generates a random imgur url
# Not guaranteed to be an actual image
def genRandomUrl():
    baseUrl = "http://www.imgur.com/"
    fileExt = ".jpg"
    genHash = ""

    chars = string.letters + string.digits

    genHash = ''.join(random.choice(chars) for X in range(5))

    url = ''.join([baseUrl, genHash, fileExt])
    return [url, genHash]


# Tests the given url to check if it's a valid imgur link and not the 404 image
def testUrl(url):
    req = requests.get(url)

    if (req.status_code != 404):

        # Hash the image to later check if it's the 404 image
        image_hash = hashlib.md5(req.content).hexdigest()

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

# Gets the image title and/or caption in a formatted string
def getImageDescription(hash):

    # Post the api.imgur server for the image information
    response = cStringIO.StringIO()
    c = pycurl.Curl()
    values = [("key", IMGUR_API_DEV_KEY)]

    c.setopt(c.URL, "http://api.imgur.com/2/image/" + hash + ".xml")
    c.setopt(c.HTTPPOST, values)
    c.setopt(c.WRITEFUNCTION, response.write)

    c.perform()
    c.close()

    imageInfo = response.getvalue()

    # Analyze the xml response
    o = untangle.parse(imageInfo)
    imageTitle = o.image.image.title.cdata
    imageCaption = o.image.image.caption.cdata


    # Format the description, taking care to not go over 140 chars
    # Admittedly, this is isn't very pretty. I'm sure it could be done better
    urlLength = 28

    if imageTitle is not "":
        if imageCaption is not "":
            # Title: Caption [Url]
            titleLength = len(imageTitle) + 2 # +2 for ": " after the title
            captionLength = 140 - urlLength - titleLength - 1 # -1 for space after caption between url
            imageFullDescription = imageTitle + ": " + imageCaption[0:captionLength]
            return imageFullDescription
        else:
            # Title [Url]
            titleLength = 140 - urlLength
            imageFullDescription = imageTitle[0:titleLength]
            return imageFullDescription

    else:
        if imageCaption is not "":
            # Caption [Url]
            captionLength = 140 - urlLength
            imageFullDescription = imageCaption[0:captionLength]
            return imageFullDescription
        else:
            # Url
            imageFullDescription = ""
            return imageFullDescription

    return imageFullDescription


# Gets a random image' url from Imgur
def getImageInfo():
    attempts = 1

    urlInfo = genRandomUrl()
    url = urlInfo[0]
    hash = urlInfo[1]

    # Continuously generate urls until one succeeds
    while not testUrl(url):
        attempts += 1
        urlInfo = genRandomUrl()
        url = urlInfo[0]
        hash = urlInfo[1]

    print "Success after " + str(attempts) + " attempts."

    description = getImageDescription(hash)

    if debug:
        print url
        print imageTitle
        print description

    return [url, description]


# Prints the imgur link for debug purposes
def printImageInfo():
    urlInfo = getImageInfo()
    imageUrl = urlInfo[0]
    imageDescription = urlInfo[1]

    print imageUrl
    print imageDescription


# Authenticates the Twitter user and posts the tweet
def tweepyAuthAndTweet():
    urlInfo = getImageInfo()
    imageUrl = urlInfo[0]
    imageTitle = urlInfo[1]

    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

        message = ""

        if imageTitle != "":
            message = imageTitle + " [" + imageUrl + "]"
        else:
            message = imageUrl

        print "Updating status with: " + message

        api.update_status(message)

    except tweepy.TweepError:
        print "Tweepy failed"

if __name__ == "__main__":
    main()
