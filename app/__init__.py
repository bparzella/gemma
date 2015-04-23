#####################################################################
# app/__init__.py
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

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

db.create_all()

import helpers

toolHandlers = helpers.loadModules("plugins/toolhandlers")

import models
import controllers
#from models import *
#from controllers import *

# instanciate all configured tools
for tool in models.Tool.query.all():
    helpers.addTool(tool)

def stop():
	helpers.stop()