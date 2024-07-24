import time
from sys import argv, exit
from colorama import Fore, Back, Style
import time
import os
from crun import debugMsg
dbPrefix = "[MANAGER] "
debugMsg("Use this Carefully", "error", dbPrefix)

debugMsg(f"Argvs: {argv}", "info", dbPrefix)
options = list(set([x[1:] for x in argv if x.startswith('-')]))
debugMsg(f"Options: {options}", "info", dbPrefix)

class Manager:
    def __init__(self, options: list, args : list,location:str=os.getcwd()):
        self.options = options
        self.location = location
        for option in options:
            if option == "clearouts":
                self.clearouts()
            if option == "removes":
                try:
                    value = args[args.index("-removes")+1]
                except IndexError as e:
                    debugMsg("Incorrect arguments", "error", dbPrefix)
                    return None
                if str(value).endswith(".py"):
                    debugMsg("You cannot purge .py files", "error", dbPrefix)
                    return None
                else:
                    fileList = [i for i in os.listdir(self.location) if i.endswith(value)]
                    for i in fileList:
                        os.remove(f'{self.location}/{i}')
                        debugMsg(f"Removed {i}", "info", dbPrefix)

    def clearouts(self):
        fileList = [i for i in os.listdir(self.location) if i.endswith('.out')]
        for i in fileList:
            os.remove(f'{self.location}/{i}')
            debugMsg(f"Removed {i}", "info", dbPrefix)

# time.sleep(2)
if len(options) == 0:
    debugMsg("All options are here: ", "info", dbPrefix)
    print("""usage: manage.py [options]\noptions:
    \t-clearouts =\tclear all .out files in current directory.
    \t-zipSave =\tarchive the 'saves' directory into a single zip file
    \t-removes <.extension> =\tremove all files in current directory with given extension.
    \t-setup =\tsetup system-wide (only for linux system)
    example:
    \tpython3 manage.py -clearouts 
    """)
else:
    manager = Manager(options, argv, location=os.getcwd())

