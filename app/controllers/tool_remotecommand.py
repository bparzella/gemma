#####################################################################
# app/controllers/tool_remotecommand.py
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

from app import app, models, helpers
from flask import request, json


@app.route("/tools/<toolname>/remotecommands")
def tool_remotecommands(toolname):
    tool = models.Tool.query.filter(models.Tool.name == toolname).first()
    toolType = helpers.getToolType(tool)

    return json.dumps(toolType.rcmds.keys())


@app.route("/tools/<toolname>/remotecommand/<rcmd>")
def tool_remotecommand_details(toolname, rcmd):
    tool = models.Tool.query.filter(models.Tool.name == toolname).first()
    toolType = helpers.getToolType(tool)

    return json.dumps(toolType.rcmds[rcmd])


@app.route("/tools/<toolname>/remotecommand/<rcmd>/run")
def tool_remotecommand_run(toolname, rcmd):
    handler = helpers.connectionManager[toolname]

    params = []

    for param in request.args:
        params.append((param, request.args[param]))

    result = handler.send_remote_command(rcmd, params)

    HCACK = result.HCACK

    if HCACK == 0:
        return "OK"
    elif HCACK == 1:
        return "Invalid command (%d)" % (HCACK)
    elif HCACK == 2:
        return "Cannot do now (%d)" % (HCACK)
    elif HCACK == 3:
        return "Parameter error (%d)" % (HCACK)
    elif HCACK == 4:
        return "OK"
    elif HCACK == 5:
        return "Rejected, already in desired condition (%d)" % (HCACK)
    elif HCACK == 6:
        return "Invalid object (%d)" % (HCACK)
    else:
        return "Errorcode %d" % (HCACK)
