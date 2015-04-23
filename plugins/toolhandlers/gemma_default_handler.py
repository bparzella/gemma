#####################################################################
# gemma_default_handler.py
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

from secsgem import *

from app import helpers, models

class gemmaDefaultHandler(gemDefaultHandler):
    def __init__(self, address, port, active, sessionID, name, eventHandler=None):
        gemDefaultHandler.__init__(self, address, port, active, sessionID, name, eventHandler)

    def _setConnection(self, connection):
        """Set the connection of the for this models. Called by :class:`secsgem.hsmsHandler.hsmsConnectionManager`.

        :param connection: The connection the model uses
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        """
        gemDefaultHandler._setConnection(self, connection)

        self.connection.registerCallback(7, 3, self.S7F3Handler)
        self.connection.registerCallback(7, 5, self.S7F5Handler)

    def S7F3Handler(self, connection, packet):
        """Callback handler for Stream 7, Function 3, Process Program Send - Request.

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = secsDecode(packet)

        tool = models.Tool.query.filter(models.Tool.name == self.name).first()

        helpers.storeProcessProgram(tool.process_program_scope, message.PPID.value, message.PPBODY.value)
        connection.sendResponse(secsS7F4(0), packet.header.system)

        data = {"processProgramScope": tool.process_program_scope, "processProgramID": message.PPID.value, "connection": self.connection, 'peer': self}
        self.fireEvent("ProcessProgramStored", data)

    def S7F5Handler(self, connection, packet):
        """Callback handler for Stream 7, Function 5, Process Program Send - Request.

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = secsDecode(packet)

        tool = models.Tool.query.filter(models.Tool.name == self.name).first()

        data = helpers.getProcessProgram(tool.process_program_scope, message.PPID.value)
        
        if data:
            connection.sendResponse(secsS7F6(message.PPID.value, data), packet.header.system)

        data = {"processProgramScope": tool.process_program_scope, "processProgramID": message.PPID.value, "connection": self.connection, 'peer': self}
        self.fireEvent("ProcessProgramRetrieved", data)

