import traceback, sys, os

ver = sys.argv[0] if len(sys.argv) > 1 else '2.9'
import wxversion
wxversion.select(ver)
print 'Changing wx version to', ver

import wx

os.chdir('./pos')
try:
    import pos.app
    pos.app.run()
except KeyboardInterrupt:
    sys.exit()
except Exception:
    traceback.print_exc()

print '[DONE EXECUTION]'
try:
    while True: pass
except KeyboardInterrupt:
    sys.exit()
