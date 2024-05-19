import shutil
from json import load, loads, dumps, dump
import os
import sys
import time
from datetime import datetime
from random import randint

cwd = os.getcwd()
session_code = randint(1000, 1000000)
default_config = {
    "build_command": "gcc [file_name] -o [output_name]",
    "run_command": "./[output_name]"
}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def file_viewer(dir=os.getcwd()):
    counter = 0
    valid_file_list = []
    for i in os.listdir(dir):
        if i.endswith('.c') or i.endswith('.cpp'):
            print(f"[{counter}] {i}")
            valid_file_list.append(i)
            counter += 1
    print("\n")
    return valid_file_list


def ctime(wdm: str = "both"):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%y %H:%M:%S").split(" ")
    if wdm == "date":
        return dt_string[0]
    elif wdm == "time":
        return dt_string[1]
    else:
        return " ".join(dt_string)


def cloader(configname: str):
    try:
        config_data = load(open(f"{cwd}\\{configname}", "r"))
        return config_data
    except Exception as error:
        print(f"[?] Configuration could not be loaded | Config_Name : {configname}")
        clog(f"config couldn't be loaded. config_name: {configname}")


def clog(comment, error=None):
    logStr = f"[+|{session_code}] {ctime()} | {comment}  {f'| Error:{error}' if error else ''}"
    print(logStr)
    try:
        with open(f"{cwd}\\crun.log", "a") as clogger:
            clogger.write(logStr + "\n")
            clogger.close()
    except Exception as error:
        print(
            f"[?] Error faced while writing logs | session_code: {session_code} | current_time: {ctime()}")
        time.sleep(3)


class Capsule:
    def __init__(self, location, file_name, output_name, extra_command=None) -> None:
        self.location = location
        self.file_name = file_name
        self.output_name = output_name
        self.extra_command = extra_command
        print(self.extra_command)

    def clearouts(self):
        paths = os.getcwd()
        out_files = []
        for i in os.listdir(paths):
            if i.endswith(".out"):
                out_files.append(i)
        if len(out_files) >= 1:
            for i in os.listdir(paths):
                if i.endswith(".out"):
                    os.remove(f"{paths}\\{i}")

            clear()
            print("[+] Cleared .out files")
            sys.exit()
        else:
            clear()
            print("[+] No files to clearout")
            sys.exit()

    def file_validation(self):
        if os.path.exists(self.location):
            if os.path.isfile(self.location + "\\" + self.file_name):
                return True
            else:
                print(f"[+] File does not exist. {self.location}\\{self.file_name}")
                return False
        else:
            print(f"[+] Path does not exist. {self.location}")
            return False

    def crun(self):
        if self.extra_command == "--reload":
            print("[+] Reload mode added")
            runtime = 10000
        else:
            runtime = 1
        if self.extra_command == "--clearout":
            self.clearouts()

        counter = 0
        print("Runtime: {}".format(runtime))

        while counter < runtime:
            if self.file_validation():
                try:
                    clear()
                    print(10 * "--")
                    if self.file_name.endswith(".cpp"):
                        compiler = "g++"
                    else:
                        compiler = "gcc"
                    os.system(
                        f"cd {self.location} && {compiler} {self.file_name} -o {self.output_name} -lm")
                    os.system(
                        f"cd {self.location} && .\\{self.output_name}")
                    print("\n" + 10 * "--")
                    operation = input(
                        f"[~] ReRun[Ctrl+C]|Quit(Q)\nSave[s] FileViewer[f] [{counter + 1}/{runtime}]: ")
                    if operation == "q":
                        os.remove(self.location + "\\" + self.output_name)
                        break
                    elif operation == "s":
                        try:
                            save_file_name = input(
                                f"[~] Save File name: ")
                        except KeyboardInterrupt:
                            save_file_name = self.file_name.split(".")[0] + str(randint(1, 10000)) + ".c"
                        try:
                            shutil.copy(f"{self.location}\\{self.file_name}",
                                        f"{self.location}\\saves\\{save_file_name}")
                        except Exception as error:
                            os.mkdir(f"{self.location}\\saves\\")
                            shutil.copy(f"{self.location}\\{self.file_name}",
                                        f"{self.location}\\saves\\{save_file_name}")
                        try:
                            print("File saved in saves folder")
                            time.sleep(20)
                        except KeyboardInterrupt:
                            continue
                    elif operation == "f":
                        counter = 0
                        max_counter = 100000
                        message = ""
                        while True:
                            clear()
                            all_files = file_viewer()
                            counter += 1
                            try:
                                if message != "":
                                    print("=>" + message)
                                selection = input(
                                    f"Reload[Ctrl+C] Quit[q/Q] Counter[{counter}/{max_counter}]\nSelect File:")
                                if selection.lower() == 'q':
                                    break
                                elif int(selection) in range(0, len(all_files)):
                                    message = f"Selected File: {all_files[int(selection)]}"
                                    self.file_name = all_files[int(selection)]
                                    break

                                else:
                                    message = "File Not Found"
                            except KeyboardInterrupt:
                                clear()
                                message = "File list refreshed"
                                continue
                            except Exception as error:
                                clear()
                                message = f"Invalid Selection: {selection}"
                                continue
                            continue

                except Exception as error:
                    print(f"[+] Error Faced: {error}")
                    break
                except KeyboardInterrupt:
                    counter += 1
                    if counter == runtime:
                        print(f"\nExited because you told to run {counter} times")
                    continue
            else:
                print("File or Path not found")
                break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Entered")
        for i in sys.argv:
            if i.startswith("--"):
                extra_command = i
                break
    else:
        extra_command = "None"

    try:
        file_name = sys.argv[1]
        file_name = file_name if file_name.endswith(
            ".c") or file_name.endswith(".cpp") else file_name + ".c"
        clog("[+] Session started")
    except Exception as error:
        counter = 0
        max_counter = 100000
        message = ""
        while True:
            clear()
            all_files = file_viewer()
            counter += 1
            try:
                if message != "":
                    print("=>" + message)
                selection = input(
                    f"Reload[Ctrl+C] Quit[q/Q] Counter[{counter}/{max_counter}]\nSelect File:")
                if selection.lower() == 'q':
                    sys.exit()
                elif int(selection) in range(0, len(all_files)):
                    message = f"Selected File: {all_files[int(selection)]}"
                    file_name = all_files[int(selection)]
                    extra_command = "--reload"
                    break
                else:
                    message = "File Not Found"
            except KeyboardInterrupt:
                clear()
                continue
            except Exception as error:
                clear()
                message = f"Invalid Selection: {selection}"
                continue

    file_location = os.getcwd()
    try:
        file_output_name = sys.argv[2] if not sys.argv[2].startswith("--") else f"{file_name}_{randint(1, 1000)}.out"
        file_output_name = file_output_name if file_output_name.endswith(".out") else file_output_name + ".out"
    except IndexError:
        print(f"[+] Default file output name selected: {file_name}_{randint(1, 1000)}")
        file_output_name = f"{file_name}_{randint(1, 1000)}.out"
    print(sys.argv)

    # Capsule Start
    crunch = Capsule(file_location, file_name, file_output_name, extra_command)
    crunch.crun()
