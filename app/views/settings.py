import logging

from flask import render_template

from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, NumberRange

from app import models, helpers, toolHandlers


class DialogSettings(Form):
    enabled = BooleanField("Enabled")
    type = SelectField("Type")
    host = StringField('Host', validators=[DataRequired()])
    port = IntegerField('Port', validators=[DataRequired()])
    deviceID = IntegerField('DeviceID', validators=[NumberRange(0, 255, "must be between 0 and 255")])
    ppScope = StringField('Process Program Scope', validators=[DataRequired()])
    passive = BooleanField("Passive")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

        self.toolname = kwargs["toolname"]
        self.postURL = kwargs["postURL"]

        self.type.choices = [(toolHandler[0], toolHandler[0]) for toolHandler in toolHandlers]

    def load(self):
        tool = models.Tool.query.filter(models.Tool.name == self.toolname).first()

        self.enabled.data = tool.enabled
        self.type.data = tool.type
        self.host.data = tool.address
        self.port.data = tool.port
        self.deviceID.data = tool.device_id
        self.ppScope.data = tool.process_program_scope
        self.passive.data = tool.passive

    def save(self):
        tool = models.Tool.query.filter(models.Tool.name == self.toolname).first()

        restartRequired = False

        if not self.enabled.data == tool.enabled:
            logging.info("tool_settings_update("+self.toolname+"): Enabled changed, reconnect required")
            restartRequired = True
        if not self.type.data == tool.type:
            logging.info("tool_settings_update("+self.toolname+"): Type changed, reconnect required")
            restartRequired = True
        if not self.host.data == tool.address:
            logging.info("tool_settings_update("+self.toolname+"): Address changed, reconnect required")
            restartRequired = True
        if not self.port.data == tool.port:
            logging.info("tool_settings_update("+self.toolname+"): Port changed, reconnect required")
            restartRequired = True
        if not self.deviceID.data == tool.device_id:
            logging.info("tool_settings_update("+self.toolname+"): DeviceID changed, reconnect required")
            restartRequired = True
        if not self.passive.data == tool.passive:
            logging.info("tool_settings_update("+self.toolname+"): Passive changed, reconnect required")
            restartRequired = True

        if restartRequired:
            if helpers.connectionManager.hasConnectionTo(tool.name):
                helpers.connectionManager.removePeer(tool.name, tool.address, tool.port, tool.device_id)

        tool.enabled = self.enabled.data
        tool.type = self.type.data
        tool.address = self.host.data
        tool.port = self.port.data
        tool.device_id = self.deviceID.data
        tool.process_program_scope = self.ppScope.data
        tool.passive = self.passive.data

        tool.store()

        if restartRequired:
            helpers.addTool(tool)

    def render(self):
        return render_template("dialog_settings.html", form=self)
