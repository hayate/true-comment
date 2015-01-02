# -*- coding: utf-8 -*-


class Config(object):
    __state = {}

    def __init__(self, config=None):
        """ application wide config object

        config -- instance of SafeConfigParser
        """
        self.__dict__ = self.__state
        if 'conf' not in self.__dict__:
            self.conf = {}
            for section in config.sections():
                self.conf[section] = {}
                for item in config.items(section):
                    self.conf[section][item[0]] = item[1]

    def __getattr__(self, name):
        return self.conf[name]

    def __getitem__(self, name):
        return self.conf[name]

    def __contains__(self, name):
        return name in self.conf
