import ConfigParser

class Config:
    def __init__(self, filename):
        self.filename = filename
        self._config = ConfigParser.SafeConfigParser()
        self.read()
        self._sections = []
        self.defaults = {}
    
    def read(self):
        self._config.read(self.filename)
    
    def save(self):
        config_file = open(self.filename, 'w')
        try:
            self._config.write(config_file)
        except:
            raise
        finally:
            config_file.close()
    
    def save_defaults(self, overwrite=False):
        for (section, option), value in self.defaults.iteritems():
            if value is None:
                continue
            if not self._config.has_section(section):
                self._config.add_section(section)
            if overwrite or not self._config.has_option(section, option):
                self._config.set(section, option, value)
        self.save()
    
    def clear(self):
        for section in self._config.sections():
            self._config.remove_section(section)
        self.save()
    
    def empty(self):
        return len(self._config.sections()) == 0
    
    def set_default(self, section, option, value=None):
        self.defaults[section, option] = value
    
    def _section(self, k):
        if k in self._sections:
            return self._sections[k]
        else:
            return ConfigSection(self, k)
    
    def __getitem__(self, k):
        if type(k) in (list, tuple):
            if self._config.has_section(k[0]):
                return self._section(k[0])[k[1]]
            else:
                try:
                    return self.defaults[k[0], k[1]]
                except KeyError:
                    return None
        else:
            if self._config.has_section(k):
                return self._section(k)
            else:
                return None
    
    def __setitem__(self, k, v):
        if type(k) in (list, tuple):
            if v is None:
                if self._config.has_option(k[0], k[1]):
                    self._config.remove_option(k[0], k[1])
            else:
                if not self._config.has_section(k[0]):
                    self._config.add_section(k[0])
                self._config.set(k[0], k[1], v)
        else:
            if type(v) == dict:
                self._config.remove_section(k)
                self._config.add_section(k)
                for _k, _v in v.iteritems():
                    self._config.set(k, _k, _v)
            elif isinstance(v, ConfigSection):
                self._config.remove_section(k)
                self._config.add_section(k)
                for _k, _v in v:
                    self._config.set(k, _k, _v)
            elif v is None and self._config.has_section(k):
                self._config.remove_section(k)
    
    def __iter__(self):
        return ((k, self._section(k)) for k in self._config.sections())

class ConfigSection:
    def __init__(self, config, section):
        self.config = config
        self.section = section
        self._config = self.config._config

    set_default = lambda self, option, value=None: self.config.set_default(self.section, option, value)
    
    def __getitem__(self, k):
        if self._config.has_option(self.section, k):
            return self._config.get(self.section, k)
        else:
            try:
                return self.config.defaults[self.section, k]
            except KeyError:
                return None
    
    def __setitem__(self, k, v):
        self._config.set(self.section, k, v)
    
    def __iter__(self):
        return iter(self._config.options(self.section))
