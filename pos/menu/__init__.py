import wx

import pos

from .root import MenuRoot
from .item import MenuItem
from .menu import Menu

pos.config.set_default('menu', 'show_empty_root_items', '')
pos.config.set_default('menu', 'show_disabled_items', '')

main = None
il = None

def _loadImage(item):
    """
    Load item's image as wx.Bitmap and in an imagelist, that will be displayed in the main toolbook,
        based on its label and root label.
    That is the image at ./images/menu/root-item.png. Image size is 24x24.
    TODO That should change to be done with img2py.
    """
    global il
    try:
        item.bmp = wx.Bitmap(item.image_name, wx.BITMAP_TYPE_PNG)
        item.image = il.Add(item.bmp)
    except:
        print '-- ERROR --', 'Invalid image', item.image_name, 'for item', item.label
        raise

def init():
    """
    Create the main Menu instance to be used in the main frame.
    """
    global main
    main = Menu()

def load():
    """
    Load the complete image list of the menu.
    """
    global main, il
    il = wx.ImageList(24, 24, True)
    for item in main.items:
        for child in item.children:
            _loadImage(child)
        _loadImage(item)
