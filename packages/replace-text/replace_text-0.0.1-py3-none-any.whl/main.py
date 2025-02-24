import argparse
import pathlib
import os

class Colors:
    red='\033[91m'
    GREEN='\033[92m'
    yellow='\033[93m'
    ORANGE='\033[94m'
    blue='\033[94m'
    MAGENTA='\033[95m'
    CYAN='\033[96m'
    gray='\033[90m'
    RESET='\033[0m'

def developer_mode(message):
    if developer_mode_enabled:
        print(f"{Colors.yellow}Developer Mode: {Colors.red}{message}")


def parse_args():
    """
    Parses arguements passed into the command line and initializes global variables.
    Returns true if "-h" or "--help" flag passed (to prevent code from moving forward), returns false if not.
    """

    # Global Variable Declaration
    global developer_mode_enabled
    developer_mode_enabled = False
    
    global help_mode
    help_mode = False
    
    global target_location
    target_location = None

    global pwd
    pwd = os.getcwd()
    
    parser = argparse.ArgumentParser(add_help=False)

    # ! Arguements
    parser.add_argument("target", help="The target file or directory of files", 
                        nargs='?', default='')

    # ! Flags 
    parser.add_argument("-d", "--developer", 
                        help="enables developer console output",
                        action="store_true")
    
    parser.add_argument("-h", "--help",
                        help="show this help message and exit",
                        action="store_true")

    # Set stuff based on arguements and flags
    args = parser.parse_args()
    if not args.target == '':
        target_location = args.target

    if args.developer:
        developer_mode_enabled = True
    
    if args.help:
        parser.print_help()
        help_mode = True
        return True
    else:
        return False

def replace_text():  
    if not parse_args():
        try:
            beginning_dev_checks()
            developer_mode("Starting package...")
            
            full_dir = os.path.join(pwd, target_location)
            
            original_text = input("What text should be replaced: ")
            replacement_text = input("Replacement text: ")

            if not (os.path.isdir(full_dir)):
                developer_mode(f"Analyzing file: {full_dir}")
                file_process(original_text, replacement_text, full_dir)
            else:
                developer_mode(f"Analyzing directory: {full_dir}")
                directory_process(original_text, replacement_text, full_dir)
        except:
            print('Please ensure you have supplied a file or directory to be affected')

    else:
        beginning_dev_checks()

def file_process(original, replacement, target):
    developer_mode(f"Running file_process() on target: {target}, replacing {original} with {replacement}")
    
    with open(target, 'r') as file:
        filedata = file.read()
    
    filedata = filedata.replace(original, replacement)

    with open(target, 'w') as file:
        file.write(filedata)

    developer_mode("Process completed")
        

def directory_process(original, replacement, target):
    developer_mode("Running directory_helper...")

    for file in os.listdir(target):
        current_file = os.path.join(target, file)
        developer_mode(f"Checking {current_file}")
        if not os.path.isdir(current_file):
            file_process(original, replacement, current_file)
        else:
            developer_mode("Skipping directory")


def beginning_dev_checks():
    developer_mode(f"{Colors.blue}(dev check) {Colors.red}developer mode = {developer_mode_enabled}")
    developer_mode(f"{Colors.blue}(dev check) {Colors.red}show help menu = {help_mode}")
    developer_mode(f"{Colors.blue}(dev check) {Colors.red}target location = {target_location}")
    developer_mode(f"{Colors.blue}(dev check) {Colors.red}current working directory = {pwd}")
    if not target_location == None:
        developer_mode(f"{Colors.blue}(dev check) {Colors.red}target location (full) = {os.path.join(pwd, target_location)}")

# ! COMMENT OUT BELOW WHEN BUILDING
if __name__ == "__main__":
    replace_text()