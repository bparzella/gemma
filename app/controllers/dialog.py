#####################################################################
# app/controllers/dialog.py
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

from app import app, views

from flask import render_template_string, request, json


@app.route("/dialog/<dialog>", methods=['POST', 'GET'])
def renderDialog(dialog):
    if hasattr(views, dialog):
        dialogClass = getattr(views, dialog)

        if request.method == 'POST':
            dialogObject = dialogClass(postURL=request.url, **(request.args.to_dict()))
            if dialogObject.validate_on_submit():
                dialogObject.save()
                return json.dumps("OK")

            return json.dumps(dialogObject.errors)
        else:
            dialogObject = dialogClass(postURL=request.url, **(request.args.to_dict()))
            dialogObject.load()
            return render_template_string(dialogObject.render())
    else:
        return "Invalid dialog {}".format(dialog)
