from __future__ import print_function

'''
Usage: python get_reddit_images.py [how] [reddit_urls] [N_pictures]
e.g.
>>> python  get_reddit_images.py
>>> python  get_reddit_images.py add reddit_urls.csv 10

how : str
    What to do with newly discovered images.
        add - save to live-slideshow with other images
        replace - save to live-slideshow in place of other images
    Note: all images will be archived upon saving in the archive_path.

reddit_urls : str
    Path to list of reddit pages from which to get images. One URL per line
    and no commas.

N_pictures : int
    Number of pictures to attempt to save from each webpage.
'''

import os
import sys

# Define variables / parse arguments
try:
    how = sys.argv[1]
except:
    how = 'replace'
try:
    reddit_urls_file = sys.argv[2]
except:
    reddit_urls_file = 'reddit_urls.csv'
try:
    N_pictures = int(sys.argv[3])
except:
    N_pictures = 1

def main():
    global how
    reddit_urls = open(reddit_urls_file).read().splitlines()
    reddit_urls = [url for url in reddit_urls if url]

    for url in reddit_urls:
        update_images(url, how, N_pictures)
        how = 'add' # Start adding photos after the initial update

def update_images(url, how, N_pictures):
    cmd = 'python update_images.py %s "%s" %d' % (how, url, N_pictures)
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    main()
