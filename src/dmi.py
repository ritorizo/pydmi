import os, sys
import glob
from PIL import Image
from pathlib import Path
from states import *

# Where to pull the icons from
icon_folder=Path("/home/ritorizo/note/ss13/Shiptest/icons")

# Where to output them
out_folder=Path("/home/ritorizo/note/ss13/pydmi/src/out")

# For the dmi which have some janky state name.
blacklist= [
    "obj/status_display.dmi",     
    "effects/crayondecal.dmi",
    "hud/screen_gen.dmi",
    "mob/robots.dmi"
    ]

stfu = False #Self explanatory

class DMI:
    def __init__(self, filepath):
        self.filepath = filepath
        self.image = None
        self.swidth = 32
        self.sheight = 32
        self.states = {}

    def load(self):
        self.image = Image.open(self.filepath)
        description = self.image.info["Description"].split('\n')
        if (description[1].split(" = ")[1] != "4.0"):
            sys.stderr.write("This package way created for dmi 4.0 files and may not work in this version.\n")

        index = 2
        while(description[index][0] == '\t'):
            stuff = description[index][1:].split(" = ")
            if (stuff[0] == "width"):
                self.swidth = int(stuff[1])
            elif (stuff[0] == "height"):
                self.sheight = int(stuff[1])
            index += 1



        self.states = {}

        name = ""
        dirs = 1
        delays = []

        for text in description[4:-2]: #Exclude first line, last line and metadata.
            # If it's a new state
            if (text[0] != '\t'):
                if (len(name)):
                    if (len(delays) > 0):
                        self.states[name] = DmiStateGIF(name, dirs, self, delays.copy())
                    else:
                        self.states[name] = DmiStatePNG(name, dirs, self)

                dirs = 1
                delays = []
                name = text[9:-1]
                continue

            # Get the good part
            now = text[1:].split(" = ")

            # If it's a delay we make a list of int out of it.
            if (now[0] == "delay"):
                delays = now[1].split(',')
                delays = [float(x) for x in delays]
            elif (now[0] == "dirs"):
                dirs = int(now[1])

        index = 0
        for key in self.states:
            self.states[key].load_from_dmi(index, self)
            index += self.states[key].get_image_count()

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
        for key in self.states:
            self.states[key].unpack(outdir)
            index += self.states[key].get_image_count()

if __name__=="__main__":
    cwd = os.getcwd()
    os.chdir(icon_folder)

    to_convert = glob.glob("**/*.dmi")

    # Nome It won't create a file named ".png" or "&.gif"
    for yeet in blacklist:
        to_convert.remove(yeet)
    
    os.chdir(cwd)

    for file in to_convert:
        print("processing", file)
        dmi = DMI(Path(icon_folder) / file)
        dmi.load()
        dmi.unpack_all(Path(out_folder) / file)
        del(dmi)
