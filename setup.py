from distutils.core import setup
import py2exe

import shutil
try:
    shutil.rmtree('build')
except:
    pass
try:
    shutil.rmtree('dist')
except:
    pass

# Data Files
from glob import glob
data_files = [('images', glob('./images/*.*')),
              ('images/menu', glob('./images/menu/*.*')),
              ('images/commands', glob('./images/commands/*.*')),
              ('reports', tuple())]

# Scripts
run = {'script': "wxPos.py",
       'dest_base': "run",
       'version': "0.8",
       'name': "wxPos"
       }

# Options
options = {}

# Options Py2Exe
includes = []
excludes = []
packages = ["pos", "reportlab", "sqlalchemy", "MySQLdb", "sqlite3", "wx"]
py2exe_options = {"py2exe": {#"compressed": 0, 
                          #"optimize": 0,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          #"dll_excludes": dll_excludes,
                          "bundle_files": 3,
                          "dist_dir": "dist",
                          #"xref": False,
                          "skip_archive": True,
                          #"ascii": False,
                          #"custom_boot_script": '',
                         }
              }
options.update(py2exe_options)

# Main setup call
setup(windows=[run],
      options=options,
      data_files=data_files
      )
