#!/usr/bin/env python
# -*- python -*-
#
#   Strict.py -- A strict interface for attributes.
#   Copyright (C) 2002 Christian Höltje
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

class ReadOnlyError(AttributeError): pass

class Strict:
    _data = None

    def _get(self, name):
        return self._data[name]

    def _set(self, name, value):
        self._data[name] = value

    attributes = {}

    def __init__(self, **kw):
        self._data = {}

    def __setattr__(self, name, value):
        if name[0] == '_':
            self.__dict__[name] = value
            return
        else:
            if name not in self.attributes.keys():
                raise AttributeError, name
            if self.attributes[name][1]:
                self.attributes[name][1](self, name, value)
            else:
                raise ReadOnlyError, name

    def __getattr__(self, name):
        if name[0] == '_':
            return self.__dict__[name]
        if name not in self.attributes.keys():
            raise AttributeError, name

        if self.attributes[name]:
            return self.attributes[name][0](self, name)
        else:
            return None

    def __str__(self):
        txt = []
        keys = self.attributes.keys()
        keys.sort()
        for attr in keys:
            txt.append( "[%s: %s]" % (attr, getattr(self, attr)) )
        return ", ".join(txt)

    __repr__ = __str__


if __name__ == '__main__':

    import unittest
    class ExampleStrict(Strict):
        _get = Strict._get
        _set = Strict._set
        
        attributes = { 'one': (_get, _set),
                       'two': (_get, _set),
                       'ro' : (_get, None),
                       'set': (None, _set),
                       }

        def __init__(self, **kw):
            apply( Strict.__init__, (self,), kw )
        
    class TestStrict(unittest.TestCase):

        def testSetGet(self):
            s = ExampleStrict()
            self.failUnlessRaises( KeyError,
                                   getattr, s, 'one' )
            s.one = 1
            s.two = 2
            self.failUnlessEqual( s.one, 1 )
            self.failUnlessEqual( s.two, 2 )

        def testSet(self):
            s = ExampleStrict()
            self.failUnlessRaises( ReadOnlyError,
                                   setattr, s, 'ro', 2 )

    unittest.main()
