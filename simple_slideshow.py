from __future__ import print_function

'''
Usage: python simple_slideshow.py [display_time] [random_order] [display_labels] [image_folder]
e.g.
>>> python simple_slideshow.py
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
'''

import os
import sys
import glob
import json
import shutil
import pyglet
import random
from distutils.util import strtobool

try:
    display_time = float(sys.argv[1])
except:
    display_time = 60
try:
    random_order = strtobool(sys.argv[2])
except:
    random_order = True
try:
    display_labels = strtobool(sys.argv[3])
except:
    display_labels = True
try:
    image_folder = sys.argv[4]
except:
    image_folder = os.path.join('static', 'live-slideshow')

def main():
    # Global variables shared with all functions
    global window
    global sprite
    global imgs
    global img_file
    global label
    global label_dict

    window = pyglet.window.Window(fullscreen=True)

    imgs = load_images()

    img_file = next(imgs)
    img = pyglet.image.load(img_file)
    sprite = pyglet.sprite.Sprite(img)
    scale = get_scale(img)
    sprite.scale = scale
    sprite.set_position(**center_coordinates(img, scale))

    if display_labels:
        label_dict = load_labels()
        label = make_label()

    pyglet.clock.schedule_interval(update_image, display_time)

    @window.event
    def on_draw():
        sprite.draw()
        if display_labels:
            label.draw()

    # Keyboard event handler
    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            save_as_favorite()

    pyglet.app.run()

def get_scale(image):
    if image.width > image.height:
        return window.width / image.width
    else:
        return window.height / image.height

def center_coordinates(image, scale):
    position = {}
    position['x'] = window.width/2 - scale*image.width/2
    position['y'] = window.height/2 - scale*image.height/2
    return position

def load_images():
    dir_files = glob.glob(os.path.join(image_folder, '*'))
    dir_imgs = [img for img in dir_files
                if img.endswith(('jpg', 'jpeg', 'png', 'gif'))]
    if random_order:
        random.shuffle(dir_imgs)
    return iter(dir_imgs)

def load_labels():
    caption_file = os.path.join(image_folder, 'captions.json')
    with open(caption_file, 'r') as f:
        label_dict = json.load(f)
    return label_dict

def update_image(dt):
    global imgs
    global label
    global img_file
    try:
        img_file = next(imgs)
    except StopIteration:
        # Re-load images
        imgs = load_images()
        img_file = next(imgs)
    img = pyglet.image.load(img_file)
    if display_labels:
        label = make_label()
    sprite.image = img
    scale = get_scale(img)
    sprite.scale = scale
    sprite.set_position(**center_coordinates(img, scale))
    window.clear()

def save_as_favorite():
    save_path = os.path.join(*('static', 'favorites',
                               os.path.split(img_file)[-1]))
    shutil.copyfile(img_file, save_path)

def make_label():
    label = label_dict.get(os.path.split(img_file)[-1], '')

    # Edit label to fit window better
    max_chars = 10
    line, split_label = '', []
    for word in label.split():
        line += '%s ' % word
        if len(line) > max_chars:
            split_label.append(line)
            line = ''
    split_label.append(line)
    label = '\n'.join(split_label)

    # Return label object
    return pyglet.text.Label(
              label,
              font_name='Cambria',
              font_size=6,
              bold=True,
              color=(255, 255, 255, 200),
              x=window.width/30, y=window.height/15*14,
              multiline=True,
              width=1000,
              dpi=300)

if __name__ == '__main__':
    main()
