print '[INIT]'

import traceback, StringIO

import wx

try:
    import pos.app
    pos.app.run()
except KeyboardInterrupt:
    sys.exit()
except Exception as e:
    strio = StringIO.StringIO()
    traceback.print_exc(file=strio)
    exc = strio.getvalue()
    print exc
    try:
        wx.MessageBox(exc, 'Exception caught', style=wx.OK)
    except:
        pass
    strio.close()
finally:
    print '[DONE]'
