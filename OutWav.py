#!/usr/bin/env python
# -*- python; coding: utf-8 -*-
#
#   outwav.py -- Output to Wav files
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

true = 1
false = 0

class OutWav(Strict):
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
        if kw.has_key('file'):
            self._file = kw['file']
            del kw['file']
        else:
            self._file = None
        if kw.has_key('fd'):
            self._fd = kw['fd']
            del kw['fd']
        else:
            self._fd = None

        apply( Strict.__init__, (self,), kw )

    def bytesForStr(self, text):
        data = self._morse.bytesForStr( text )

        header = array(self._morse.array_char)

        header.fromstring( "data"+\
                           pack("<L",len(data)*data.itemsize) )
        data = header+data

        if self.is_stereo:
            channels = 2
        else:
            channels = 1
        fmt = "WAVEfmt " + pack("<LHHLLHH",16,
                                1, channels,
                                self.sample_rate,
                                data.itemsize*self.sample_rate*channels,
                                data.itemsize,
                                8*data.itemsize )
        header = array(self._morse.array_char)
        header.fromstring( fmt )
        data = header+data

        header = array(self._morse.array_char)
        header.fromstring( "RIFF"+\
                           pack("<L",len(data)*data.itemsize) )

        return header+data

    def generate(self, text, file=None, fd=None ):
        if not file and self._file:
            file = self._file
        if not fd and self._fd:
            fd = self._fd
        if not file and not fd:
            file = "output"
            if self.is_8bit:
                file += "-8bit"
            else:
                file += "-16bit"
            if self.is_stereo:
                file += "-stereo"
            else:
                file += "-mono"
            file += ".wav"

        if not fd:
            fd = open( file, "wb" )
        arry = self.bytesForStr( text )
        arry.tofile( fd )
        fd.close()


if __name__ == '__main__':

    wav = OutWav()
    wav.is_8bit = false
    wav.is_stereo = true
    print wav
    print wav._morse

    wav.generate( "This is text we want written to a file" )

# Helpful info:
# http://www.borg.com/~jglatt/tech/wave.htm
# http://www.technology.niagarac.on.ca/courses/comp630/WavFileFormat.html
