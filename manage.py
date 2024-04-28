"""
NOT FOR END USER. ONLY FOR THE DEVELOPER.
"""

import os
import json
from crun import file_viewer, clear
cwd = os.getcwd()
config = json.load(open(cwd + '/crun.json'))

os.system('find . -name "*.out" -type f -delete')








