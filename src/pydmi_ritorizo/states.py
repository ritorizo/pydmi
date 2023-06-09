# Delay in 1/10th of a second
from PIL import Image
from pathlib import Path
DMI_DELAY_UNIT_DURATION = 100

class DmiState:
    def __init__(self, name, dirs, dmi):
        """
        :param name: The name of the dmi state.
        :param dirs: the number of dirrection the state have (1, 4 or 8).
        """
        self.name = name
        self.dirs = dirs
        self.frames = 1
        self.dirrection = {} # A dictionary of sprites by dirrection.
        self.extention = ""

        # The DMI this state is a part of.
        self.dmi = dmi

    def __str__(self):
        return self.name

    def get_image_count(self):
        """
        return: The number of frames this state have (frames * number of dirrection)
        """
        return self.dirs * self.frames

    def load_from_dmi(self, index, dmi):
        """
        param: index: The image index at wich the state start.
        param: dmi: The dmi class from wich import the images.
        """
        pass
            
    def unpack(self, outdir, dirrections={}):
        """
        param: outdir: The directory where all the state is gonna be outputed.
        A pathlib path.
        param: dirrection (optional) : an iterable object containing the dirrection of the 
        state to take (ex ["noth"], ["south", "east", "north_east"]) print all directions if left blank
        """
        if (not (outdir).exists()):
            (outdir).mkdir(parents=True)

    def get_default_sprite(self):
            return self.dirrection[self.get_default_dir]

    def get_default_dir(self):
        return "north"

class DmiStateGIF(DmiState):
    def __init__(self, name, dirs, dmi, delays):
        super().__init__(name, dirs, dmi)
        self.frames = len(delays) 
        self.delays = delays
        self.extention = ".gif"

    def load_from_dmi(self, index, dmi):
        for orientation in get_direction_list(self.dirs):
            self.dirrection[orientation] = []
        for i in range(self.frames):
            for orientation in self.dirrection:
                self.dirrection[orientation].append(dmi.get_image(index))
                index += 1
        return self.dirrection


    def unpack(self, outdir, dirrections=[], separate_frames=False):
        super().unpack(outdir)
        print(dirrections)
        if (len(dirrections) == 0):
            dirrections = self.dirrection
        for orientation in dirrections:
            if(separate_frames):
                for i in range(len(self.dirrection[orientation])):
                    self.dirrection[orientation][i].save(
                            fn = outdir / (self.name+orientation+"_"+str(i)+".png"),
                            format="PNG"
                            )
            else:
                self.dirrection[orientation][0].save(
                        outdir / (self.name+orientation+".gif"),
                        format="GIF",
                        save_all=True,
                        disposal = 2,
                        transparency=0,
                        loop=0,
                        append_images = self.dirrection[orientation][1:],
                        duration=list(map((lambda x : x*DMI_DELAY_UNIT_DURATION), self.delays))
                    )

class DmiStatePNG(DmiState):
    def __init__(self, name, dirs, dmi):
        super().__init__(name, dirs, dmi)
        self.extention = ".png"

    def load_from_dmi(self, index, dmi):
        for orientation in get_direction_list(self.dirs):
            self.dirrection[orientation] = dmi.get_image(index)
            index += 1
        return self.dirrection

    def unpack(self, outdir, dirrections=[]):
        super().unpack(outdir)
        if (len(dirrections) == 0):
            dirrections = self.dirrection
        for orientation in dirrections:
            self.dirrection[orientation].save(
                    outdir / (self.name+orientation+".png"), 
                    "PNG"
                )

def get_direction_list(number):
    value = []
    if (number > 1):
        value += ["north", "south", "east", "west"]
    if (number > 4):
        value += ["northeast", "northwest", "southeast", "southwest"]

    if (len(value) == 0):
        value = ["north"]

    return value 
