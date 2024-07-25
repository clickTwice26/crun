import shutil
from json import load, loads, dumps, dump
import os
import sys
import time
from datetime import datetime
from random import randint
from colorama import Fore, Back, Style, init
cwd = os.getcwd()

session_code = randint(1000, 1000000)

default_config = {
	"build_command": "gcc [file_name] -o [output_name]",
	"run_command": "./[output_name]"
}
def cout(message : str, type : str = "info"):
	if type in ["info", "warning", "error"]:
		prefix = "[OUT] "
	elif type == "input":
		prefix = "[IN] "
	else:
		prefix = "[NULL] "
	if type == "info":
		colorType = Back.CYAN
	elif type == "error":
		colorType = Back.RED
	elif type == "warning":
		colorType = Back.YELLOW
	else:
		colorType = Back.GREEN
	print(Fore.CYAN + prefix + Style.RESET_ALL + colorType + message + Style.RESET_ALL, end="\n")
def clear():
	os.system('cls' if os.name == 'nt' else 'clear')
def checkFileName(fileName: str) -> bool:
	fileName = fileName.split(" ")
	if len(fileName) != 1:
		return False
	else:
		return True
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
def ctime(wdm:str = "both"):
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%y %H:%M:%S").split(" ")
	if wdm == "date":
		return dt_string[0]
	elif wdm == "time":
		return dt_string[1]
	else:
		return " ".join(dt_string)





def debugMsg(message:str, category:str = "info", prefix: str="[DEBUG]=>"):
	if category == "info":
		msgColor = Fore.CYAN
	elif category == "error":
		msgColor = Fore.RED
	elif category == "warning":
		msgColor = Fore.BLUE

	else:
		msgColor = Fore.GREEN

	print(msgColor+ prefix + message + Style.RESET_ALL)
	# time.sleep(1)

def clearouts(location):
	fileList = [i for i in os.listdir(location) if i.endswith('.out')]
	for i in fileList:
		os.remove(f'{location}/{i}')
		debugMsg(f"Removed {i}", "info")
def default_log():
	# need a default configuration loader whenever needed
	pass
def update_checking(): #it will check update weekly and daily
	#there should be a another machenism to update itself
	pass
def cloader(configname: str):
	try:
		config_data = load(open(f"{cwd}/{configname}", "r"))
		return config_data
	except Exception as error:
		print(f"[?] Configuration couldnot loaded | Config_Name : {configname}")
		clog(f"config couldn't loaded. config_name: {configname}")
def clog(comment, error=None):
	return None
	logStr = f"[+|{session_code}] {ctime()} | {comment}  {f'| Error:{error}' if error else ''}"
	print(logStr)
	try:
		with open(f"{cwd}/crun.log", "a") as clogger:
			clogger.write(logStr+"\n")
			clogger.close()
	except Exception as error:
		cout(f"[?] Error faced while writing logs | session_code: {session_code} | current_time: {ctime()}", "error")
		time.sleep(3)
class Capsule:
	def __init__(self, location, file_name, output_name, extra_command=None) -> None:
		self.location = location
		if not checkFileName(file_name):
			#debugMsg("Filename has 'space'", "warning")
			#debugMsg("Trying to fix", "info")
			prefix = "'"
			self.file_name = prefix + file_name + prefix
			self.output_name = prefix + output_name + prefix
			#debugMsg(f"after fixing {self.file_name} | {self.output_name}", "info")
			self.sourceFileLocation = f"{self.location}/{file_name}"
			self.outputFileLocation = f"{self.location}/{output_name}"
		else:
			self.sourceFileLocation = f"{self.location}/{file_name}"
			self.outputFileLocation = f"{self.location}/{output_name}"

			self.file_name = file_name
			self.output_name = output_name
		self.extra_command = extra_command
	def clearouts(self):
		paths = os.getcwd()
		out_files = []
		for i in os.listdir(paths):
			if i.endswith(".out"):
				out_files.append(i)
		if len(out_files) >= 1:
			for i in os.listdir(paths):
				if i.endswith(".out"):
					os.remove(f"'{paths}/{i}'")

			clear()
			debugMsg("[+] Cleared .out files")
			sys.exit()
		else:

			clear()
			debugMsg("[+] No files to clearout", "warning")
			sys.exit()
	def file_validation(self):
		if os.path.exists(self.location):
			if os.path.isfile(self.sourceFileLocation):
				return True
			else:
				# debugMsg(f"[+] File does not exist. {self.location}/{self.file_name}", "error")
				debugMsg(f"[+] File does not exist. {self.sourceFileLocation}", "error")
				return False
		else:
			debugMsg(f"[+] Path does not exist. {self.location}", error)
			return False




	def crun(self):
		if self.extra_command == "--reload":
			debugMsg("[+] Reload mode added", "success")
			runtime = 10000
		else:
			runtime = 1
		if self.extra_command == "--clearout":
			self.clearouts()
		counter = 0
		# cout("Runtime: {}".format(runtime), "info")

		while counter < runtime:
			if self.file_validation():
				try:
					os.system("clear")
					print(10 * "--")
					if self.file_name.endswith(".cpp"):
						compiler = "g++"
					else:
						compiler = "gcc"
					compileCommand = f"cd {self.location} && {compiler} {self.file_name} -o {self.output_name} -lm"
					#debugMsg(f"Compiling Command: {compileCommand}")
					os.system(compileCommand)
					os.system(f"cd {self.location} && ./{self.output_name}")
					# cout(f"Filename: {self.file_name}\tRuntime: {runtime}\n", "success")
					print("\n" + 5 * "--" + f"[{self.file_name}]" + 5 * "--")
					cout(f"[~] ReRun[Ctrl+C]|Quit(Q)\nSave[s] FileViewer[f] [{counter+1}/{runtime}]: ", "input")
					operation = input()
					if operation == "q":

						# os.remove(self.location+"/"+self.output_name)
						try:
							os.remove(self.outputFileLocation)
							debugMsg(f"{self.outputFileLocation} removed", "info")
						except Exception as error:
							debugMsg(f"{self.output_name} couldn't removed", "error")
						cout(f"Program Exited\n", "info")
						break
					elif operation == "s":
						try:
							cout(f"[~] Save File name: ", "input")
							save_file_name = input()
						except KeyboardInterrupt:
							save_file_name = self.file_name.split(".")[0]+str(randint(1,10000))+".c"
						try:
							#shutil.copy(f"{self.location}/{self.file_name}", f"{self.location}/saves/{save_file_name}")
							shutil.copy(f"{self.sourceFileLocation}", f"{self.location}/saves/{save_file_name}")
						except Exception as error:
							debugMsg(error, "error")
							os.mkdir(f"{self.location}/saves/")
							shutil.copy(f"{self.location}/{self.file_name}", f"{self.location}/saves/{save_file_name}")
						try:
							cout("File saved in saves folder\n", type="success")
							time.sleep(10)

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
								cout(f"Refresh[Ctrl+C]\tQuit[q/Q]\tCounter[{counter}/{max_counter}]\nSelect File:", "input")
								selection = input()
								if selection.lower() == 'q':
									# self.clearouts()

									cout("Quit", "info")
									exit()
								elif int(selection) in range(0, len(all_files)):
									# print(all_files[int(selection)])
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
					debugMsg(f"[+] Error Faced: {error}", "error")
					break
				except KeyboardInterrupt:
					counter+=1

					if counter == runtime:
						try:
							os.remove(self.outputFileLocation)
							debugMsg(f"{self.outputFileLocation} removed", "info")
						except Exception as error:
							debugMsg(f"{self.output_name} couldn't removed", "error")
						cout(f"Program Exited\n", "info")
					continue
			else:
				cout("File or Path not found", "error")
				break


if __name__ == "__main__":
	init()
	debugMsg("Program Started", "error")
	debugMsg(f"Argvs : {sys.argv}", "info")

	options = [x for x in sys.argv if x.startswith("--")]

	#param = sys.argv
	if len(options) > 0:
		extra_command = options[0]
	else:
		extra_command = "None"
	try:
		file_name = sys.argv[1]
		file_name = file_name if file_name.endswith(".c") or file_name.endswith(".cpp") else file_name+".c"
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
				cout(f"Reload[Ctrl+C] Quit[q/Q] Counter[{counter}/{max_counter}]\nSelect File:", "input")
				selection = input()
				if selection.lower() == 'q':
					# break
					cout("Program Exited\n", "info")
					sys.exit()
				elif int(selection) in range(0, len(all_files)):
					# print(all_files[int(selection)])
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
		file_output_name = file_output_name if file_output_name.endswith(".out") else file_output_name+".out"
	except IndexError:
		cout(f"[+] Default file output name selected: {file_name}_{randint(1, 1000)}", "info")
		file_output_name = f"{file_name}_{randint(1, 1000)}.out"

	# Capsule Start
	try:
		crunch = Capsule(file_location, file_name, file_output_name, extra_command)
		crunch.crun()
	except Exception as error:
		debugMsg(str(error), "error")