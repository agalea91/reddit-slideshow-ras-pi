from __future__ import print_function

'''
Usage: python update_images.py [how] [url] [N_pictures]
e.g.
>>> python update_images.py
>>> python update_images.py add https://www.reddit.com/r/Animewallpaper/ 5

how : str
    What to do with newly discovered images.
        add - save to live-slideshow with other images
        replace - save to live-slideshow in place of other images
    Note: all images will be archived upon saving in the archive_path.

url : str
    Reddit webpage to download images from.

N_pictures : int
    Number of pictures to attempt to save from webpage.
'''

import re
import os
import sys
import glob
import time
import json
import shutil
import datetime
import requests
from PIL import Image
from bs4 import BeautifulSoup

date = datetime.datetime.now().strftime('%d_%m_%Y')

def main():
    # Define variables / parse arguments
    try:
        how = sys.argv[1]
    except:
        how = 'add'
    try:
        url = sys.argv[2]
    except:
        url = 'https://www.reddit.com/r/pics/top/?sort=top&t=day'
    try:
        N_pictures = int(sys.argv[3])
    except:
        N_pictures = 10
    temp_path = os.path.join('static', '.temp')
    archive_path = os.path.join('static', 'archive')
    live_path = os.path.join('static', 'live-slideshow')

    print('*** %s ***' % url)
    print('-'*len('*** %s ***' % url))

    # Attempt to save images from reddit webpage
    save_top_images(url, N_pictures, temp_path)

    # How many did we get?
    search_cmd = os.path.join(temp_path, '*')
    num = len([f for f in glob.glob(search_cmd) if f.split('.')[-1] in
                                            ('jpg', 'jpeg', 'png', 'gif')])
    print('*** saved %d picture(s) ***' % num, end='\n\n')

    # Replace photo caption dictionary in live-slideshow folder
    if how == 'replace':
        clean_captions(os.path.join(live_path, 'captions.json'))

    # Backup pictures and captions
    files = glob.glob(os.path.join(temp_path, '*'))
    copy(files, archive_path)

    # Move images and captions from temporary save folder
    # to live-slideshow folder
    organize_images(how, files, live_path)
    write_paths_to_file(live_path)


def save_top_images(url, N_pictures, save_path, attempts=0):
    ''' Save the top images on a reddit.com page to your
    local machine.

    url : str
        Reddit URL from which to find pictures.

    N_pictures : int
        Number of pictures to (attempt to) save.

    save_path : str
        Where to save images on local machine.
    '''

    page = requests.get(url)
    # Make sure the page loded properly

    if page.status_code != 200:
        _attempts = attempts + 1
        if _attempts < 10:
            # Wait and try again
            time.sleep(3)
            save_top_images(url, N_pictures, save_path, _attempts)

    soup = BeautifulSoup(page.content, 'html.parser')

    elements = soup.findAll('p', {'class': 'title'})
    urls = [e.findAll('a')[0]['href']
            for e in elements]
    captions = [e.findAll('a')[0].text
                for e in elements]

    labels = {} # keep track of the saved image captions
    i = 0
    for u, c in zip(urls, captions):
        f_type = u.split('.')[-1]
        if f_type not in ('jpg', 'jpeg', 'png', 'gif'):
            f_type = 'jpg'
        f_category = re.findall('^.*/r/([^/]*)', url)[0]
        f_name = '%s_%d_%s.%s' % (f_category, i+1, date, f_type)
        f_path = os.path.join(save_path, f_name)
        f = open(f_path, 'wb')
        try:
            print('%s ...' % u, end=' ')
            if u.endswith(('jpg', 'jpeg', 'png', 'gif')) or 'reddituploads' in u:
                img = requests.get(u)
            else:
                if 'imgur' in u:
                    # Try to find img url (by looking in first img element)
                    page_ = requests.get(u)
                    u_ = 'http:' + BeautifulSoup(page_.content, 'html.parser')\
                        .findAll('img')[0]['src']
                    print('%s ...' % u_, end=' ')
                    img = requests.get(u_)
                else:
                    raise Exception
            f.write(img.content)
            f.close()
            try:
                with Image.open(f_path) as test:
                    # The image has been validated
                    i += 1
                    labels[f_name] = c
                print('success')
            except OSError as e:
                print('cannot open image')
                os.remove(f_path)
        except:
            print('cannot open URL')
            # Clean up if needed
            if os.path.exists(f_path):
                try:
                    f.close()
                    #os.remove(f_path)
                except:
                    pass
                os.remove(f_path)
        if i >= N_pictures:
            break

    with open(os.path.join(save_path, 'captions.json'), 'w') as f:
        json.dump(labels, f)

def copy(files, save_path_final, clean=False):
    # Deal with the captions
    caption_file = [f for f in files if f.split('/')[-1] == 'captions.json']
    if caption_file:
        update_captions(caption_file[0],
                        os.path.join(save_path_final, 'captions.json'))

    # Deal with the images
    files_ = [f for f in files if f.split('/')[-1] != 'captions.json']
    for f in files_:
        f_ = f.split('/')[-1]
        f_ = os.path.join(save_path_final, f_)
        if clean:
            os.rename(f, f_)
        else:
            shutil.copyfile(f, f_)

def update_captions(dict_path_start, dict_path_final):
    with open(dict_path_start) as f:
        dict_start = json.load(f)

    try:
        with open(dict_path_final) as f:
            dict_final = json.load(f)
    except:
        # The file probably doesn't exist
        dict_final = {}

    with open(dict_path_final, 'w') as f:
        # json.dump({**dict_start, **dict_final}, f) # python 3 only!
        dict_ = dict_start.copy()
        dict_.update(dict_final)
        return dict_


def clean_captions(dict_path):
    with open(dict_path, 'w') as f:
        json.dump({}, f)

def organize_images(how, files, save_path_final):
    if how == 'add':
        copy(files, save_path_final, clean=True)

    elif how == 'replace':
        # Remove old files
        live_files = glob.glob(os.path.join(save_path_final, '*'))
        for f in live_files:
            os.remove(f)
        # Move from temp
        copy(files, save_path_final, clean=True)

def write_paths_to_file(path):
    files = glob.glob(os.path.join(path, '*'))
    imgs = [f for f in files if f.split('.')[-1] in
            ('jpg', 'jpeg', 'png', 'gif')]
    with open(os.path.join(path, 'image_paths.txt'), 'w') as f:
        for img in imgs:
            f.write(img+'\n')

if __name__ == '__main__':
    main()
