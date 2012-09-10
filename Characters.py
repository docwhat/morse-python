# -*- python; coding: utf-8 -*-
"""
A set of morse code characters.
"""
#
#   characters.py -- Character collections.
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

morse_dict = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
    '.': '.-.-.-',   #<AAA>
    ',': '--..--',   #<MIM>
    '?': '..--..',   #<IMI>
    '/': '-..-.',    #<DN>
    '+': '.-.-.',    #<AR> End of Message
    '*': '...-.-',   #<SK> End of Work
    '=': '-...-',    #<BT>
    ';': '-.-.-.',   #<KR>
    ':': '---...',   #<OS>
    "'": '.----.',   #<WG>
    '"': '.-..-.',   #<AF>
    '-': '-....-',   #<DU>
    '_': '..--.-',   #<IQ>
    '$': '...-..-',  #<SX>
    '(': '-.--.',    #<KN>
    ')': '-.--.-',   #<KK>
    '&': '.-...',    #<AS> Wait
    '!': '...-.',    #<SN> Understood
    '%': '-.-.-',    #<KA> Starting Signal
    '@': '........', #<HH> Error
    '#': '.-.-..',   #<AL> Paragraph
    }

ARRL_list = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?+*=/'
ARRL_lessons = ( 'AERN+T',
                 'IOSDHC',
                 'UY.LMPG',
                 'F,WB=J/',
                 'KQXVZ?*',
                 '12345',
                 '67890' )

# Koch Method Lessons
KOCH_lessons = ( 'KMRSUA',
                 'PTLOWI',
                 '.NJE0FY',
                 ',VG5/Q',
                 '9ZH38B',
                 '?427C1',
                 'D6X=*+' )

ARRL_prosigns = '.,?+*=/'
