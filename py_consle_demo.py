
"""
import time
from time import gmtime, strftime

tt = strftime("%Y%m%d", gmtime())
print(tt)
print(gmtime())
"""


"""
import os

print(os.getcwd())
output_folder = "Output"
output_path = os.path.join(os.getcwd(), output_folder)

if not os.path.exists(output_path):
    os.mkdir(output_path)
"""

"""
# See https://stackoverflow.com/a/15882054
import json
import os
from types import SimpleNamespace

output_folder = "Output"
output_file = "items.json"
output_path = os.path.join(os.getcwd(), output_folder, output_file)

with open(f"{output_path}", "r") as file_json:
    contnet = file_json.readlines()

# Parse JSON into an object with attributes corresponding to dict keys.
data = json.loads(contnet.pop(), object_hook=lambda d: SimpleNamespace(**d))

for x in data:
    print(x.name, x.value, hasattr(x, "values"))

"""
