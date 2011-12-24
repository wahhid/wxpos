import argparse, sys

parser = argparse.ArgumentParser(description='Launch wxPos')
parser.add_argument('--wx', type=str, default=None,
                   help='the wx version string')
parser.add_argument('-c', '--config', action="store_true", default=False,
                   help='run wxPos configuration')
parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=None,
                   help='output redirection')
args = parser.parse_args()

if args.output and sys.stdout != args.output:
    sys.stdout = args.output
    sys.stderr = args.output

print '[INIT]'

import traceback, StringIO

if not (hasattr(sys, 'frozen') and sys.frozen) and args.wx is not None:
    import wxversion
    print 'Changing wx version to', args.wx
    wxversion.select(args.wx)

import wx
import wx.lib.dialogs

try:
    import pos.app
    pos.app.run(config=args.config)
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
    if args.output and sys.stdout != args.output:
        args.output.close()
