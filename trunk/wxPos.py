print '[INIT]'

import traceback, sys, StringIO

ver = sys.argv[1] if len(sys.argv) > 1 else '2.9'
import wxversion
wxversion.select(ver)
print 'Changing wx version to', ver

import wx
import wx.lib.dialogs

class MyLog(wx.PyLog):
    def __init__(self, textCtrl, logTime=0):
        wx.PyLog.__init__(self)
        self.tc = textCtrl
        self.logTime = logTime

    def DoLogString(self, message, timeStamp):
        print 'LOOGOGOGOGOGO'
        print message, timeStamp
        if self.logTime:
            message = time.strftime("%X", time.localtime(timeStamp)) + \
                      ": " + message
        #if self.tc:
        #    self.tc.AppendText(message + '\n')

# Set the wxWindows log target to be this textctrl
#wx.Log_SetActiveTarget(wx.LogTextCtrl(self.log))

# But instead of the above we want to show how to use our own wx.Log class
wx.Log_SetActiveTarget(MyLog(None))#self.log))

# for serious debugging
#wx.Log_SetActiveTarget(wx.LogStderr())
#wx.Log_SetTraceMask(wx.TraceMessages)

try:
    import pos.app
    pos.app.run()
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
