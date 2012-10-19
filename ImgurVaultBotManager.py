from optparse import OptionParser
from TwitterController import TwitterController
from ImgurController import ImgurController
from CommandParser import CommandParser


def main():
    # Parse the command line arguments to determine what to tweet

    parser = OptionParser()
    imgController = ImgurController()
    twController = TwitterController()
    cmdParser = CommandParser(imgController, twController)

    parser.add_option("-e", "--exec-direct-messages", dest="exec_direct_messages", default=False,
        action="store_true", help="Check direct messages for commands")

    parser.add_option("-n", "--number", dest="number", default=1,
        help="Specify the number of images to post")

    parser.add_option("-g", "--gallery", dest="gallery", default="random",
        help="Specify a gallery to get images from")

    (options, args) = parser.parse_args()

    if options.exec_direct_messages:
        # Parse direct messages and exec their commands
        print "Exec direct messages!"
        cmdParser.parse_commands()

    elif options.gallery != "random":
        # Print images from specific gallery
        print "Printing " + options.number + " images from gallery " + options.gallery + "!"

    else:
        # just post random images
        for i in range(int(options.number)):
            message = imgController.get_formatted_random_image_message()
            twController.tweet_message(message)


if __name__ == "__main__":
    main()
