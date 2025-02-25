import os
import subprocess
import importlib.util
import datetime
import shutil
import itertools
import threading
import time
import sys
import re
from pathlib import Path

def generate_input_file(profile_name):
    package_name = "anchorestig"
    spec = importlib.util.find_spec(package_name)
    package_root_directory = os.path.dirname(spec.origin)
    print("Retrieving input file template.")
    try:
        shutil.copyfile(f"{package_root_directory}/policies/input_templates/{profile_name}-template.yaml", f'{os.getcwd()}/{profile_name}-template.yaml')
    except:
        print("Input template not found.")
        exit(1)
    print(f"Input template: {profile_name}-template.yaml saved in the current directory")