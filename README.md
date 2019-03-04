# calvin-hobbes-web-scraper
Python script for scraping the Calvin &amp; Hobbes comic strips being hosted on the [GoComics website](https://www.gocomics.com/calvinandhobbes/1985/11/18)

I wrote this to get image data for a hackathon project back in 2017

To use:
- Clone this repository
- Open `calvinWebCrawler.py`
- Set `data_dir` to the directory path where you want the images to be saved
- Run `python calvinWebCrawler.py --verbose`

Troubleshooting:
- You might need to increase the wait time between requests to prevent your IP address from getting blocked
- That line looks like this: `time.sleep(2)`

This script was working as of March 2019, but the structure of the GoComics website could change at any time and cause this script to fail

**Update:** I recently learned about `robots.txt` files, and the one for GoComics says
```
User-agent: *
Disallow:
```

Pretty sure that means they don't want scripts scraping their website, so take that into account before using (or not using) this thing
