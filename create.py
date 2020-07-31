import os
import shutil
from distutils.dir_util import copy_tree
import uuid
import json
import sys
import traceback
from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

#Easily generate pretty warnings/errors

def debug_traceback():
    track = traceback.format_exc()
    print(track)

def warning(m):
    print(Fore.YELLOW +  "WARNING:" + Style.RESET_ALL  + " " + m)

def warn(m):
    print(Fore.YELLOW +  "+:" + Style.RESET_ALL + " " + m)

def err(m):
    print(Fore.RED +  "+:" + Style.RESET_ALL + " " + m)

def error(m):
    print(Back.RED + Fore.BLACK +  "ERROR:" + Fore.RED + Back.RESET  + " " + m)

def get_com_mojang_folder():
    com_mojang_folder =  "C:\\Users\\{}\\AppData\\Local\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang".format(os.getlogin())
    if not os.path.isdir(com_mojang_folder):
        error("Could not validate com.mojang folder.")
        err("This may be a user-permission issue.")
        err("Is this your computer name? " + os.getlogin())
        sys.exit(1)
    
    return com_mojang_folder

#Local file locations
base = os.getcwd()

packname = input("Enter pack name: ")
packdescription = input("Enter pack description: ")

rp_name = packname.replace(" ","_").lower() + "_RP"
bp_name = packname.replace(" ","_").lower() + "_BP"

#Output location
com_mojang_loc = get_com_mojang_folder()
devrp_folder = os.path.join(com_mojang_loc, "development_resource_packs")
devbp_folder = os.path.join(com_mojang_loc, "development_behavior_packs")
rp_folder = os.path.join(devrp_folder, rp_name)
bp_folder = os.path.join(devbp_folder, bp_name)

# Do not create if files already exist
print("Validing output location")
if os.path.exists(rp_folder) or os.path.exists(rp_folder):
    error("Pack already exists! Cannot create!")
    sys.exit(1)

#Make dir
os.mkdir(rp_folder)
os.mkdir(bp_folder)

#Copy in the base pack information
copy_tree(os.path.join("templates", "blank_RP"), rp_folder)
copy_tree(os.path.join("templates", "blank_BP"), bp_folder)

templates = os.path.join(base, "templates")

bp_manifest = os.path.join(bp_folder, "manifest.json")
rp_manifest = os.path.join(rp_folder, "manifest.json")

rp_id = str(uuid.uuid4())
bp_module_id = str(uuid.uuid4())
rp_module_id = str(uuid.uuid4())
bp_id = str(uuid.uuid4())

#Behavior Pack
with open(bp_manifest, 'r') as f:
    data = json.load(f)
    data['header']['uuid'] = bp_id
    data['modules'][0]['uuid'] = bp_module_id
    data['dependencies'][0]['uuid'] = rp_id

with open(os.path.join(bp_folder, "texts", "en_US.lang"), 'w') as f:
    f.write("pack.name=" + packname)
    f.write("pack.description=" + packdescription)

with open(os.path.join(rp_folder, "texts", "en_US.lang"), 'w') as f:
    f.write("pack.name=" + packname)
    f.write("pack.description=" + packdescription)

os.remove(bp_manifest)
with open(bp_manifest, 'w') as f:
    json.dump(data, f, indent=4)

#Resource Pack
with open(rp_manifest, 'r') as f:
    data = json.load(f)
    data['header']['uuid'] = rp_id
    data['modules'][0]['uuid'] = rp_module_id
    data['dependencies'][0]['uuid'] = bp_id

os.remove(rp_manifest)
with open(rp_manifest, 'w') as f:
    json.dump(data, f, indent=4)









