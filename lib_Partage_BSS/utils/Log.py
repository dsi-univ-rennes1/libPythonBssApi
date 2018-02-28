#!/usr/bin/env python3
# vim: set tabstop=4 softtabstop=4 shiftwidth=4 expandtab:

"""
Logger (singleton)

Logger pour les consommateurs RMQ
DSI plamaizi 25/04/2017

"""
import syslog


class Logger(object):
    class __Logger:
        def __init__(self):
            self.ident = None

        def loginfo(self, text):
            print(self.ident)
            syslog.openlog(ident=self.ident, facility=syslog.LOG_USER)
            syslog.syslog(syslog.LOG_INFO, str(text))
            print(text)

        def logerror(self, text):
            syslog.openlog(ident=self.ident, facility=syslog.LOG_USER)
            syslog.syslog(syslog.LOG_ERR, str(text))
            print(text)

    instance = None

    def __new__(cls):
        if not Logger.instance:
            Logger.instance = Logger.__Logger()
        return Logger.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
