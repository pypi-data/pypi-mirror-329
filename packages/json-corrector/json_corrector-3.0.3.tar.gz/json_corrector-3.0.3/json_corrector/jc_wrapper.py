import subprocess
import sys

def windows():
    if len(sys.argv) > 1: 
        subprocess.run(["py", "-m", "json_corrector.jc"] + sys.argv[1:])
    else:
        subprocess.run(["py", "-m", "json_corrector.jc"])
    
    

def linux():
    if len(sys.argv) > 1: 
        subprocess.run(["python3", "-m", "json_corrector.jc"] + sys.argv[1:])
    else:
        subprocess.run(["python3", "-m", "json_corrector.jc"])
        

def main():
    if "linux" in sys.platform:
        linux()
    elif "win" in sys.platform:
        windows()

if __name__ == "__main__":
    main()
