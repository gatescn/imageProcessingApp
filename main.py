# main script of image processing app
import os
from PIL import Image, ImageFile
from pluginfiles.plugin import FilterPluginInterface

imageDictionary = {}


class pluginimporter:
    def isfilterplugin(self):
        return issubclass(self.attribute, FilterPluginInterface)

    def __init__(self, modulename, classname):
        self.module = __import__(modulename)
        self.attribute = getattr(self.module, classname)


# reads config file
def read_config():
    filename = "external.config"
    contents = open(filename).read()
    filters = []
    config = eval(contents)
    rawimagedirectory = config['imageDirectory']
    processedimagedirectory = config['outputDirectory']
    for f in config['filters']:
        filters.append(f)

    return rawimagedirectory, processedimagedirectory, filters


def copyimagedata(d):
    newimgdata = []
    for t in d:
        tempList = []
        for i in t:
            tempList.append(i)
        newimgdata.append(tempList)
    return newimgdata


def finalizeimagedata(d):
    datafinal = []
    for s in d:
        tuplelist = tuple(s)
        datafinal.append(tuplelist)
    return datafinal


def createnewimg(mode, size, d):
    newimg = Image.new(mode, size)
    newimg.putdata(d)
    return newimg


def getimagedata(img):
    d = list(img.getdata())
    w = img.width
    h = img.height
    return d, w, h


def addtohistory(index, img):
    dictkey = "img" + str(index)
    imageDictionary[dictkey] = img


if __name__ == '__main__':

    ImageFile.LOAD_TRUNCATED_IMAGES = True

    rawdirectory, outputdirectory, filters = read_config()

    files = os.listdir(rawdirectory)

    fileindex = 0

    for file in files:
        fileindex += 1
        filepath = rawdirectory + "/" + file
        # the raw image
        rawimg = Image.open(filepath)
        data, width, height = getimagedata(rawimg)
        print(fileindex)
