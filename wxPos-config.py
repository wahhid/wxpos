import traceback, sys, os

os.chdir('./pos')
try:
    import pos.dbConfig
    pos.dbConfig.run()
except KeyboardInterrupt:
    sys.exit()
except Exception:
    traceback.print_exc()

print '[DONE EXECUTION]'
try:
    while True: pass
except KeyboardInterrupt:
    sys.exit()
