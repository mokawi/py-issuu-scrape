# Issuu Scraper (Python)

Basic Issuu scraper, and since I'm not an expert at Python, this is a simple script and nothing advanced or special. It still does the trick though. :) Enter the url, and then enter the number of pages the book has. The program will then do the rest by downloading each image, compiling into a pdf, and outputting the urls and information in separate text files.

## Usage

    python3 ./issuu.py <url> [output path] [-f format] [--list-format]

The script will prompt you to enter Issuu item's URL and page count.

## Requirements

<<<<<<< HEAD
This script requires Python 3 and the package Beautiful Soup. To install the required packages:
=======
This script requires Python 3, and the package Beautiful Soup. To install the required packages:
>>>>>>> 9389d119ab81228fd58701bc5779ef0f438b8bc1

    pip install bs4

## Credits

This script was inspired and is based on the Ruby script from pietrop: https://github.com/pietrop/issuu.com-downloader
