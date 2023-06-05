import os, sys
from PIL import Image
from pathlib import Path
from states import *

class DMI:
    def __init__(self, filepath):
        self.filepath = filepath
        self.image = None
        self.swidth = 0
        self.sheight = 0
        self.states = []

    def load(self):
        self.image = Image.open(self.filepath)
        description = self.image.info["Description"].split('\n')
        if (description[1].split(" = ")[1] != "4.0"):
            sys.stderr.write("This package way created for dmi 4.0 files and may not work in this version.\n")

        self.swidth = int(description[2].split(" = ")[1])
        self.sheight = int(description[3].split(" = ")[1])
        self.states = []

        name = ""
        dirs = 1
        delays = []

        for text in description[4:-2]: #Exclude first line, last line and metadata.
            # If it's a new state
            if (text[0] != '\t'):
                if (len(name)):
                    if (len(delays) > 0):
                        self.states.append(DmiStateGIF(name, dirs, self, delays.copy()))
                    else:
                        self.states.append(DmiStatePNG(name, dirs, self))

                dirs = 1
                delays = []
                name = text[9:-1]
                continue

            # Get the good part
            now = text[1:].split(" = ")

            # If it's a delay we make a list of int out of it.
            if (now[0] == "delay"):
                delays = now[1].split(',')
                delays = [int(x) for x in delays]
            elif (now[0] == "dirs"):
                dirs = int(now[1])

        index = 0
        for state in self.states:
            state.load_from_dmi(index, self)
            index += state.get_image_count()

    def get_image(self, number):
        x = self.swidth * number % self.image._size[0]
        y = (self.swidth * number // (self.image._size[0]) * self.sheight)

        return self.image.crop((
                x, y,
                x + self.swidth-1, y + self.sheight-1))

    def unpack_all(self, outdir=""):
        index = 0
        if outdir == "":
            outdir = Path("out", self.filepath.stem)
        if (not (outdir.exists())):
            outdir.mkdir(parents=True)
        for state in self.states:
            state.unpack(outdir)
            index += state.get_image_count()
