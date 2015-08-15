#####################################################################
# app/controllers/tool_settings.py
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

import logging

from app import app, models, helpers
from flask import request, json


@app.route("/tools/<toolname>/settings", methods=['GET', 'POST'])
def tool_settings(toolname):
    if request.method == 'GET':
        settings = {}

        tool = models.Tool.query.filter(models.Tool.name == toolname).first()

        settings["enabled"] = tool.enabled
        settings["type"] = tool.type
        settings["address"] = tool.address
        settings["port"] = tool.port
        settings["deviceID"] = tool.device_id
        settings["passive"] = tool.passive
        settings["processProgramScope"] = tool.process_program_scope

        return json.dumps(settings)
    elif request.method == 'POST':
        tool = models.Tool.query.filter(models.Tool.name == toolname).first()

        restartRequired = False

        formEnabled = (request.form["enabled"] == "true")
        formType = request.form["type"]
        formAddress = request.form["address"]
        formPort = request.form["port"]
        formDeviceID = request.form["deviceID"]
        formPassive = (request.form["passive"] == "true")
        formProcessProgramScope = request.form["processProgramScope"]

        if not formEnabled == tool.enabled:
            logging.info("tool_settings_update("+toolname+"): Enabled changed, reconnect required")
            restartRequired = True
        if not formType == tool.type:
            logging.info("tool_settings_update("+toolname+"): Type changed, reconnect required")
            restartRequired = True
        if not formAddress == tool.address:
            logging.info("tool_settings_update("+toolname+"): Address changed, reconnect required")
            restartRequired = True
        if not int(formPort) == tool.port:
            logging.info("tool_settings_update("+toolname+"): Port changed, reconnect required")
            restartRequired = True
        if not int(formDeviceID) == tool.device_id:
            logging.info("tool_settings_update("+toolname+"): DeviceID changed, reconnect required")
            restartRequired = True
        if not formPassive == tool.passive:
            logging.info("tool_settings_update("+toolname+"): Passive changed, reconnect required")
            restartRequired = True

        if restartRequired:
            if helpers.connectionManager.has_connection_to(tool.name):
                helpers.connectionManager.remove_peer(tool.name, tool.address, tool.port)

        tool.enabled = formEnabled
        tool.type = formType
        tool.address = formAddress
        tool.port = formPort
        tool.device_id = formDeviceID
        tool.passive = formPassive
        tool.process_program_scope = formProcessProgramScope

        tool.store()

        if restartRequired:
            helpers.addTool(tool)

        return "OK"
    else:
        return "NOGET"


@app.route("/tools/<toolname>/settings/collectionevents/")
def tool_settings_collectionevents(toolname):
    collectionEvents = []

    tool = models.Tool.query.filter(models.Tool.name == toolname).first()
    toolType = helpers.getToolType(tool)

    for collection_event in tool.collection_events:
        collectionEvent = {}
        collectionEvent["ID"] = collection_event.ceid
        collectionEvent["name"] = toolType.ceids[collection_event.ceid]["name"]

        dataValues = []
        for dv in collection_event.dvs:
            dataValue = {}
            dataValue["ID"] = dv.dvid
            dataValue["name"] = toolType.dvs[dv.dvid]["name"]
            dataValues.append(dataValue)

        collectionEvent["DVIDs"] = dataValues

        collectionEvents.append(collectionEvent)

    return json.dumps(collectionEvents)


@app.route("/tools/<toolname>/settings/collectionevents/available")
def tool_settings_collectionevent_available(toolname):
    tool = models.Tool.query.filter(models.Tool.name == toolname).first()
    toolType = helpers.getToolType(tool)

    ceids = []
    for ceid in toolType.ceids:
        ce = {"id": str(ceid)}
        ce.update(toolType.ceids[ceid])
        ceids.append(ce)

    return json.dumps(ceids)


@app.route("/tools/<toolname>/settings/collectionevents/create", methods=["POST"])
def tool_settings_collectionevent_create(toolname):
    if request.method == 'POST':
        tool = models.Tool.query.filter(models.Tool.name == toolname).first()

        ceid = request.form["ceid"]

        for collection_event in tool.collection_events:
            if int(collection_event.ceid) == int(ceid):
                return "EXISTING"

        ce = models.CollectionEvent(ceid=ceid)
        ce.tool = tool

        ce.create()

        return "OK"
    else:
        return "ILLEGAL_REQUEST " + request.method


@app.route("/tools/<toolname>/settings/collectionevents/<ceid>/delete")
def tool_settings_collectionevent_delete(toolname, ceid):
    tool = models.Tool.query.filter(models.Tool.name == toolname).first()

    for collection_event in tool.collection_events:
        if int(collection_event.ceid) == int(ceid):
            collection_event.delete()
            return "OK"

    return "NOTFOUND"


@app.route("/tools/<toolname>/settings/collectionevents/<ceid>/dataValue/available")
def tool_settings_datavalue_available(toolname, ceid):
    tool = models.Tool.query.filter(models.Tool.name == toolname).first()
    toolType = helpers.getToolType(tool)

    dvids = []
    for ceidIterator in toolType.ceids:
        if int(ceidIterator) == int(ceid):
            for dvid in toolType.ceids[ceidIterator]["dv"]:
                dv = {"id": str(dvid)}
                dv.update(toolType.dvs[dvid])
                dvids.append(dv)

    return json.dumps(dvids)


@app.route("/tools/<toolname>/settings/collectionevents/<ceid>/dataValue/create", methods=["POST"])
def tool_settings_collectionevent_datavalue_create(toolname, ceid):
    if request.method == 'POST':
        tool = models.Tool.query.filter(models.Tool.name == toolname).first()

        dvid = request.form["dvid"]

        for collection_event in tool.collection_events:
            if int(collection_event.ceid) == int(ceid):
                for dv in collection_event.dvs:
                    if int(dv.dvid) == int(dvid):
                        return "EXISTING"

                dv = models.DataValue(dvid=dvid, ce_id=collection_event.id)

                dv.create()

                return "OK"

        return "NOCE"
    else:
        return "ILLEGAL_REQUEST " + request.method


@app.route("/tools/<toolname>/settings/collectionevents/<ceid>/dataValue/<dvid>/delete")
def tool_settings_collectionevent_datavalue_delete(toolname, ceid, dvid):
    tool = models.Tool.query.filter(models.Tool.name == toolname).first()

    for collection_event in tool.collection_events:
        if int(collection_event.ceid) == int(ceid):
            for dv in collection_event.dvs:
                if int(dv.dvid) == int(dvid):
                    dv.delete()
                    return "OK"

    return "NOTFOUND"
