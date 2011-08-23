import wx

from .root import MenuRoot
from .item import MenuItem
from .menu import Menu
from .module import ModuleMenuBase

menu = None
il = None

def _loadImage(item):
    global il
    try:
        item.bmp = wx.Bitmap(item.image_name, wx.BITMAP_TYPE_PNG)
        item.image = il.Add(item.bmp)
    except:
        print '-- ERROR --', 'Invalid image', item.image_name, 'for item', item.label
        raise

def init():
    global menu
    menu = Menu()

def load():
    global menu, il
    il = wx.ImageList(24, 24, True)
    for item in menu.items.itervalues():
        for child in item.children:
            _loadImage(child)
        _loadImage(item)

def getItems():
    global menu
    return menu.getItems()
