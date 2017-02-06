# Reddit picture live slideshow

Continuous slideshow of reddit pictures from your favorite subreddits. For your desktop or raspberry PI. Requires python 2 or 3 and the following external library dependencies: `shutil, requests, beautifulsoup4, Pillow, and pyglet`.

You may want to create a virtual environment to install them in. After [downloading this repository](https://github.com/agalea91/reddit-slideshow-ras-pi/archive/master.zip), the installation can be done with pip. On Unix systems you can do
```
git clone https://github.com/agalea91/reddit-slideshow-ras-pi
cd reddit-slideshow-ras-pi
pip install --upgrade -r requirement.txt
```
If on Windows, you can install the libraries by navigating to the downloaded repository and running the final line above.

The tool, which downloads pictures from reddit and then displays them in a slideshow, should be run in two steps. First navigate to the project directory and run
```
python get_reddit_images.py
```
The script will request to download URLs from the list of subreddits in the reddit_urls.csv file. You can add your favorites.

Once the script is complete you can start the slideshow with

```
python simple_slideshow.py
```

Save pictures you like by pressing the `enter` key. Quit the slideshow with `escape`.
___

To customize your slideshow you include arguments when running she scripts.

```
python get_reddit_images.py [how] [reddit_urls] [N_pictures]
e.g.
>>> python  get_reddit_images.py remove reddit_urls.csv 3

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


python simple_slideshow.py [display_time] [random_order] [display_labels] [image_folder]
e.g.
>>> python simple_slideshow.py 5 False False static/archive

display_time : int
    Time in seconds to display each picture for. Default is 60.
    Image are cycled continuously until script is terminated. Press
    escape key to stop slideshow.

random_order : bool
    Display images in random order if True. Otherwise sort them.

display_labels : bool
    Overlay labels on photos. Labels are read from captions.json -
    a dictionary where keys are image files names.

image_folder : str
    Path to images. Default is static/live-slideshow.
```
___

The `simple_slideshow` script can run continuously. The `reddit_urls.csv` file currently has URLs for the top daily content (as per the parameters at the end or each URL). As such, it can be run daily for new content. On Unix, this could be done with a cron job:

insert example
