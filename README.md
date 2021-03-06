#The Imgur Vault Twitter Bot

Grabs a random image from Imgur and tweets it. You can see it in action at <a href="www.twitter.com/ImgurVault">www.twitter.com/ImgurVault</a>

##Direct message commands

This bot supports basic commands via Direct Messages, which are only able to be sent by specific users that ImgurVault follows (the admin group, if you will). The syntax is pretty simple, but there is only basic functionality at this time.

The general syntax is:
<blockquote>
<p>gallery [subreddit name] [random/top] [optional num]</p>

<p>random [optional num]</p>
</blockquote>

Here are some example commands:
<blockquote>
<p>gallery aww random 10</p>

<p>gallery pics top 5</p>

<p>gallery wtf top </p>

<p>random </p>

<p>random 5</p>
</blockquote>

If the image is labeled NSFW on the subreddit, it should be flagged as NSFW on the tweeted message as well. Of course, if people don't mark it as NSFW, there's not a whole lot one can do to warn others. 

##Notes

First and foremost, this program has absolutely no idea what it is posting. I more or less let the bot do its own thing aside from a few direct message commands here and there, and don't really moderate the images that are posted. Images could very well be NSFW (Not safe for work), offensive to some, or just plain odd. I take no responsibility for any of the images tweeted, since there is no way to check the content of the image without actually looking at it. So, be cautious. I make no claim of ownership for any of the images found and tweeted with this script. 

I encourage you to read through Imgur's Terms of Service <a href="http://imgur.com/tos">here</a> and see their stance on images containing any sort of offensive or illegal content. If you see an image that you believe violates these terms, please email <a href="mailto:abuse@imgur.com">abuse@imgur.com</a> and let the fine people at Imgur know.

Considering the posting of these images to Twitter for the public eye to see, please read Imgur's policy on intellectual property <a href="http://imgur.com/tos#dmca">here</a>, which includes the following:
<blockquote><p>By uploading a file ... you grant Imgur a non-exclusive, royalty- free, perpetual, irrevocable worldwide license (with sublicense and assignment rights) to use, to display online and in any present or future media, to create derivative works of, to allow downloads of, and/or distribute any file or other content you upload to our servers.</p></blockquote>

Lastly, this code verifies that the image exists by comparing the md5 hash of the image against Imgur's 404 image. If Imgur changes their 404 image, there's a good chance that this program will break and start posting invalid images. If you see this happening and this script isn't updated, please let me know on Github so I can fix it!

It seems that Imgur has updated their API to v2, so this will have to be updated shortly to reflect that before v1 is deprecated.
