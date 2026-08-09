from cwio import *
from cwio.const import *
import os
import fs
import ui
import res
from wifi import support as wifi_support
from update import INFO

class Error(Exception):
    pass


class RequireError(Error):
    pass

class UnsupportedError(Error):
    pass


class EntryPointError(Error):
    pass


apps = []
for path in os.listdir("/apps"):
    if path.endswith(".py") and (not path.startswith("_")) and fs.isfile("/apps/" + path):
        name = path[:-3]
        module = getattr(__import__("apps." + name), name)
        lib = hasattr(module, "lib")
        apps.append([name, module])
        print("[" + ("LIBS" if lib else "APPS") + "] Loaded \"" + name + "\"")

def get(name: str):
    for app in apps:
        if app[0] == name:
            return app[1]
    raise NameError("app \"" + name + "\" couldn't be found")


def require(name: str):
    try:
        return get(name)
    except NameError:
        pass
    
    ui.notify("Missing library", "Please install \"" + name + "\" to continue", res.ui.error)
    raise RequireError(name)


def run(name: str):
    app = require(name)
    requires = getattr(app, "requires", [])
    if (not wifi_support) and ("wifi" in requires):
        ui.notify("Unsupported app", "This app requires WiFi, which isn't supported\nby this device.", res.ui.error)
        raise UnsupportedError("wifi")
    if "cwii" in requires and INFO.TARGET != "cwii":
        ui.notify("Unsupported app", "This app targets CWII devices, while you\ncurrently have a " + INFO.TARGET.upper() + " one.", res.ui.error)
        raise UnsupportedError("cwii")
    if "cwi" in requires and INFO.TARGET != "cwi":
        ui.notify("Unsupported app", "This app targets CWI devices, while you\ncurrently have a " + INFO.TARGET.upper() + " one.", res.ui.error)
        raise UnsupportedError("cwi")
    appmain = getattr(app, "main", None)
    if appmain:
        return appmain()
    lib = hasattr(app, "lib")
    if lib:
        ui.notify("Library app", "This library is only meant to be used by other\napps.", res.ui.error)
    else:
        ui.notify("Missing entry", "This application cannot be launched directly.", res.ui.error)
    raise EntryPointError(lib)

