import traceback, sys

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
