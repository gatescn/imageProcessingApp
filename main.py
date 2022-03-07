# main script of image processing app
import os

from pluginfiles.plugin import FilterPluginInterface
from PIL import Image, ImageFile
import numpy as np

from pluginfiles.GaussianNoiseFilter import GaussianNoiseFilter
from pluginfiles.LinearFilter import LinearFilter
from pluginfiles.MedianFilter import MedianFilter
from pluginfiles.img_histogram import img_histogram

imageDictionary = {}

#each filters needs to create a img copy, similat to how it's done in the slides.
#img.copy, blank array for imagae data, filter and add img data to empty array.
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

if __name__ == '__main__':

    ImageFile.LOAD_TRUNCATED_IMAGES = True

    rawdirectory, outputdirectory, filters = read_config()

    files = os.listdir(rawdirectory)

    fileindex = 0

    for file in files:
        fileindex += 1
        filepath = rawdirectory + "/" + file
        # the raw image
        raw_img = Image.open(filepath).convert('L')
        image_copy = raw_img.copy()
        img_histogram = img_histogram(raw_img, False)
        img_histogram.cretateHistogram()
        #lf = MedianFilter(1, 1, image_copy)
        #filtered_image_data = lf.performfilter()
        #im = Image.fromarray(filtered_image_data)
        #im.show("test")
        break;
