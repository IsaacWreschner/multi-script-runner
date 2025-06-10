from io import TextIOWrapper
import os 
import sys
import json
import subprocess
import time
import shlex



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Base Directory: {BASE_DIR}")

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QListWidget, QVBoxLayout, QWidget
except ModuleNotFoundError:
    print("Error: PyQt6 module not found. Please install it using 'pip install PyQt6'.")
    sys.exit(1)

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts.json")

class ScriptRunnerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Tab Script Runner")
        self.setGeometry(100, 100, 600, 400)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.load_config()

    def open_windows_terminal(self):
        try:
            process = subprocess.Popen(["wt"], shell=True)
            return process
        except Exception as e:
            print(f"Error opening Windows Terminal: {e}")
            return None

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                 config = self.preprocess_config_file(f)
                 for tab_name, tab_data in config.items():
                    self.add_tab(tab_name, tab_data.get("list", []))
        except FileNotFoundError:
            print(f"Error: Config file '{CONFIG_FILE}' not found.")
        except json.JSONDecodeError:
            print("Error: Config file is not a valid JSON.")
        except Exception as e:
            print(f"Error loading config: {e}")

    def preprocess_config_file(self, file:TextIOWrapper):
            config =  file.read()
            base_dir_normalized = BASE_DIR.replace("\\", "/")
            config = config.replace("{baseDir}", base_dir_normalized)
            return json.loads(config)
           

    def add_tab(self, tab_name, items):
        """Adds a tab with a list of items."""
        tab = QWidget()
        layout = QVBoxLayout()

        list_widget = QListWidget()
        for item in items:
            list_widget.addItem(item.get("name", "Unnamed Item"))

        # Open script in a new tab inside Windows Terminal when clicked
        list_widget.itemClicked.connect(lambda item: self.open_script_in_new_terminal_tab(item.text(), items, tab_name))

        layout.addWidget(list_widget)
        tab.setLayout(layout)
        self.tabs.addTab(tab, tab_name)

    def open_script_in_new_terminal_tab(self, item_name, items, tab_name):
        """Opens a new tab in the existing Windows Terminal window and executes the command."""
        for item in items:
            if item.get("name") == item_name:
                multi_script = item.get("multiScript")
                if multi_script:
                    command = self.generate_multi_script_command(multi_script)
                    self.run_script_in_terminal(command, tab_name, item_name, use_wrapper=True)
                else:
                    command = self.generate_single_script_command(item)
                    self.run_script_in_terminal(command, tab_name, item_name, use_wrapper=item.get("useWrapper", False))
                           
                           
                            
    def run_script_in_terminal(self, script, tab_name, item_name, use_wrapper=False):
        try:
            title = f'{tab_name} {item_name}'
            base_command = f'wt -w 0 -p "Windows Powershell" -d . powershell -noExit -Command'
            if use_wrapper:
                # Wrap the script using the Python wrapper
                wrapper_path = os.path.join(BASE_DIR, "script_wrapper.py")
                command = f'{base_command} python "\'{wrapper_path}\'" {script}'
            else:
                command = f'{base_command} "{script}"'

            print(f'Executing: {command}')
            subprocess.Popen(command, shell=True)

        except Exception as e:
            print(f"Error running script '{script}': {e}")

    def generate_multi_script_command(self, multi_script):
            script_list = ['command=' + self.generate_single_script_command(item) for item in multi_script] 
            commands = " ".join([f'"{cmd}"' for cmd in script_list])
            return commands


    def generate_single_script_command(self, item):
        script = item.get("script")
        script_path = item.get("scriptPath")
        if script:
            return script
        elif script_path:
            return self.generate_command_for_script_path(script_path)
        
        
   
   
    def generate_command_for_script_path(self, script_path):
        if not os.path.isabs(script_path):
            full_path = os.path.normpath(os.path.join(BASE_DIR, script_path))
        else:
            full_path = os.path.normpath(script_path)
        print(f"Full path: {full_path}")
        print(f"Script path: {script_path}")
        print("isabs:", os.path.isabs(script_path))
        ext = os.path.splitext(full_path)[1].lower()
        if ext == ".py":
            return f"python \"'{full_path}'\""
        elif ext == ".ps1":
            return f"pwsh -ExecutionPolicy Bypass -File \"'{full_path}'\""
        else:
            return f"echo 'Script extention not supported yet. pls go to \"'{full_path}'\" and run it manually.'"



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScriptRunnerApp()
    window.show()
    sys.exit(app.exec())