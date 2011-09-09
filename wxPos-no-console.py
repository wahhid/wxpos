import traceback, sys, os

out = open('out.log', 'a')
sys.stdout = out
sys.stderr = out
os.chdir('./pos')
print
try:
    import pos.app
    pos.app.run()
except:
    print '[ERROR]'
    traceback.print_exc()
finally:
    print '----------'
    out.close()
