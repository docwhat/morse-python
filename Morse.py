#!/usr/bin/env python
# -*- python -*-
#
#   morse.py -- Python Morse Library
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

from math import pi, sin
from Characters import *
from array import array
from struct import *
from Strict import Strict
import sys

true = 1
false = 0

class Beep:
    def _envelope( self, step, cycles, front ):
        if step == 0:
            return 0.0

        if step < front:
            # number from 0 to 1
            i = step/(front*2.0)
            #return step/front # trapezoid
            #return sin( pi*step/(front*2.0) ) # 1/4 sin
            return sin( pi*i ) # 1/4 sin
            return (sin(pi*(i - 0.5)) + 1)/2.0
        
        if step < cycles - front:
            return 1
        
        if step < (cycles-1):
            # number from 0 to 1
            i = (cycles-step)/(front*2.0)
            #return (cycles-step-1)/front  # trapezoid
            #return sin( pi*(cycles-step)/(front*2.0) ) # 1/4 sin
            return sin( pi*i ) # 1/4 sin
            #return (sin(pi*(i - 0.5)) + 1)/2.0
            

        return 0

    def __init__(self,
                 sample_rate,
                 frequency, channels=1):
        
        self.sample_rate = float(sample_rate)
        self.frequency = float(frequency)
        self.divisor = (sample_rate/frequency)/2.0
        self.channels = channels
        

    def __call__(self, duration, volume, type='B', zero=127):
        duration = float(duration)
        volume = float(volume)

        cycles = int(duration * self.sample_rate)
        
        s = array(type)

        if volume == 0.0:
            for i in range(0, cycles*self.channels):
                #s.fromstring( pack("<H", 0) )
                s.append(0)
        else:
            for i in range(0, cycles):
                front = float(self.sample_rate)/200.0
                x = pi * i / self.divisor
                amp = self._envelope( i, cycles, front )
                #print amp
                amp = amp  * volume
                byte = int( (sin(x) * amp + zero) )
                for j in range(0,self.channels):
                    s.append(byte)
                    #s.fromstring( pack("<H", byte) )

        return s

class MorseCode(Strict):
    _beep_class = Beep

    _u = 0
    _Ta = 0
    _Tc = 0
    _Tw = 0

    _get = Strict._get
    _set = Strict._set

    def _setBitSign(self, name, value):
        self.__dict__['_cache'] = {}
        self._set(name,value)
        if name == 'is_8bit':
            self._set('is_unsigned',value)
        if self.is_8bit:
            if self.is_unsigned:
                # Unsigned 8bit
                zero = 127
                volmax = 127
                achar = 'B'
            else:
                # Signed 8bit
                zero = 0
                volmax = 63
                achar = 'b'
        else:
            if self.is_unsigned:
                # Unsigned 16bit
                zero = 32768
                volmax = 32760
                achar = 'H'
            else:
                # Signed 16bit
                zero = 0
                volmax = 32760
                achar = 'h'
                
        self._data['zero'] = zero
        self._data['volume_max'] = volmax
        self._data['array_char'] = achar

    def _setWPM(self, name, value):
        if self.character_speed == None:
            self._set( 'transmission_speed', value )
            if value < 18:
                self._set( 'character_speed', 18 )
            else:
                self._set( 'character_speed', value )
        else:
            self._set( name, value )

    def _setVolume(self, name, value):
        if value < 0 or value > 100:
            raise ValueError, "volume must be a number between 0 and 100"
        else:
            self._set( name, value )

    attributes = { 'sample_rate':        (_get, _set),
                   'is_unsigned':        (_get, _setBitSign),
                   'is_8bit':            (_get, _setBitSign),
                   'is_stereo':          (_get, _set),
                   'zero':               (_get, None),
                   'volume_max':         (_get, None),
                   'array_char':         (_get, None),
                   'volume':             (_get, _setVolume),
                   'frequency':          (_get, _set),
                   'transmission_speed': (_get, _setWPM),
                   'character_speed':    (_get, _set),
                   'is_arrl_wpm':        (_get, _set),
                   'is_arrl_spacing':    (_get, _set),
                  }

    def __init__(self, **kw):
        apply( Strict.__init__, (self,), kw )
        self._data = { 'sample_rate':     44100,
                       'frequency':       700,
                       'is_stereo':       false,
                       'is_arrl_wpm':     true,
                       'is_arrl_spacing': true,
                       'volume':          95,
                       }
        self.is_unsigned = true
        self.is_8bit = true
        self.transmission_speed = 6
        for i in kw.keys():
            if i == 'beep':
                self._beep_class = kw[i]
            else:
                setattr(self, i, kw[i])

    def __getattr__(self, name):
        try:
            return Strict.__getattr__(self, name)
        except KeyError:
            return None

    def __setattr__(self, name, value):
        Strict.__setattr__(self, name, value)
        self._recalc()

    def _upm(self, wpm):
        if self.is_arrl_wpm:
            return 60.0/(50.0*wpm)
        else:
            return 60.0/(50.0*wpm + (wpm-1)*7)

    def _recalc(self):
        """
        From an ARRL document:
        http://www.arrl.org/files/infoserv/tech/code-std.txt
        Unit costs:
          dit                        1
          dah                        3
          space between dit/dah      1
          space between characters   3
          space between words        7
        """
        self.__dict__['_cache'] = {}
        if not self.character_speed or not self.transmission_speed:
            return
        c = float(self.character_speed)
        s = float(self.transmission_speed)

        u = self._upm( c )
        Ta = 50.0*self._upm(s) - 31.0*self._upm(c)

        if self.is_arrl_spacing:
            Tc = 3.0*Ta/19.0
            Tw = 7.0*Ta/19.0
        else:
            Tc = 3.0*self._upm( s )
            Tw = 7.0*self._upm( s )

        self.__dict__['_u']  = u
        self.__dict__['_Ta'] = Ta
        self.__dict__['_Tc'] = Tc
        self.__dict__['_Tw'] = Tw

    def _fillCache(self):
        if self.__dict__['_cache']:
            return
        
        cache = {}
        if self.is_stereo:
            channels = 2
        else:
            channels = 1
        beeper = self._beep_class( sample_rate=self.sample_rate,
                                   frequency=self.frequency,
                                   channels=channels )
        vol = float(self.volume)*float(self.volume_max)/100.0
        
        cache['cs']   = beeper( duration=self._Tc,
                                volume=0.0,
                                zero=self.zero,
                                type=self.array_char
                                )
        cache['ws']   = beeper( duration=self._Tw,
                                volume=0.0,
                                zero=self.zero,
                                type=self.array_char
                                )
        cache['us']   = beeper( duration=self._u,
                                volume=0.0,
                                zero=self.zero,
                                type=self.array_char
                                )
        cache['dot']  = beeper( duration=self._u,
                                volume=vol,
                                zero=self.zero,
                                type=self.array_char
                                )
        cache['dash'] = beeper( duration=3.0*self._u,
                                volume=vol,
                                zero=self.zero,
                                type=self.array_char
                                )
        self.__dict__['_cache'] = cache

    def bytesForChar( self, c ):
        self._fillCache()
        parts = array(self.array_char)
        start = 1
        c = c.upper()
        space = self._cache['us']
        dot = self._cache['dot']
        dash = self._cache['dash']
        if not morse_dict.has_key( c ):
            print "Rejected Character: %c" % c
            return parts
        for i in morse_dict[c]:
            if start:
                start = 0
            else:
                parts += space
            if i == '.':
                parts += dot
            elif i == '-':
                parts += dash
            else:
                raise ValueError, "What part of morse is a '%s'?" % i
        return parts

    def bytesForWord( self, word ):
        self._fillCache()
        parts = array(self.array_char)
        start = 1
        for c in word:
            if start:
                start = 0
            else:
                parts += self._cache['cs']
            parts += self.bytesForChar(c)

        return parts

    def bytesForStr( self, text ):
        self._fillCache()
        text.strip()
        words = text.split()
        parts = array(self.array_char)
        parts += self._cache['us'] + self._cache['us']
        start = 1
        for word in words:
            if start:
                start = 0
            else:
                parts += self._cache['ws']
            parts += self.bytesForWord( word )
        parts += self._cache['us'] + self._cache['us']

        if sys.byteorder == 'big':
            parts.byteswap()
        return parts


if __name__ == '__main__':

    import esd


    mc = MorseCode()
    mc.sample_rate = esd.ESD_DEFAULT_RATE
    mc.frequency = 700
    mc.transmission_speed = 6
    #mc.character_speed = 6
    mc.is_8bit = false
    #mc.is_arrl_wpm = false
    #mc.is_arrl_spacing = false

    fmt = esd.ESD_PLAY | esd.ESD_MONO 
    if mc.is_8bit:
        fmt |= esd.ESD_BITS8
    else:
        fmt |= esd.ESD_BITS16
    print mc

    for i in ('_u','_Ta','_Tc','_Tw'):
        print "%s: %s" % ( i[1:], getattr(mc,i) )
    mc._fillCache()
    #print mc._cache

    sound = mc.bytesForStr( "Nick is nuts" )
    soundstr = sound.tostring()

    print "Done Computing"

    p = esd.Player(fmt, mc.sample_rate, '', 'morse')

    p.write( soundstr )


    #http://www.technology.niagarac.on.ca/courses/comp630/WavFileFormat.html
