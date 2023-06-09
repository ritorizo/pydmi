#!/urs/bin/python3
from dmi import *
from pathlib import *
import glob, os
from flask import Flask
from flask import send_file
from flask import request

DMI_DELAY_UNIT_DURATION = 100

# Where to pull the icons from
icon_dir=Path("/home/ritorizo/note/ss13/Shiptest/icons")

# Where to output them
out_dir=Path("/home/ritorizo/note/ss13/pydmi/src/out")


# get url
# if !(url.exist && url.is_up_to_date)
#       if (create_icon(path))
#           return the icon
#       else you absolute boffon error 404 nerd get bonked you idiot, your mother eat cheese.
#
# return the file at url

suported_dirs = ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]

app = Flask(__name__)

@app.route('/', defaults={'_path': ''})
@app.route('/<path:_path>', methods=['GET'])
def catch_all(_path):
    args = request.args.to_dict()
    path = Path(_path)

    posib_dirs = ["north", ""]
    
    # Determine dirrection
    if("dir" in args):
        if args["dir"] not in suported_dirs: 
            print("dirrection '"+args["dir"]+"' not suported")
            return False

        posib_dirs = [args["dir"]]

    #Check all path for existing
    found = False
    image_path = None
    for posib_end in [x+y for x in posib_dirs for y in [".gif", ".png"]]:
        image_path = out_dir / (str(path) + posib_end)
        print(str(image_path))
        if image_path.exists():
            found = True
            print("found the image")
            break
    
    if found:
        return send_file(image_path)
    print("not found the image", len(posib_dirs))

    return send_file(create_icon(path, orientation=(posib_dirs[0] if len(posib_dirs) == 1 else None)))

def create_icon(path, orientation = None):
    """
    param: path: the icon_dir path of the icon.
    """
    dmi = DMI(icon_dir / path.parent.with_suffix(".dmi"))
    dmi.load()
    state = dmi.states[path.name]
    if orientation == None:
        orientation = state.get_default_dir()
    state.unpack(out_dir / path.parent, [orientation])
    return out_dir / (str(path)+orientation+state.extention)

if __name__ == '__main__':
    app.run()

#if __name__=="__main__":
#    cwd = os.getcwd()
#    os.chdir(icon_dir)
#
#    to_convert = glob.glob("*/**/*.dmi", recursive=True)
#
#    # Nope It won't create a file named ".png" or "&.gif"
#    #for yeet in blacklist:
#    #    to_convert.remove(yeet)
#    
#    os.chdir(cwd)
#
#    last_blacklisted = to_convert.index(blacklist[-1])
#
#    for file in to_convert[last_blacklisted +1 :]:
#        print("processing", file)
#        dmi = DMI(Path(icon_dir) / file)
#        dmi.load()
#        dmi.unpack_all(Path(out_dir) / file)
#        del(dmi)
# For the dmi which have some janky state name.
#blacklist= [
#    "obj/status_display.dmi",     
#    "effects/crayondecal.dmi",
#    "hud/screen_gen.dmi",
#    "mob/robots.dmi",
#    "mob/species/misc/digitigrade_shoes.dmi"
#    ]
# stfu = False #Self explanatory
