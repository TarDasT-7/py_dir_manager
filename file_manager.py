import os
import tkinter as tk
from tkinter import filedialog
from art import text2art
from tqdm import tqdm
import time
import sys
import atexit
import signal

suffix = None
real_name = None


def UI(text):
    ascii_art = text2art(text)
    print(ascii_art)


def sayWellcome():
    print("\n")
    UI("File  Manager :)")
    print("\n")


def sayBye():
    print("\n\n")
    UI("Bye   Bye ^_^ ")
    print("\n\n")


def getNumOfDirs():
    while True:
        customer_input = (
            input("How many directories you want to make? (1-1000) ") or "0"
        )
        try:
            count = int(customer_input)
            if 1 <= count <= 1000:
                return count
            else:
                print("you should enter an integer between 1 and 1000\n")
                return getNumOfDirs()
        except ValueError:
            print("you should enter an integer between 1 and 1000\n")
            return getNumOfDirs()


def getPathGraphical():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Directory")
    if folder_path:
        return folder_path
    else:
        return None


def getPathWithTerminal():
    user_input = input(
        f"please enter your path to make directories: ( current directory is {os.getcwd()} )   "
    )
    starting_path = os.path.abspath(user_input)
    return starting_path


def validationPath(path):
    if path is not None:
        return os.path.exists(path)
    else:
        return False


def getPath():
    condition = validation = False
    while condition is False or validation is False:
        answer = (
            input(
                "please write G for select path graphically or T for write path in terminal. G or T? default is T  "
            ).upper()
            or "T"
        )
        path = False
        if answer == "G":
            path = getPathGraphical()
            condition = True
            validation = validationPath(path)
        elif answer == "T":
            path = getPathWithTerminal()
            condition = True
            validation = validationPath(path)
        else:
            condition = False
            validation = False

    return path


def dirExistsCheck(path, name):
    global real_name
    condition = True
    full_path = os.path.join(path, name)
    if os.path.exists(full_path):
        while condition:
            answer = dirRename(path, name, real_name)
            if answer["status"] == 200:
                if os.path.exists(answer["path"]):
                    name = answer["new_name"]
                    answer = None
                    continue
                else:
                    condition = False
                    break
            else:
                continue
    else:
        answer = {"status": 200, "name": name, "path": full_path}

    return answer


def dirRename(path, name, real_name):
    global suffix
    result = None
    answer = input(
        f"The directory '{name}' already exists. Do you want to rename it? (y/n) or exit for exit of proccess: "
        or "y"
    ).upper()
    if answer == "Y":
        suffix = input(
            "Please write a Suffix for directories or exit for exit of proccess: "
        )
        if suffix == "exit":
            sys.exit()
        else:
            suffix = suffix
            new_name = f"{real_name}_{suffix}"
            full_path = os.path.join(path, new_name)
            result = {"status": 200, "new_name": new_name, "path": full_path}
    elif answer == "EXIT":
        sys.exit()
    else:
        answerForExist = input("do you want to exist? (y/n)").upper()
        if answerForExist == "Y":
            sys.exit()
        else:
            dirRename(path, name, real_name)

    return result


def build(count, path):
    global suffix
    global real_name
    with tqdm(total=count, desc="Creating Directories", unit="dirs") as pbar:
        for i in range(1, count + 1):
            real_name = dir_name = str(i).zfill(2)
            if suffix is None:
                validDirName = dirExistsCheck(path, dir_name)
                os.makedirs(validDirName["path"])
            else:
                os.makedirs(os.path.join(path, f"{dir_name}_{suffix}"))

            pbar.update(1)
            time.sleep(0.1)
    print("end of the tasks...")
    sayBye()
    input("please Enter to exit...")


def run(initial=True):
    if initial == True:
        sayWellcome()
    atexit.register(sayBye)
    count = getNumOfDirs()
    path = getPath()
    if path and count:
        build(count, path)
    else:
        print("something went wrong. please try again...\n")
        run(False)


def signal_handler(sig, frame):
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)

run(True)
