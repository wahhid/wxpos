print '[INIT]'

import traceback, StringIO

import wx
import wx.lib.dialogs

try:
    import pos.app
    pos.app.run(config=True)
except KeyboardInterrupt:
    sys.exit()
except Exception as e:
    strio = StringIO.StringIO()
    traceback.print_exc(file=strio)
    exc = strio.getvalue()
    try:
        wx.lib.dialogs.scrolledMessageDialog(message=exc, title='Exception Caught')
    except:
        print exc
    strio.close()
finally:
    print '[DONE]'
