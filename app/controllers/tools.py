#####################################################################
# app/controllers/tools.py
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

import time

from app import app, models, helpers, toolHandlers
from flask import render_template, json


@app.route("/tools/")
def tools_list():
    return render_template("tools_list.html", tools=models.Tool.query.all(), connectionManager = helpers.connectionManager)


@app.route("/tools/<toolname>")
def tool_detail(toolname):
    handler = helpers.connectionManager[toolname]
    tool = models.Tool.query.filter(models.Tool.name == toolname).first()

    if handler and handler.connection.connected:
        SVs = sorted(handler.list_svs(), key=lambda SV: SV.SVID.get())
        ECs = sorted(handler.list_ecs(), key=lambda EC: EC.ECID.get())
    else:
        SVs = {}
        ECs = {}

    return render_template("tool_detail.html", handler=handler, tool=tool, modules=toolHandlers, svids=SVs, ecids=ECs)


@app.route("/tools/<toolname>/restart")
def tool_restart(toolname):
    tool = models.Tool.query.filter(models.Tool.name == toolname).first()

    if helpers.connectionManager.has_connection_to(tool.name):
        helpers.connectionManager.remove_peer(tool.name, tool.address, tool.port)

    helpers.addTool(tool)

    return "OK"


@app.route("/tools/<toolname>/comet/<queue>")
def tool_comet(toolname, queue):
    handler = helpers.connectionManager[toolname]

    if not helpers.queueExists(queue):
        return json.dumps({}, default=helpers.jsonEncoder, encoding='latin1')

    if handler is None:
        time.sleep(2)
        return json.dumps([])

    events = helpers.waitForEvents(queue)
    return json.dumps(events, default=helpers.jsonEncoder, encoding='latin1')
