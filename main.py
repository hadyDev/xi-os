from cwio import *
from cwio.const import *
from cwio.font import Font
import time
import machine
from machine import Pin
import sys
import os
import power
import ui
from ui import choose
import res
import wifi
from wifi import wlan
import update
import garbage
import loader
from loader import apps

class DebugInterrupt(Exception):
    pass


init()

screen.on()
screen.init()
keyboard.init()

scr = ui.Screen()

scr + (title := ui.Label(72, 15, "XIOS", SCR.COLOR.DARK, font.classwiz_cw)) + (desc := ui.Label(72, 30, "Press ALPHA\n" + "\n", SCR.COLOR.BLACK, font.miniwi)) + (desc := ui.Label(74, 40, "Vesion 1.5", SCR.COLOR.BLACK, font.miniwi))

applist = []
for app in apps:
    module = app[1]
    applist.append(("[LIB] " if hasattr(module, "lib") else "") + module.name)

def protected_run(func):
    try:
        return func()
    except loader.Error:
        pass
    except Exception as e:
        ui.notify("Python error", (type(e).__name__) + ":\n" + (str(e)), res.ui.error, wait = False)
        raise e
    


def run_app(app):
    def run():
        loader.run(app)
    
    protected_run(run)


try:
    while True:
        screen.clear()
        scr.render()
        screen.apply()
        key = keyboard.get_next()
        if key == KB.KEY.SETTINGS:
            c = choose(["Updates", "WiFi", "Power", "Debug"])
            if c == 0:
                if wifi.support:
                    c = choose(("From OFW repo", "From custom repo"))
                    if c >= 0:
                        if wifi.choose_connect():
                            if c == 0:
                                ui.notify("Updating", "OS will restart automatically after the update.", res.ui.info, wait = False)
                                garbage.collect()
                                if protected_run(update.download):
                                    print("[FWUP] Rebooting device")
                                    machine.reset()
                                else:
                                    ui.notify("Update error", "Something went wrong while downloading the\nupdate.", res.ui.error)
                            elif c == 1:
                                repo = ui.ask("GitHub repo to fetch from:", update.OFW.REPO)
                                if repo.count("/") == 1:
                                    ui.notify("Updating", "OS will restart automatically after the update.", res.ui.info, wait = False)
                                    
                                    garbage.collect()
                                    # lambda macro
                                    if protected_run((lambda: update.download(repo))):
                                        print("[FWUP] Rebooting device")
                                        machine.reset()
                                    else:
                                        ui.notify("Update error", "Something went wrong while downloading the\nupdate. Are you sure the repository you\nspecified exists?", res.ui.error)
                                else:
                                    ui.notify("Invalid repo", "https://github.com/" + repo + "\nis not a valid GitHub repo.", res.ui.error)
                            
                        else:
                            ui.notify("No connection", "A stable Internet connection is required to\nperform updates.", res.ui.error)
                else:
                    ui.notify("No WiFi support", "WiFi support is required to perform updates.", res.ui.error)
            elif c == 1:
                if wifi.support:
                    wifi.choose_connect()
                else:
                    ui.notify("No WiFi support", "WiFi support is required to connect to a\nnetwork.", res.ui.error)
            elif c == 2:
                c = choose(["Deep sleep", "Soft reset", "Hard reset"])
                if c == 0:
                    power.deepsleep()
                elif c == 1:
                    machine.soft_reset()
                elif c == 2:
                    machine.reset()
                
            elif c == 3:
                ui.notify("Debug mode", "Control has been redirected to USB", res.ui.info, wait = False)
                raise DebugInterrupt("Returning to REPL")
            
        elif key == KB.KEY.HOME:
            c = choose(applist)
            if c >= 0:
                run_app(apps[c][0])
        elif key == KB.KEY.AC:
            power.deepsleep()
        
except DebugInterrupt as e:
    print("DEBUG: " + (str(e)))

