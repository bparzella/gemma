#####################################################################
# app/controllers/tool_ec.py
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
from flask import render_template, redirect, url_for, request, json, abort

@app.route("/tools/<toolname>/ec/<ecid>", methods=['POST', 'GET'])
def tool_ec(toolname, ecid):
    peer = helpers.connectionManager[toolname]
    if request.method == 'POST':
        result = peer.requestEC(int(ecid))
        result.value = int(request.form["value"])
        result = peer.setEC(int(ecid), result)

        return str(ord(result.value[0]))
    else:
        result = peer.requestEC(int(ecid))

        return str(result.value)
