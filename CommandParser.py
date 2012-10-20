from TwitterController import TwitterController
from ImgurController import ImgurController


class CommandParser(object):
    """
    Parser for commands given via direct message for the ImgurVault bot
    Valid commands:
    random [n (optional)]
    gallery [galleryName] [top/random] [n (optional)]
    """

    def __init__(self, ImgurController, TwitterController):
        super(CommandParser, self).__init__()
        self.imgController = ImgurController
        self.twController = TwitterController
        self.MAX_IMAGES = 10

    def parse_commands(self, commands=None):
        if commands:
            cmds = commands
        else:
            cmds = self.twController.get_direct_messages()

        for cmd in cmds:
            cmdTokens = cmd.text.split()
            numTokens = len(cmdTokens)

            if numTokens not in [1, 2, 3, 4]:
                return

            # random
            elif cmdTokens[0] in ["random", "Random"]:

                # random
                if numTokens == 1:
                    numImages = 1
                else:
                    numImages = min([int(cmdTokens[1]), self.MAX_IMAGES])

                # Tweet numImages random images, across all of imgur
                # Does not keep track of previously tweeted images
                for i in range(numImages):
                    message = self.imgController.get_formatted_random_image_message()
                    self.twController.tweet_message(message)

            # gallery
            elif cmdTokens[0] in ["gallery", "Gallery"]:
                galleryName = cmdTokens[1]
                imagePool = cmdTokens[2]

                if numTokens == 4:
                    numImages = min([int(cmdTokens[3]), self.MAX_IMAGES])
                else:
                    numImages = 1

                # Tweet numImages random or top images from the given gallery
                # Does not keep track of previously tweeted images
                if imagePool in ["top", "random"]:
                    messages = self.imgController.get_formatted_gallery_messages(galleryName, type=imagePool, numImages=numImages)
                    for msg in messages:
                        self.twController.tweet_message(msg)
