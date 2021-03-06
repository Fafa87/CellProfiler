import os.path
import sys
import weakref

if hasattr(sys, "frozen"):
    path = os.path.split(os.path.abspath(sys.argv[0]))[0]

    path = os.path.join(path, "artwork")
else:
    path = os.path.join(os.path.dirname(os.path.dirname(__path__[0])), "artwork")

image_cache = weakref.WeakValueDictionary()


def get_builtin_image(name):
    import wx

    try:
        return image_cache[name]
    except KeyError:
        image_cache[name] = image = wx.Image(os.path.join(path, name + ".png"))

        return image


def get_builtin_images_path():
    return os.path.join(path, '')
