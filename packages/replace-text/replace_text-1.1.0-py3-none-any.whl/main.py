import argparse
import os

class Colors:
    red='\033[91m'
    yellow='\033[93m'
    blue='\033[94m'

def developer_mode(message):
    if developer_mode_enabled:
        print(f"{Colors.yellow}Developer Mode: {Colors.red}{message}")


def parse_args():
    """
    Parses arguments passed into the command line and initializes global variables.
    Returns true if "-h" or "--help" flag passed (to prevent code from moving forward), returns false if not.
    """

    # Global Variable Declaration
    global target_location
    target_location = None

    global developer_mode_enabled
    developer_mode_enabled = False
    
    global help_mode
    help_mode = False

    global replacement_text
    replacement_text = None

    global original_text
    original_text = None 

    global pwd
    pwd = os.getcwd()
    
    parser = argparse.ArgumentParser(add_help=False)

    # ! Arguments
    parser.add_argument("target", help="The target file or directory of files", 
                        nargs='?', default="")

    # ! Flags 
    parser.add_argument("-d", "--developer", 
                        help="enables developer console output",
                        action="store_true")
    
    parser.add_argument("-h", "--help",
                        help="show this help message and exit",
                        action="store_true")
    
    parser.add_argument("-o", "--original-text",
                        help="the text to be replaced",
                        default="", metavar="")
    
    parser.add_argument("-r", "--replacement-text",
                        help="the new text to replace the old",
                        default="", metavar="")
    
    parser.add_argument("-v", "--version",
                         help="displays the version number",
                         action="store_true")
    

    # Set stuff based on arguments and flags
    args = parser.parse_args()
    if not args.target == '':
        target_location = args.target

    if args.developer:
        developer_mode_enabled = True

    if args.replacement_text:
        replacement_text = args.replacement_text

    if args.original_text:
        original_text = args.original_text

    if args.version:
        print('1.1.0')
        return True
    
    if args.help:
        parser.print_help()
        help_mode = True
        return True
    else:
        return False

def replace_text():  
    if not parse_args():
        if not target_location is None:
            beginning_dev_checks()
            developer_mode("Starting package...")
            
            full_dir = os.path.join(pwd, target_location)
            
            global original_text
            if original_text is None:
                original_text = input("What text should be replaced: ")
            global replacement_text
            if replacement_text is None:
                replacement_text = input("Replacement text: ")

            if not (os.path.isdir(full_dir)):
                developer_mode(f"Analyzing file: {full_dir}")
                file_process(original_text, replacement_text, full_dir)
            else:
                developer_mode(f"Analyzing directory: {full_dir}")
                directory_process(original_text, replacement_text, full_dir)
        else:
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
    if not original_text is None:
        developer_mode(f"{Colors.blue}(dev check) {Colors.red}original text = {original_text}")
    if not replacement_text is None:
        developer_mode(f"{Colors.blue}(dev check) {Colors.red}replacement text = {replacement_text}")
    if not target_location is None:
        developer_mode(f"{Colors.blue}(dev check) {Colors.red}target location (full) = {os.path.join(pwd, target_location)}")

# ! COMMENT OUT BELOW WHEN BUILDING
if __name__ == "__main__":
    replace_text()