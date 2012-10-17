from optparse import OptionParser
import os
import sys
import string
import ImgurVaultBot


def main():
	# Parse the command line arguments to determine what to tweet
	parser = OptionParser()
	parser.add_option("-e", "--exec-direct-messages", dest="exec_direct_messages", default=False,
					action="store_true", help="Check direct messages for commands")
	parser.add_option("-n", "--number", dest="number", default=1,
					help="Specify the number of images to post")
	parser.add_option("-g", "--gallery", dest="gallery", default="random",
	 				help="Specify a gallery to get images from")

	(options, args) = parser.parse_args()

	ImgurVaultBot.tweepy_authenticate()

	if options.exec_direct_messages:
		# Parse direct messages and exec their commands
		print "Exec direct messages!"
        elif options.gallery != "random":
                # Print images from specific gallery
                print "Printing " + options.number + " images from gallery " + options.gallery + "!"
	else:
		# just post random images
		ImgurVaultBot.tweet_random_image(int(options.number))


if __name__ == "__main__":
    main()
