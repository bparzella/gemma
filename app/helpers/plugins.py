#####################################################################
# app/helpers/plugins.py
#
# (c) Copyright 2015, Benjamin Parzella. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#####################################################################

import sys
import os

import secsgem


def loadModules(path):
    modules = []
    sys.path.append(path)
    for name in os.listdir(path):
        if name.endswith(".py"):
            # strip the extension
            module = name[:-3]
            modules.append((module, module))
            # set the module name in the current global name space:
            globals()[module] = __import__(module)

    return modules


def getToolType(tool):
    # set default handler
    toolType = secsgem.SecsHandler

    # check if module loaded for tooltype
    if tool.type in globals():
        # get loaded module
        module = globals()[tool.type]
        # check if module has class for tooltype
        if tool.type in module.__dict__:
            # get loaded class
            classType = module.__dict__[tool.type]
            # check if class is correct type
            if issubclass(classType, secsgem.SecsHandler):
                toolType = classType

    return toolType
