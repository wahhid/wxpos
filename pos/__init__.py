import ConfigParser

config_filename = 'wxpos.cfg'

config = ConfigParser.SafeConfigParser()
config.read(config_filename)

def saveConfig():
    global config, config_filename
    config_file = open(config_filename, 'wb')
    try:
        config.write(config_file)
    except:
        raise
    finally:
        config_file.close()