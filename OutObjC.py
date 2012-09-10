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

from OutWav import OutWav
import objc
from AppKit import NSSound
from tempfile import mkdtemp
import os
from time import sleep
from shutil import rmtree

class OutObjC(OutWav):
    def generate(self, text, host="", name="Morse" ):
        tmpdir = mkdtemp()
        try:
            filename = os.path.join(tmpdir, "objc.wav")
            fd = open(filename, 'wb')
            self.bytesForStr( text ).tofile(fd)
            fd.close()

            player = NSSound.alloc()
            try:
                player.initWithContentsOfFile_byReference_(filename, False)
                player.play()
                sleep(player.duration() + 1)
            finally:
                del player
        finally:
            rmtree(tmpdir)

if __name__ == '__main__':

    e = OutObjC()
    e.is_8bit = False
    e.is_stereo = True

    print e
    print e._morse

    e.generate( "This is text we want played via ObjC" )
