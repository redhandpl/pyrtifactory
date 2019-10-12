# -*- coding: utf-8 -*-

import sys

class checkRuntime():
    def checkRuntimeVersion(self):
        currentVersion = sys.version_info
        reqV = 3

        if currentVersion[0] == reqV:
            pass
        else:
            sys.stderr.write("[%s] - Error: You need to use Python %d.x.\n" % (sys.argv[0], reqV))
            sys.exit(1)

        return 0
