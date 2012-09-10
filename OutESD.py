#!/usr/bin/env python
# -*- python; coding: utf-8 -*-
#
#   outesd.py -- Output to ESD
#   Copyright (C) 2012 Christian Höltje
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

from Morse import *
from array import array
from struct import *
from Strict import Strict
import esd

true = 1
false = 0

class OutESD(Strict):
    _get = Strict._get
    _set = Strict._set

    def _getMorse(self, name):
        return getattr(self._morse, name)

    def _setMorse(self, name, value):
        setattr(self._morse, name, value)

    attributes = { 'sample_rate':        (_getMorse, _setMorse),
                   'frequency':          (_getMorse, _setMorse),
                   'is_8bit':            (_getMorse, _setMorse),
                   'is_stereo':          (_getMorse, _setMorse),
                   'volume':             (_getMorse, _setMorse),
                   'transmission_speed': (_getMorse, _setMorse),
                   'character_speed':    (_getMorse, _setMorse),
                   'is_arrl_wpm':        (_getMorse, _setMorse),
                   'is_arrl_spacing':    (_getMorse, _setMorse),
                   }

    def __init__(self, **kw):
        self.__dict__['_morse'] = MorseCode()
        apply( Strict.__init__, (self,), kw )

    def bytesForStr(self, text):
        return self._morse.bytesForStr( text )

    def generate(self, text, host="", name="Morse" ):
        fmt = esd.ESD_PLAY
        if self.is_stereo:
            fmt |= esd.ESD_STEREO
        else:
            fmt |= esd.ESD_MONO
        if self.is_8bit:
            fmt |= esd.ESD_BITS8
        else:
            fmt |= esd.ESD_BITS16

        bytes = self.bytesForStr( text )
        string = bytes.tostring()

        player = esd.Player( fmt, self.sample_rate, host, name )

        player.write( string )

if __name__ == '__main__':

    e = OutESD()
    e.is_8bit = false
    e.is_stereo = true

    print e
    print e._morse

    e.generate( "This is text we want played via ESD" )
