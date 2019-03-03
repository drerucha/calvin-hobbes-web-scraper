import os
import time
import shutil
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta


class CalvinAndHobbesWebCrawler(object):
    """
    Simple class for scraping the Calvin & Hobbes comic strips being hosted on the GoComics website
    """
    #: YOU NEED TO SET THIS!
    #: Path to directory where you want the comic strips to be saved. Ex: '/Users/drerucha/Pictures/calvin_and_hobbes/'
    data_dir = ''

    #: Base URL where the comic strips are being hosted
    root_url = 'http://www.gocomics.com/calvinandhobbes/'
    #: Image format of the hosted comic strips
    image_extension = 'gif'
    # Date the first Calvin & Hobbes comic strip was published
    default_start_date = date(1985, 11, 18)
    # Date the last Calvin & Hobbes comic strip was published
    default_end_date = date(1995, 12, 31)

    def go(self, start_date=None, end_date=None):
        """
        Kicks off the scraping process. Downloads the Calvin & Hobbes strips published between start_date and end_date,
        and saves them as separate images in data_dir. File names will have the following format: YYYY_MM_DD.gif

        Ex: 1985_11_18.gif

        :param start_date: the first date in the date range to scrape (optional)
        :type start_date: datetime.date
        :param end_date: the last date in the date range to scrape (optional)
        :type end_date: datetime.date
        """
        # If no date parameters are specified, then the entire Calvin & Hobbes catalog will be downloaded by default
        start_date = self.default_start_date if start_date is None else start_date
        end_date = self.default_end_date if end_date is None else end_date

        # Iterate through the date range one day at a time
        delta = end_date - start_date
        for i in range(delta.days + 1):
            curr_date = start_date + timedelta(days=i)

            # Construct the path where we'll save the image that we're about to download
            file_name = "%04d_%02d_%02d" % (curr_date.year, curr_date.month, curr_date.day)
            save_path = os.path.join(self.data_dir, "%s.%s" % (file_name, self.image_extension))

            # If the file already exists, then skip the current date because the strip has already been downloaded
            if os.path.exists(save_path):
                continue

            # Generate the URL where the strip can be found. Ex: https://www.gocomics.com/calvinandhobbes/1985/11/18
            strip_url = os.path.join(self.root_url, str(curr_date.year), str(curr_date.month), str(curr_date.day))

            # Extract the image URL from the web page
            image_url = self.src_image(strip_url)

            # If we were able to extract the image URL, then download and save the image
            if image_url:
                self.download_image(url=image_url, path=save_path)
                print("downloaded comic strip at %s" % strip_url)
            else:
                print("unable to download comic strip at %s" % strip_url)

            # Pause for 2 seconds between requests so that GoComics doesn't block our IP address
            time.sleep(2)

    @staticmethod
    def src_image(url):
        """
        Requests and parses the data at the given website URL. Tries to locate a specific piece of data within the HTML
        that represents a comic strip image.

        :param url: the website URL we want to scrape
        :type url: string
        :return: URL of the comic strip image or None if the image cannot be found
        """
        # Fetch the data at the given URL
        r = requests.get(url)

        # If the request was successful...
        if r.status_code == 200:
            # Parse the website's HTML
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                # Return the URL to the comic strip image if we can find it
                return soup.find('picture', {'class': 'item-comic-image'}).img['src']
            except KeyError:
                print("unable to extract src image for %s" % url)

        # Return a null value if we were unable to locate the comic strip image
        return None

    @staticmethod
    def download_image(url, path):
        """
        Downloads the image being hosted at the given URL and saves a local copy of the image at the given path

        :param url: the image URL we want to download
        :type url: string
        :param path: the file path where we want to save the downloaded image
        :type path: string
        """
        # Fetch the data at the given URL
        r = requests.get(url, stream=True)
        # Create the file where we want to save the image
        with open(path, 'wb') as out_file:
            # Copy the image contents into our new local file
            shutil.copyfileobj(r.raw, out_file)


if __name__ == '__main__':
    import sys
    import traceback
    try:
        crawler = CalvinAndHobbesWebCrawler()
        crawler.go()
    except SystemExit:
        raise
    except:
        if '--verbose' in sys.argv:
            traceback.print_exc(sys.stderr)
        else:
            sys.stderr.write("Error: %s\n" % sys.exc_info()[1])
        exit(1)
