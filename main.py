#main script of image processing app
import os
from PIL import Image

#reads config file
def read_config():
    filename = "external.config"
    contents = open(filename).read()
    config = eval(contents)
    rawimagedirectory = config['imageDirectory']
    processedimagedirectory = config['outputDirectory']
    return rawimagedirectory, processedimagedirectory

if __name__ == '__main__':
    imageDictionary = {}
    rawdirectory,outputdirectory = read_config()
    files = os.listdir(rawdirectory)
    for file in files:
        filepath = rawdirectory+"/"+file
        rawimg = Image.open(filepath)
        newimg = rawimg
        data = list(rawimg.getdata())
        #operations here....
        newimg.save(outputdirectory+"/"+file)
        break
