#!/usr/bin/env python
# -*- python; coding: utf-8 -*-
#
#   Strict.py -- A strict interface for attributes.
#   Copyright (C) 2002, 2008 Christian Höltje
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

class Strict(object):
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
            return object.__setattr__(self,name,value)
        else:
            if name not in self.attributes.keys():
                raise AttributeError, name
            if self.attributes[name][1]:
                self.attributes[name][1](self, name, value)
            else:
                raise ReadOnlyError, name

    def __getattr__(self, name):
        if name[0] == '_':
            return object.__getattr__(self,name)
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
            try:
                value = getattr(self,attr)
            except:
                value = '*error*'
            txt.append( "[%s: %s]" % (attr, value) )
        return ", ".join(txt)

    __repr__ = __str__


if __name__ == '__main__':

    import unittest
    class TestStrict(unittest.TestCase):
        def setUp(self):
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

            self.klass = ExampleStrict
            self.object = ExampleStrict()


        def testSetGet(self):
            self.failUnlessRaises( KeyError,
                                   getattr, self.object, 'one' )
            self.object.one = 1
            self.object.two = 2
            self.failUnlessEqual( self.object.one, 1 )
            self.failUnlessEqual( self.object.two, 2 )

        def testSet(self):
            self.failUnlessRaises( ReadOnlyError,
                                   setattr, self.object, 'ro', 2 )
            self.object.__fish__ = 1
            self.failUnlessEqual( self.object.__fish__, 1 )

        def testAttrError(self):
            """Make sure that AttributeError is raised when fetching
            non-existant attributes"""
            self.failUnlessRaises( AttributeError, getattr,
                                   self.object, '__nozero__' )
            self.failUnlessRaises( AttributeError, getattr,
                                   self.object, 'noexist' )

        def testStr(self):
            self.object.one = 'red'
            self.object.two = 'fish'
            str(self.object)

    unittest.main()
