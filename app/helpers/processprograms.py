#####################################################################
# app/helpers/processprograms.py
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

import os


def processProgramFilename(processProgramScope, processProgramID):
    return os.path.abspath("data/processprogram/" + processProgramScope + "/" + processProgramID)


def getProcessProgram(processProgramScope, processProgramID):
    filename = processProgramFilename(processProgramScope, processProgramID)

    if not os.path.exists(filename):
        return None

    with open(filename, "r") as file:
        data = file.read()

    return data


def storeProcessProgram(processProgramScope, processProgramID, processProgramData):
    filename = processProgramFilename(processProgramScope, processProgramID)
    filepath = os.path.dirname(filename)

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    with open(filename, "w") as file:
        file.write(processProgramData)
