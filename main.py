import cmd
import os
import glob
import color_module as cm
import config
import editor
import subprocess as sub
# Colored text escape sequences
class Colors:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    RESET = "\033[0m"

def Error(text):
    print(Colors.RED + text + Colors.RESET)

def Alert(text):
    print(Colors.YELLOW + text + Colors.RESET)


class Command(cmd.Cmd):
    def __init__(self,completionKey) -> 'Command':
        super().__init__()
        self.completekey = completionKey
        self.prompt = f"{Colors.CYAN}{os.getcwd()}{Colors.RESET}:>"
        self.commands = {
            "ls": {
                "name": "ls",
                "description": "returns the contents of the folder"
            },
            "cd": {
                "name": "cd",
                "description": "changes the working directory"
            },
            "clear": {
                "name": "clear",
                "description": "clears the console window"
            },
            "(...)":{
                "name":"(...)",
                "description":"executes python code fromm betwin the parentesis"
            },
            "mkdir":{
                'name':'mkdir',
                'description':'creates a directory'
            },
            "touch":{
                'name':'touch',
                'description':'creates a empty file'
            },
            "edit":{
                'name':'edit',
                'description':'a simple editor'
            }
        }
        cm.delay(f"Crystal cmd\n",0.001,['cyan',"blue"],True)
        print("created by Cross")
        print("https://github.com/cross-sans2/crystal-comand")
        print("type \"help\" for a list of commands")
        print(f"os info: name(related to code, and functions) {os.name}, cpu count: {os.cpu_count()}")

    def complete_cd(self, text, line, begidx, endidx):
        """
        Tab completion for the 'cd' command.
        """
        dir_names = glob.glob(text + '*/')  # Only match directories
        return dir_names

    def complete_ls(self, text, line, begidx, endidx):
        """
        Tab completion for the 'ls' command.
        """
        dir_files = glob.glob(text + '*/')  # Only match directories
        return dir_files
    def do_help(self, arg: str) -> bool | None:
        if not arg:
            for command in self.commands.values():
                print(f"{Colors.YELLOW}{command['name']} >>> {command['description']}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}{self.commands[arg]['name']} >>> {self.commands[arg]['description']}{Colors.RESET}")
    def do_clear(self, arg):
        if os.name == "nt":
            os.system("cls")  # Clear the screen on Windows
        else:
            os.system("clear")  # Clear the screen on Unix-like systems
    def emptyline(self) -> None:
        pass

    def do_edit(self,arg):
        editor.main(file=arg or None)

    def do_ls(self, arg: str) -> None:
        folder = arg or "."
        for item in os.listdir(folder):
            print(f"{Colors.YELLOW}{item}{Colors.RESET}")
    
    def do_touch(self,args):
        for arg in args.split(' '):
            with open(arg,'w') as f:
                f.write()

    def do_mkdir(self,arg):
        folders = arg.split(" ")
        for folder in folders:
            os.mkdir(os.path.join(os.getcwd(),folder))

    def do_cd(self, arg: str) -> None:
        folder = arg or "~"  # Default to the home directory if no argument is provided
        folder = os.path.expanduser(folder)  # Expand the "~" or "$HOME" path
        try:
            os.chdir(folder)
            self.prompt = f"{Colors.CYAN}{os.getcwd()}{Colors.RESET}:>"
        except FileNotFoundError:
            Error("Directory not found.")
    def default(self, line: str) -> None:
        if line.startswith("(") and line.endswith(")"):
            try:
                result = eval(line[1:-1])
                if result is not None:
                    print(result)
            except Exception as e:
                Error(f"Error executing command: {e}")
        else:
            Error(f"Command not recognized: {line}")

if __name__ == "__main__":
    main = Command(config.read_completion_key())
    main.cmdloop()
