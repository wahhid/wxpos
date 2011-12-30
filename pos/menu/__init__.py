import wx

from .root import MenuRoot
from .item import MenuItem
from .menu import Menu
from .module import ModuleMenuBase

menu = None
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
    global menu
    menu = Menu()

def load():
    """
    Load the complete image list of the menu.
    """
    global menu, il
    il = wx.ImageList(24, 24, True)
    for item in menu.items.itervalues():
        for child in item.children:
            _loadImage(child)
        _loadImage(item)

def getItems():
    """
    Return all the items of the main Menu instance.
    TODO Change that wherever it is used to directly get it from the Menu instance itself. 
    """
    global menu
    return menu.getItems()
