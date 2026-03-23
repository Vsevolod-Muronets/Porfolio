#!/usr/bin/env python3

import os
import os.path
import subprocess
import sys

def installing_libs():
    environm = os.environ.get('VIRTUAL_ENV')
    if environm is None:
        raise Exception("No active environment")
    elif os.path.basename(environm) == 'anothera':
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check = True)
        installed = subprocess.run(['pip', 'freeze'], capture_output = True, text = True, check = True)
        print(installed.stdout)
        with open('requirements.txt', 'w') as outp_file:
            outp_file.write(installed.stdout)
        subprocess.run(['tar', '-czf', "anothera.tar.gz", 'anothera'], check = True)
    else:
        raise Exception("Wrong environment")

if __name__ == "__main__":
    try:
        installing_libs()
    except subprocess.CalledProcessError as err:
        print(f"Something went wrong due to an error: {str(err)}")
        sys.exit(1)
    except Exception as exc:
        print(f"{str(exc)}")
        sys.exit(1)