# main script of image processing app
import importlib
import os
import sys

from PIL import Image, ImageFile
from pluginfiles.plugin import registeredFilters
from pluginfiles.plugin import FilterPluginInterface, NoiseFilterPluginInterface


# reads config file
def read_config():
    filename = "external.config"
    try:
        contents = open(filename).read()
    except OSError:
        print("Could not find file:", filename)
        sys.exit()
    filters_ = []
    config = eval(contents)
    rawimagedirectory = config['imageDirectory']
    processedimagedirectory = config['outputDirectory']
    for fp in config['filtersToApply']:
        if isRegisteredFilter(fp):
            filters_.append(fp)
    return rawimagedirectory, processedimagedirectory, filters_


def isRegisteredFilter(name):
    for rf in registeredFilters:
        if rf == name:
            return True

    return False


if __name__ == '__main__':

    ImageFile.LOAD_TRUNCATED_IMAGES = True

    rawdirectory, outputdirectory, filters = read_config()

    files = os.listdir(rawdirectory)

    for file in files:
        filepath = rawdirectory + "/" + file
        # the raw image
        raw_img = Image.open(filepath).convert('L')
        image_copy = raw_img.copy()
        for f in filters:
            moduleName = "pluginfiles." + f
            module = importlib.import_module(moduleName)
            plugin = getattr(module, f)
            operationDefDirectory = "/operationDefinitionRepository/"
            pathDir = os.path.dirname(__file__)
            fullpath = os.path.join(pathDir+operationDefDirectory+f+"Definition.config")
            try:
                def_cont = open(fullpath).read()
            except OSError:
                print("Could not find definition file for:", fullpath)
                sys.exit()
            definitionParams = eval(def_cont)
            if issubclass(plugin, FilterPluginInterface):
                maskSize = int(definitionParams['maskSize'])
                maskWeight = float(definitionParams['filterWeight'])
                plugin.performFilter(plugin, maskSize, maskWeight, raw_img)
            if issubclass(plugin, NoiseFilterPluginInterface):
                strength = int(definitionParams['strength'])
                plugin.performFilter(plugin, strength, raw_img)
        filterName = str(filter.__name__)
        print(file+" converted using "+f)

