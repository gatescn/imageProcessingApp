# main script of image processing app
import os
import random
from PIL import Image, ImageFile


class SaltAndPepperFilter:

    trashcan = []

    def setstrength(self):
        if self.strength == 1:
            self.strength = (-1, 0, 0, 1)
            return
        if self.strength == 2:
            self.strength = (-1, -1, 0, 1, 1)
            return
        self.strength = (-1,0,0,0,0,0,0,0,0,0,0,0 ,1)
        return

    def __init__(self, strength, matrix):
        self.strength = strength
        self.imgMatrix = matrix
        self.setstrength()

    def performfilter(self):
        for r, rows in enumerate(self.imgMatrix):
            for c, col in enumerate(rows):
                pixelvalue = self.computevalue(col)
                self.imgMatrix[r][c] = pixelvalue

    def computevalue(self, currentpixel):
        decider = random.randint(0, len(self.strength) - 1)
        choice = self.strength[decider]
        if choice == -1:
            # salt
            currentpixel = 0
        if choice == 1:
            # pepper
            currentpixel = 255
        return currentpixel


# reads config file
def read_config():
    filename = "external.config"
    contents = open(filename).read()
    config = eval(contents)
    rawimagedirectory = config['imageDirectory']
    processedimagedirectory = config['outputDirectory']
    return rawimagedirectory, processedimagedirectory


if __name__ == '__main__':
    imageDictionary = {}
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    rawdirectory, outputdirectory = read_config()
    files = os.listdir(rawdirectory)
    index = 0
    for file in files:
        index += 1
        filepath = rawdirectory + "/" + file
        # the raw image
        rawimg = Image.open(filepath)
        # copy of the raw image
        newimgdata = []
        # create copy of raw image data into editable lists.
        data = list(rawimg.getdata())
        for t in data:
            tempList = []
            for i in t:
                tempList.append(i)
            newimgdata.append(tempList)
        width = rawimg.width
        height = rawimg.height
        s = SaltAndPepperFilter(1, newimgdata)
        s.performfilter()
        newimgdatafinal = []
        for s in newimgdata:
            tuplelist = tuple(s)
            newimgdatafinal.append(tuplelist)
        newImg = Image.new(rawimg.mode, rawimg.size)
        newImg.putdata(newimgdatafinal)
        newImg.save(outputdirectory + "/" + file)
        break
