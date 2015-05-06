#####################################################################
# run.py
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

import sys
import signal
import traceback
import threading

import app as appmodule
from app import app


def strackTrace(num, frame):
    print >> sys.stderr, "\n*** STACKTRACE - START ***\n"

    threadNames = {}
    for thread in threading.enumerate():
        threadNames[thread.ident] = thread.getName()

    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# ThreadName: %s ThreadID: %s" % (threadNames[threadId], threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                                                        lineno, name))
            if line:
                code.append("  %s" % (line.strip()))

    for line in code:
        print >> sys.stderr, line
    print >> sys.stderr, "\n*** STACKTRACE - END ***\n"

signal.signal(signal.SIGUSR1, strackTrace)

app.run(host="0.0.0.0", port=4999, debug=True, use_reloader=False, threaded=True)

appmodule.stop()
