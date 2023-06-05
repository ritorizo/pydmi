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

        # The DMI this state is a part of.
        self.dmi = dmi

    def __str__(self):
        return self.name

    def get_image_count(self):
        return self.dirs * self.frames

    def load_from_dmi(self, index, dmi):
        pass
            
    def unpack(self, outdir, dirrections={}):
        if (not (outdir).exists()):
            (outdir).mkdir(parents=True)

class DmiStateGIF(DmiState):
    def __init__(self, name, dirs, dmi, delays):
        super().__init__(name, dirs, dmi)
        self.frames = len(delays) 
        self.delays = delays

    def load_from_dmi(self, index, dmi):
        for orientation in get_direction_list(self.dirs):
            self.dirrection[orientation] = []
            for i in range(self.frames):
                self.dirrection[orientation].append(dmi.get_image(index))
                index += 1
        return self.dirrection

    def unpack(self, outdir, dirrections={}, separate_frames=False):
        super().unpack(outdir)
        if (len(dirrections) == 0):
            dirrections = self.dirrection
        for orientation in self.dirrection:
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
                        append_images = self.dirrection[orientation][1:],
                        duration=list(map((lambda x : x*DMI_DELAY_UNIT_DURATION), self.delays))
                    )

class DmiStatePNG(DmiState):
    def load_from_dmi(self, index, dmi):
        for orientation in get_direction_list(self.dirs):
            self.dirrection[orientation] = dmi.get_image(index)
            index += 1
        return self.dirrection

    def unpack(self, outdir, dirrections={}):
        super().unpack(outdir)
        if (len(dirrections) == 0):
            dirrections = self.dirrection
        for orientation in dirrections:
            self.dirrection[orientation].save(
                    outdir / (self.name+orientation+".png"), 
                    "PNG"
                )

def get_direction_list(number, circle = True):
    value = []
    if (number > 1):
        value += ["north", "south", "east", "west"]
    if (number > 4):
        value += ["northeast", "northwest", "southeast", "southwest"]

    if(circle):
        value = ['('+x+')' for x in value]

    if (len(value) == 0):
        value = [""]

    return value 
