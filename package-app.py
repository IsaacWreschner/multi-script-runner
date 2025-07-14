import os
import subprocess

# Get the current script's path
curr_dir = os.path.dirname(os.path.abspath(__file__))
script_path = f'{curr_dir}\ssh.py'
data_path = f'{curr_dir}\config.json'
# Get the name of the script without the file extension


# Define the PyInstaller command
pyinstaller_command = [
    'pyinstaller',
    '--onefile',
    '--windowed',
    '--add-data', f"{data_path};.",  # Ensure the config.json is included
    '--distpath', curr_dir,
    script_path
]

# Print the command to be executed
print(f"Running command: {' '.join(pyinstaller_command)}")

# Run the PyInstaller command to create the .exe
try:
    subprocess.run(pyinstaller_command, check=True)
    print("Executable created successfully!")
except subprocess.CalledProcessError as e:
    print(f"Error creating executable: {e}")
