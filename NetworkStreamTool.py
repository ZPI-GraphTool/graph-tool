import subprocess
import webbrowser

if __name__ == "__main__":
    subprocess.Popen([".venv/Scripts/python.exe", "app/app.py"])
    webbrowser.open("http://localhost:8000")
