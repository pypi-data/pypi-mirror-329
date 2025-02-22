import subprocess
import sys

def build(setup_kwargs):
    pass

def create_executable():
    try:
        subprocess.run(
            ["pyinstaller", "tableau_toolkit/cli.py", "--name", "tt", "--onefile"],
            check=True
        )
        print("Windows executable (tt.exe) created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating Windows executable: {e}")
