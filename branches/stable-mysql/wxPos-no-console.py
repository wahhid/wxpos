import traceback, sys

out = open('out.log', 'a')
sys.stdout = out
sys.stderr = out

print
try:
    import pos.app
    pos.app.run()
except:
    print '[ERROR]'
    traceback.print_exc()
finally:
    print '---- DONE EXECUTION ----'
    print
    out.close()
