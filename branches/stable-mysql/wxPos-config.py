import traceback, sys

try:
    import pos.dbConfig
    pos.dbConfig.run()
except Exception:
    print '[ERROR]'
    traceback.print_exc()
    raw_input('Press enter to exit...')
finally:
    print '---- DONE EXECUTION ----'
