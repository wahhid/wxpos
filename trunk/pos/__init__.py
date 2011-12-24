import ConfigParser
import os, sys

import pos.database as database

def readConfig():
    global config, config_filename
    config.read(config_filename)

def saveConfig():
    global config, config_filename
    config_file = open(config_filename, 'w')
    try:
        config.write(config_file)
    except:
        raise
    finally:
        config_file.close()

config_filename = 'wxpos.cfg'
config = ConfigParser.SafeConfigParser()
readConfig()
