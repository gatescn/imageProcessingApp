# main script of image processing app
import importlib
import os
import sys
from datetime import datetime
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


def fileDirectoryCheck(path):
    return os.path.isdir(path)


if __name__ == '__main__':

    ImageFile.LOAD_TRUNCATED_IMAGES = True

    rawdirectory, outputdirectory, filters = read_config()

    files = os.listdir(rawdirectory)

    for file in files:
        filename = str(file)
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
            fullpath = os.path.join(pathDir + operationDefDirectory + f + "Definition.config")
            try:
                def_cont = open(fullpath).read()
            except OSError:
                print("Could not find definition file for:", fullpath)
                sys.exit()
            definitionParams = eval(def_cont)
            if issubclass(plugin, FilterPluginInterface):
                maskSize = int(definitionParams['maskSize'])
                maskWeight = float(definitionParams['filterWeight'])
                filteredImageData = plugin.performFilter(plugin, maskSize, maskWeight, raw_img)
            if issubclass(plugin, NoiseFilterPluginInterface):
                strength = int(definitionParams['strength'])
                filteredImageData = plugin.performFilter(plugin, strength, raw_img)
        filteredImage = Image.fromarray(filteredImageData)
        fulloutputdirectory = outputdirectory + "/" + f
        if fileDirectoryCheck(fulloutputdirectory):
            now = datetime.now()
            d = now.strftime("%m%d%Y%H_%M_%S")
            os.rename(fulloutputdirectory,outputdirectory+"/"+f+"_"+"History_"+d)
            os.mkdir(fulloutputdirectory)
            filteredImage.save(fulloutputdirectory+"/"+f+"_"+filename, "bmp")
        else:
            os.mkdir(fulloutputdirectory)
            filteredImage.save(fulloutputdirectory + "/" + f + "_" + filename, "bmp")
        print(file + " converted using " + f)
