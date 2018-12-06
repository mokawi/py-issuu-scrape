#!/usr/bin/python3

from bs4 import BeautifulSoup
import sys
import os
import urllib.request
import re
import subprocess
import argparse
import json

__version__ = "0.2mok"

def get_metadata(soup):
    "Gets metadata from javascript declaration."

    # Get the right script node:
    scriptnode = soup.find("script", string=re.compile(r"__INITIAL_STATE__"))

    # Select the json data
    metadata = re.search(
            r"window\.__INITIAL_STATE__\s+=\s+({.+});",
            scriptnode.contents[0]
        ).group(1)

    # Parse and return
    return json.loads(metadata)

def scrape(url, output_path, filetype="jpg"):
    "Scrapes a issuu document in a given path."
    webpage = urllib.request.urlopen(url)
    soup = BeautifulSoup(webpage, "html.parser")

    # Get relevant metadata
    metadata = get_metadata(soup)

    howmanypages = metadata["document"]["pageCount"]
    pagetitle = metadata["document"]["title"]
    # pagetitle = soup.find('meta', attrs={'property': 'og:title'})['content']
    description = metadata["document"]["description"]
    # description = soup.find('meta', attrs={'property': 'og:description'})['content']
    username = metadata["publisher"]["username"]
    uploadername = metadata["publisher"]["displayName"]
    uploaded = metadata["document"]["originalPublishDate"]
    # uploaded = soup.find('div', attrs={'class': 'DocumentInfo__date--2llaY'})['datetime']

    # Download pages
    for page in range(1, howmanypages + 1):

        firstpagelnk = soup.find('meta', attrs={'property': 'og:image'})['content']
        imglink = re.sub("1.jpg$", "%d.jpg" % page, firstpagelnk)
        getimg = urllib.request.urlretrieve(imglink, "page_%0{}d.jpg".format(len(str(howmanypages))) % page)
        print('Page %d: %s' % (page, imglink))

        myfile = open('urls.txt', 'a')
        myfile.write("%s\n" % imglink)
        myfile.close()

        if filetype == "pdf":

    # Make info.txt file
    url_out = "URL: " + url
    desc_out = "Description: " + description
    upload_out = "Uploaded: " + uploaded
    uploadlink_out = "Uploader link: " + "https://issuu.com/" + username
    uploader_out = "Uploader: " + uploadername

    myfile2 = open('info.txt', 'w')
    myfile2.write(url_out + "\n" +uploader_out + "\n" + uploadlink_out + "\n" + desc_out + "\n" + upload_out)
    myfile2.close()

    # If format is pdf, convert everything in a single pdf file.
    if filetype == "pdf":
        params = ['convert', 'page_*.jpg', pagetitle + '.pdf']
        subprocess.check_call(params)
        os.system('rm page_*.jpg')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Downloads all pages from a Issuu file."
    )

    parser.add_argument("--list-formats", "-F", action="store_true", default=False, help="Lists available output formats.")
    parser.add_argument("url", type=str, help="URL of the Issuu document.")
    parser.add_argument("--output-path", "-o", type=str, nargs=1, default=os.getcwd(), help="Path where the image files are to be downloaded.")
    parser.add_argument("--format", "-f", default="jpg", help="Output format for image files.")

    args = parser.parse_args()

    if args.list_formats:
        print("jpg\tJPEG image files (default)")
        print("pdf\tPDF files")
        exit()

    scrape(args.url, args.output_path, args.format)
    print("Done!")
