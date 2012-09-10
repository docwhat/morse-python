#!/usr/bin/env python
# -*- python; coding: utf-8 -*-
#
#   OutPyGame.py -- Output to PyGame's Mixer
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

from Morse import *
from Strict import Strict
from cStringIO import StringIO
from OutWav import OutWav
import pygame

true = 1
false = 0

class OutPyGame(OutWav):

    def generate(self, text ):
        self.is_8bit = false
        self.is_stereo = true
        fobj = StringIO( self.bytesForStr( text ).tostring() )

        time = pygame.time
        mixer = pygame.mixer
        mixer.init(self.sample_rate)
        snd = pygame.mixer.Sound( fobj )
        channel = snd.play()
        
        while channel.get_busy():
            time.wait(1000)

        pygame.mixer.quit()


if __name__ == '__main__':

    p = OutPyGame()
    p.sample_rate = 44100
    p.generate( "This is text we want played via PyGame." )
    
