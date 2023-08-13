import os
from tkinter import messagebox as mbox
import yaml
import requests
import shutil

"""
Ha minden igaz, és jól működik, akkor ebbe a fájlba nem kell szerkessz a működéshez.
"""

ModDlVer = "beta-1.0"

if os.path.exists("mods.yml"):
    pass
else:
    mbox.showerror("Hiba!", "Nem található a mods.json fájl.")

with open("mods.yml", 'r') as raw:
    config = yaml.load(raw, yaml.FullLoader)
if not config["mod.dl.version"] == ModDlVer:
    mbox.showerror("Hiba!", f"A konfigurációs fájl és a program verziója nem egyezik! \nKonfiguráció verzió: {config['mod.dl.version']}\nProgram verzió: {ModDlVer}")

print("███████╗ ███████╗ ██╗  █████╗  ██╗\n██╔════╝ ╚══███╔╝ ██║ ██╔══██╗ ██║\n███████╗   ███╔╝  ██║ ███████║ ██║\n╚════██║  ███╔╝   ██║ ██╔══██║ ╚═╝\n███████║ ███████╗ ██║ ██║  ██║ ██╗\n╚══════╝ ╚══════╝ ╚═╝ ╚═╝  ╚═╝ ╚═╝")
print("Lusta vagyok GUI-t írni")
input('Nyomj "ENTER"-t a program indításához...')

if not os.path.exists("temp"):
    os.mkdir("temp")
if not os.path.exists("temp/mods"):
    os.mkdir("temp/mods")



modcount = len(config["mods"])
i = 1
for file in config["mods"]:
    if os.path.exists(f'temp/mods/{file["filename"]}'):
        print(f"Már létező fájl: {file['filename']} ({i}/{modcount})")
        i += 1
        continue
    print(f"{file['filename']} letöltése ({i}/{modcount})...")
    url = file["url"]
    r = requests.get(url, allow_redirects=True)
    open(f'temp/mods/{file["filename"]}', 'wb').write(r.content)
    i += 1


print("Mod fájlok letöltve!")
print("---------------------------------------------------------------")
print("Parancsok:")
print("mcpath | beállítja a Minecraft elérési utat (csak ennek a programnak). Ha az alap helyen van a Minecraftod, kihagyható")
print("dlinstaller | Letölti a modloader telepítő fájlját (EZ EGY FUTTATHATÓ FÁJL!)")
print("loadmods | Berakja a letöltött modokat a megfelelő mappába.")
print("listmods (lsmods, mods)")
print("exit | Kilép a programból")

running = True
mcpath = rf"C:/Users/{os.getlogin()}/AppData/Roaming/.minecraft/"
while running:
    inp = input("> ")
    if inp.casefold() == "exit":
        exit()
    elif inp.casefold() in ('listmods', "lsmods", 'mods'):
        print("---------------- MODS ----------------")
        for item in config["mods"]:
            print(item["filename"])
            print(f' ⊢ {item["url"]}')
        print("--------------------------------------")
    elif inp.casefold() == "mcpath":
        newpath = input("Új elérési út (mégse: hagyd üresen): ")
        if newpath == "":
            print("> Mégsem")
            continue
        else:
            mcpath = newpath
        print("Elérési út beállítva: "+mcpath)
    elif inp.casefold() == "dlinstaller":
        if not os.path.exists("temp/installer"):
            os.mkdir("temp/installer")
        print(f"{config['modLoader']['filename']} letöltése...")
        url = config['modLoader']['url']
        r = requests.get(url, allow_redirects=True)
        open(f'temp/installer/{config["modLoader"]["filename"]}', 'wb').write(r.content)
        print(r"Kész! (hely: temp\installer)")
    elif inp.casefold() == "loadmods":
        if os.path.exists(mcpath):
            modpath = rf"{mcpath}mods"
            if os.path.exists(modpath):
                if len(os.listdir(modpath)) == 0:
                    print("Fájlok másolása folyamatban...")
                    for file in os.listdir("temp/mods"):
                        print(rf"temp/mods/{file} --> {modpath}/{file}")
                        shutil.copy(rf"temp/mods/{file}", modpath)
                else:
                    print("A mods mappa nem üres!")
                    choice = input("Mods mappa törlése? igen(i)/nem(n): ")
                    if choice.casefold() in ('igen', 'i'):
                        print("Mods mappa tartalmának tölése folyamatban...")
                        for file in os.listdir(modpath):
                            print(rf"{modpath}/{file}")
                            os.remove(rf"{modpath}/{file}")
                        print("Fájlok másolása folyamatban...")
                        for file in os.listdir("temp/mods"):
                            print(rf"temp/mods/{file} --> {modpath}/{file}")
                            shutil.copy(rf"temp/mods/{file}", modpath)
                    if choice.casefold() in ('nem', 'n'):
                        print("Fájlok másolása folyamatban...")
                        for file in os.listdir("temp/mods"):
                            print(rf"temp/mods/{file} --> {modpath}/{file}")
                            shutil.copy(rf"temp/mods/{file}", modpath)
            else:
                mbox.showerror("Hiba!", "'mods' mappa nem található!")
        else:
            mbox.showerror("Hiba!", "Elérési út nem található")
