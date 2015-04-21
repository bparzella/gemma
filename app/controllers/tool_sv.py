#####################################################################
# app/controllers/tool_sv.py
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

@app.route("/tools/<toolname>/sv/<svid>")
def tool_sv(toolname, svid):
    peer = helpers.connectionManager[toolname]
    result = peer.requestSV(int(svid))

    if isinstance(result, list):
        return str(result)

    return str(result.value)
