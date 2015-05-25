#####################################################################
# app/controllers/process_programs.py
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

from app import app, helpers
from flask import render_template, json, request


@app.route("/pp")
def process_programs():
    return render_template("process_programs.html")


@app.route("/pp/scopes")
def process_programs_scopes():
    return json.dumps(helpers.getProcessProgramScopes())


@app.route("/pp/<scope>")
def process_programs_scope(scope):
    return json.dumps(helpers.getProcessPrograms(scope))


@app.route("/pp/<scope>/upload", methods=["POST"])
def process_program_upload(scope):
    helpers.processProgramUpload(scope, request.files['file'])
    return "OK"


@app.route("/pp/<scope>/<program>/copy/<targetScope>")
def process_program_copy(scope, program, targetScope):
    helpers.processProgramCopy(scope, program, targetScope)
    return "OK"


@app.route("/pp/<scope>/<program>/move/<targetScope>")
def process_program_move(scope, program, targetScope):
    helpers.processProgramMove(scope, program, targetScope)
    return "OK"

@app.route("/pp/<scope>/<program>/duplicate/<newProgram>")
def process_program_duplicate(scope, program, newProgram):
    helpers.processProgramDuplicate(scope, program, newProgram)
    return "OK"


@app.route("/pp/<scope>/<program>/rename/<newProgram>")
def process_program_rename(scope, program, newProgram):
    helpers.processProgramRename(scope, program, newProgram)
    return "OK"


@app.route("/pp/<scope>/<program>/remove")
def process_program_remove(scope, program):
    helpers.processProgramRemove(scope, program)
    return "OK"
