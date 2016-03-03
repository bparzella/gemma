#####################################################################
# app/helpers/__init__.py
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

from json_encoder import jsonEncoder
from plugins import getToolType, loadModules
from secs import connectionManager, addTool, waitForEvents, stop, queueExists, _onEvent, is_int
from processprograms import getProcessProgram, storeProcessProgram, getProcessProgramScopes, getProcessPrograms, processProgramCopy, processProgramMove, processProgramDuplicate, processProgramRename, processProgramRemove, processProgramUpload
import contextprocessor

def stop():
    secs.stop()
