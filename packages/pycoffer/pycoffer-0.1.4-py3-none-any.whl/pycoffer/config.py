# -*- encoding: utf-8 -*-
"""CLI programm

"""
__author__ = 'bibi21000 aka Sébastien GALLET'
__email__ = 'bibi21000@gmail.com'

import os
import sys
import configparser

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points  # noqa
else:
    from importlib.metadata import entry_points  # noqa

from cofferfile.decorator import reify

class Config():

    def __init__(self, filename, chkmode=True):
        self.filename = filename
        self.parser = configparser.ConfigParser()
        self.parser.read(filename)

    @classmethod
    @reify
    def _imp_base64(cls):
        """Lazy loader for base64"""
        import importlib
        return importlib.import_module('base64')

    def check_perms(self, exc=True):
        """Check user right on config file. Must be 600 !!!"""
        mode = oct(os.stat(self.filename).st_mode)[-3:]
        if mode != '600':
            if exc is True:
                raise PermissionError('File %s must be user read/write only: 600 != %s !!!'%(self.filename, mode))
            else:
                return False
        else:
            return True

    def get_defaults(self, filename=None):
        """Return defaults from configuration file"""
        return self._get_defaults(self.parser)

    @classmethod
    def _get_defaults(self, parser=None):
        """Return defaults from configuration file"""
        ret = {}
        if parser is not None:
            for (each_key, each_val) in parser.items('DEFAULT'):
                if each_key.startswith('default_'):
                    ret[each_key.replace('default_','')] = each_val
        if 'ext' not in ret:
            ret['ext'] = '.pcof'
        return ret

    @classmethod
    def Defaults(cls, filename=None):
        """Return defaults from configuration file"""
        parser = configparser.ConfigParser()
        if filename is not None:
            parser.read(filename)
        return cls._get_defaults(parser)

    def coffer(self, section=None):
        """Return a coffer matching section"""
        ret = {}
        if section is None:
            section = 'DEFAULT'

        name = ret['type'] = self.parser[section]['type']
        if 'backup' in self.parser[section]:
            ret['backup'] = self.parser[section]['backup']
        else:
            ret['backup'] = None
        if 'coffer_key' in self.parser[section]:
            ret['coffer_key'] = self._imp_base64.b64decode(self.parser[section]['coffer_key'])
            # ~ ret['coffer_key'] = self.parser[section]['coffer_key']
        # ~ else:
            # ~ ret['coffer_key'] = None
        if 'secure_key' in self.parser[section]:
            # ~ ret['secure_key'] = self.parser[section]['secure_key']
            ret['secure_key'] = self._imp_base64.b64decode(self.parser[section]['secure_key'])
        # ~ else:
            # ~ ret['secure_key'] = None
        if 'location' in self.parser[section]:
            if os.path.isdir(self.parser[section]['location']):
                ret['location'] = os.path.join(self.parser[section]['location'], '.'+section)
            else:
                ret['location'] = self.parser[section]['location']
        else:
            if section == 'DEFAULT':
                ret['location'] = os.path.expanduser('~/.pycoffer')
            ret['location'] = '.' + section
        if name is None:
            raise ValueError("coffer_type must be defined for %s"%(section))
        else:
            crpt = entry_points(group='cofferfile.coffer', name=name)
            if len(crpt) != 1:
                raise IndexError("Problem loading %s : found %s matches"%(name, len(crpt)))
            cls = tuple(crpt)[0].load()
            ret['class'] = cls
        return ret

    @classmethod
    def generate(self, coffer_name=None, type=None, location=None, backup=None, filename=None):
        """Return a coffer configuration as a list of lines"""
        if coffer_name is None:
            raise ValueError("Youd need to provide a coffer_name")
        # are we called from the class or from instance
        if hasattr(self, 'parser'):
            # From instance, we can use parser
            defaults = self._get_defaults(self.parser)
        else:
            # From class ... if we have filename, we could load defaults
            parser = configparser.ConfigParser()
            if filename is not None:
                parser.read(filename)
            defaults = self._get_defaults(parser)
        ret = []

        if type is None:
            if 'type' in defaults:
                type = defaults['type']
            else:
                raise ValueError("Youd need to provide a type")
        crpt = entry_points(group='cofferfile.coffer', name=type)
        if len(crpt) != 1:
            raise IndexError("Problem loading %s : found %s matches"%(type, len(crpt)))
        cls = tuple(crpt)[0].load()
        ret.append('[%s]' % coffer_name)
        ret.append('type = %s' % type)
        if backup is not None:
            ret.append('backup = %s' % backup)
        keys = cls.gen_params()
        for k in keys:
            ret.append('%s = %s' % (k, self._imp_base64.b64encode(keys[k]).decode()))
            # ~ ret.append('%s = %s' % (k, keys[k].decode()))
        if location is not None:
            ret.append('location = %s' % location)
        elif 'location' in defaults:
            ret.append('location = %s' % defaults['location'])
        return ret
