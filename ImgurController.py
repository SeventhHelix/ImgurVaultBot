import os
import requests
import random
import hashlib
import string
import pycurl
import cStringIO
import untangle

debug = False


def main():
    imgController = ImgurController()
    # imgController.get_formatted_messages_from_gallery("aww")
    # if debug:
    #     print_image_info()
    # else:
    #     tweepy_authenticate()
    #     tweet_random_image()
        # tweepy_auth_and_tweet()


class ImgurController(object):
    """
    Class for finding random Imgur images, getting formatted messages with the url,
    and other Imgur api functions
    """
    def __init__(self):
        super(ImgurController, self).__init__()
        self.IMGUR_API_DEV_KEY = ''

    def gen_random_url(self):
        """Generates a random imgur hash and url, not guaranteed to be an actual image"""

        baseUrl = "http://www.imgur.com/"
        fileExt = ".jpg"
        genHash = ""

        chars = string.letters + string.digits

        genHash = ''.join(random.choice(chars) for X in range(5))

        url = ''.join([baseUrl, genHash, fileExt])
        return [url, genHash]

    def test_url(self, url):
        """Tests the given url to check if it's a valid imgur link and not the 404 image"""

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

    def save_image(self, filename, imageData, path="~/tmp/RandomImgur/"):
        """Saves an image to the specified directory"""

        if not os.path.exists(path):
            os.makedirs(path)

        outfile = open(path + filename, 'w')
        outfile.write(imageData)
        outfile.close()

    def get_image_description(self, hash):
        """Gets the image title and/or caption in a formatted string
            Note that the xml returned for random images vs. gallery/subreddit images
            is a bit different, they have to be done differently. This is for random
            images.
        """

        # Getting the xml information for images can fail if the Imgur servers are busy or down
        # In this case, just set the title and caption to ""
        try:
            # Post the api.imgur server for the image information
            response = cStringIO.StringIO()
            c = pycurl.Curl()
            values = [("key", self.IMGUR_API_DEV_KEY)]

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

        except:
            imageTitle = ""
            imageCaption = ""

        # Format the description, taking care to not go over 140 chars
        # Admittedly, this is isn't very pretty. I'm sure it could be done better
        urlLength = 28

        if imageTitle is not "":
            if imageCaption is not "":
                # Title: Caption [Url]
                titleLength = len(imageTitle) + 2                   # +2 for ": " after the title
                captionLength = 140 - urlLength - titleLength - 1   # -1 for space after caption between url
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

    def get_image_info(self):
        """Gets a random image url from Imgur"""
        attempts = 1

        urlInfo = self.gen_random_url()

        (url, hash) = urlInfo

        # Continuously generate urls until one succeeds
        while not self.test_url(url):
            attempts += 1
            urlInfo = self.gen_random_url()
            (url, hash) = urlInfo

        description = self.get_image_description(hash)

        return [url, description]

    def format_message(self, imageUrl, imageTitle):
        """Returns a formatted message containing the url and title/desc if applicable"""
        if imageTitle != "":
            message = imageTitle + " [" + imageUrl + "]"
        else:
            message = imageUrl

        return message

    def print_image_info(self):
        """Prints the formatted message for debug purposes"""
        urlInfo = self.get_image_info()
        (imageUrl, imageDescription) = urlInfo

        print imageUrl
        print imageDescription
        print self.format_message(imageUrl, imageDescription)

    def get_formatted_random_image_message(self):
        """Gets a random imgur image and tweets it"""

        urlInfo = self.get_image_info()
        imageUrl = urlInfo[0].replace("imgur", "i.imgur")
        imageTitle = urlInfo[1]

        message = self.format_message(imageUrl, imageTitle)
        return message

    def get_gallery_values(self, gallery):
        """Returns a list of [hash, title, nsfw] for the first page of a given gallery"""
        try:
            # Post the imgur server for the image information
            url = "http://imgur.com/r/" + gallery + ".xml"
            response = requests.get(url)

            xml = response.text

            # Analyze the xml response
            doc = untangle.parse(xml)
            items = doc.data.item

            # Get a list of [hash, title] from the xml feed
            images = [[img.hash.cdata, img.title.cdata, img.nsfw.cdata] for img in items]

            return images

        except Exception, e:
            print "Failed: %s" % e
            return []

    def get_formatted_gallery_messages(self, gallery, type="random", numImages=1):
        """Returns a list of random or top formatted messages from a gallery"""
        imgIncr = 0
        imageMessages = []

        images = self.get_gallery_values(gallery)

        for x in range(numImages):
            if type == "random":
                imgNumber = random.choice(range(len(images)))
                randImage = images[imgNumber]
                imgHash = randImage[0]
                imgTitle = randImage[1]
                imgNSFW = randImage[2]

            elif type == "top":
                topImage = images[imgIncr]
                imgHash = topImage[0]
                imgTitle = topImage[1]
                imgNSFW = topImage[2]
                imgIncr = imgIncr + 1

            if imgNSFW == "true":
                imgNSFW == "NSFW "
            else:
                imgNSFW = ""

            imgUrl = " [" + imgNSFW + "http://i.imgur.com/" + imgHash + ".jpg]"
            availTitleLen = 160 - len(imgUrl)

            if len(imgTitle) > availTitleLen:
                msg = imgTitle[0:availTitleLen - 3] + "..." + imgUrl

            else:
                msg = imgTitle + imgUrl

            imageMessages.append(msg)

        return imageMessages


if __name__ == "__main__":
    main()
