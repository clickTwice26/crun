from crun import debugMsg, cout, ctime
from sys import argv, exit
from colorama import Fore, Back, Style
from random import randint
import sys
import time
import subprocess
import os
import shutil

dbPrefix = "[MANAGER] "
# debugMsg("Use this Carefully", "error", dbPrefix)
helpMessage = ("""usage: manage.py [options]\noptions:
\t-clearouts\t=\tclear all .out files in current directory.
\t-zipSave\t=\tarchive the 'saves' directory into a single zip file
\t-removes <.extension>\t=\tremove all files in current directory with given extension.
\t-setup\t=\tsetup system-wide (only for linux system)
example:
\tpython3 manage.py -clearouts 
""")
def check_file_permissions(file_path):
    if os.access(file_path, os.R_OK):
        # print(f"Read permission is granted for file: {file_path}")
        if os.access(file_path, os.W_OK):
            # print(f"Write permission is granted for file: {file_path}")


            if os.access(file_path, os.X_OK):
                cout("Exec Permission granted", "success")
                time.sleep(1)
                return True
    return False
def is_root():
    return os.getuid() == 0
# debugMsg(f"Argvs: {argv}", "info", dbPrefix)
options = list(set([x[1:] for x in argv if x.startswith('-')]))
# debugMsg(f"Options: {options}", "info", dbPrefix)
def uniqueFolderName(directoryLocation: str, folderName: str) -> str:
    fileList = os.listdir(directoryLocation)
    counter = 0
    while counter < 100:
        if folderName in fileList:
            folderName = folderName+str(randint(0, 1000))
            counter += 1
            continue
        else:
            return folderName

def clearScr():
    os.system("clear")
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
            if option == "setup":
                self.setup()
            if option == "zipSave":
                try:
                    value = args[args.index("-zipSave") + 1]
                except IndexError as e:
                    debugMsg("No zip name given. Selecting a random name", "error", dbPrefix)
                    value = None

                if str(value).endswith(".py"):
                    debugMsg("You cannot purge .py files", "error", dbPrefix)
                    return None
                else:
                    self.zipSave(value)
            if option == "help":
                print(helpMessage)
    def clearouts(self):
        fileList = [i for i in os.listdir(self.location) if i.endswith('.out')]
        for i in fileList:
            os.remove(f'{self.location}/{i}')
            debugMsg(f"Removed {i}", "info", dbPrefix)
    def selfValidation(self):
        fileList = os.listdir(self.location)
        validationReport = 0
        for i in fileList:
            if i in ["crun.py", "manage.py"]:
                validationReport += 1
        if validationReport >= 2:
            debugMsg("Necessary files are there", "success", dbPrefix)
            return True
        else:
            debugMsg("Missing files", "error", dbPrefix)
            return False
    def requirementsCheck(self):
        aptList = [
            "sed"

        ]
        pipList = [
            "colorama"
        ]
        for i in aptList:
            cout(f"Tried to install {i}", "info")
            os.system(f"sudo apt install {i} >> report.txt")
        for i in pipList:
            cout(f"Tried to install {i}", "info")
            os.system(f"pip3 install {i} >> report.txt")
        cout("Requirement check completed.", "info")
        cout(f"{os.getcwd()}/report.txt saved", "info")
    def setup(self):
        if self.selfValidation():
            if not is_root() == 0:
                pass
            else:
                cout("Please run this with 'sudo' permission", "error")
                exit()
            debugMsg("Starting setup of crun", "info", dbPrefix)
            # self.requirementsCheck()
            time.sleep(1)
            cout("Creating Executable file", "info")
            command = "whereis python3"
            result = subprocess.check_output(command, shell=True, text=True)
            execDir = result.split(" ")[1]
            firstLine = "#!"+execDir
            binDir = "/usr/local/bin"
            setupCred = f"""\"\"\"This was setup by manage.py in {ctime("both")}\"\"\""""
            try:
                crunCode = open(f"{os.getcwd()}/crun.py", "r").read()
                manageCode = open(f"{os.getcwd()}/manage.py", "r").read()
                totalCRUNCode =  firstLine+"\n"+ setupCred + "\n" +crunCode
                totalMANAGECode =   firstLine+"\n"+ setupCred+ "\n"+ manageCode

                try:
                    with open(f"{binDir}/crun", "w") as f:
                        f.write(totalCRUNCode)
                        f.close()
                    with open(f"{binDir}/cmanage", "w") as f:
                        f.write(totalMANAGECode)
                        f.close()
                    cout(f"Executable files created", "info")
                    os.system(f"sudo chmod +x {binDir}/crun")
                    os.system(f"sudo chmod +x {binDir}/cmanage")
                    cout("Executable permission given to the files", "success")
                    cout("Crun & Cmanage setup completed", "success")
                except Exception as error:
                    cout(f"{error}", "error")
            except Exception as error:
                cout(f"{error}", "error")
                sys.exit(1)

        else:
            debugMsg("Missing files", "error", dbPrefix)
    def zipSave(self, output_name=None):
        savesDir = f"{os.getcwd()}/saves"
        if output_name == None:
            zipOutputName = uniqueFolderName(os.getcwd(), f"{str(randint(0,100))}_saves.zip")
        else:
            if output_name.endswith(".zip"):
                zipOutputName = output_name
            else:
                zipOutputName = f"{output_name}.zip"
            zipOutputName = uniqueFolderName(savesDir, zipOutputName)


        cout(f"Creating zip file with the name of '{zipOutputName}'", "info")
        try:
           shutil.make_archive(zipOutputName, "zip", savesDir)
        except Exception as error:
            cout(f"{error}", "error")
# time.sleep(2)
if len(options) == 0:
    cout("Loading Options in 2 secs", "info")
    time.sleep(2)
    os.system("clear")


    print(helpMessage)
else:
    manager = Manager(options, argv, location=os.getcwd())

