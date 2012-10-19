from TwitterController import TwitterController
from ImgurController import ImgurController


class CommandParser(object):
    """docstring for CommanParser"""
    def __init__(self, ImgurController, TwitterController):
        super(CommandParser, self).__init__()
        self.imgController = ImgurController
        self.twController = TwitterController

    def parse_commands(self, commands):
        if commands:
            cmds = commands
        else:
            cmds = self.twController.get_direct_messages()

        for cmd in cmds:
            cmdTokens = cmd.split()

            # Valid commands:
            # random [n (optional)]
            # gallery [galleryName] [top/random] [n (optional)]

            if len(cmdTokens) not in [1, 2, 3, 4]:
                return

            elif cmdTokens[0] == "random":
                if len(cmdTokens) == 1:
                    pass    # one random image
                else:
                    numImages = int(cmdTokens[1])
                    pass    # numImages random images

            elif cmdTokens[0] == "gallery":
                galleryName = cmdTokens[1]
                imagePool = cmdTokens[2]

                if len(cmdTokens) == 3:
                    pass    # one image from galleryName and imagePool

                else:
                    numImages = int(cmdTokens[3])
                    pass    # numImages images from galleryName and imagePool
