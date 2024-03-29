# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, February 21st 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from pathlib import Path
import sys
import os

root = Path(__file__).resolve().parents[3]
sys.path = [str(root)] + sys.path

import pyufunc as pf

# Get all the modules in the pyufunc package
category_lst = []
for module_lst in pf.ufunc_category.values():
    if module_lst:
        for module in module_lst:
            category_lst.append(module)

# remove all documents in the api folder
api_folder = "api"
for file in os.listdir(api_folder):
    if file.endswith(".rst"):
        os.remove(os.path.join(api_folder, file))

# Create the API documentation
for module in category_lst:
    file_name = f"api/pyufunc.{module}.rst"

    with open(file_name, "w", encoding="utf-8") as f:
        heading_message = "pyufunc." + module

        heading_message_split = heading_message.split("_")
        heading_message_new = heading_message_split[0]
        for i in range(1, len(heading_message_split)):
            heading_message_new += heading_message_split[i] + "\\" + "_"

        heading_message_new = heading_message_new[:-2]
        heading_dashes = "=" * len(heading_message_new)

        f.write(heading_message_new + "\n")
        f.write(heading_dashes + "\n\n")

        # if gmns_geo is in the module name, then it is a subpackage
        if "gmns_geo" in file_name:
            f.write(".. automodule:: pyufunc." + module + "\n\n")
        else:
            f.write(".. automodule:: pyufunc\n\n")
            f.write(".. autofunction:: " + module + "\n\n")

        f.close()

print("Successfully updated API documentation!")
