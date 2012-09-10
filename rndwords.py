#!/usr/bin/env python
# -*- python; coding: utf-8 -*-
LICENSE = \
"""
   rndwords -- Random Words in Morse
   Copyright (C) 2012 Christian Höltje

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import getopt, sys
import random

sys.path.append( '/usr/local/lib/morse' )
from Characters import morse_dict,ARRL_list,ARRL_lessons,KOCH_lessons,ARRL_prosigns
from HamWords import randomHamWord

class OutOfWordsError(IndexError): pass

true = 1
false = 0

class RndWords:
    default_dictionaries = ( "/usr/share/dict/words",
                             "/usr/lib/dict/words",
                             "common_words" )

    options = ( ('d:', 'dict', 'Dictionary File'),
                ('c', 'no-caps', 'Ignore words that begin with capitals'),
                ('l:', 'arrl-lesson=', 'Limit words by ARRL lesson number (or less)'),
                ('L',  'list-arrl-lessons', 'List all ARRL lessons'),
                ('k:', 'koch-lesson=', 'Limit words by Koch lesson number (or less)'),
                ('K',  'list-koch-lessons', 'List all ARRL lessons'),
                ('a',  'all-arrl', 'Limit words by all ARRL exam characters'),
                ('A',  'list-all-arrl', 'List all the ARRL exam characters'),
                ('m',  'all-morse', 'Limit words by morse characters'),
                ('M',  'list-all-morse', 'List all morse characters'),
                ('h', 'hamwords', 'Use HamWords library for additional words'),
                ('u:', None, 'Use only these characters'),
                ('x:', 'extra=', 'Use these extra characters (in addition)'),
                ('p:', 'priority=', 'Give these characters priority'),
                ('n:', None, 'Number of words to select'),
                (None, 'seconds=', 'Minimum number of seconds worth of words'),
                ('o:', None, 'Output a wave file'),
                ('e',  None, 'Output sound via ESD'),
                ('g',  None, 'Output sound via PyGame'),
                ('t:', 'text=', 'Play this text with no limiting.'),
                ('s:', 'strip-file=', 'Read a file, stripping out characters'),
                ('v', 'verbose', 'Display lots of extra info'),
                (None, 'transmission_speed=', 'Number of words per minute (def: 6)'),
                (None, 'character_speed=', 'Speed of individual characters (def: 18)'),
                (None, 'sample_rate=', 'Sample rate of the sound output'),
                (None, 'frequency=', 'Frequency of the beep (def: 720)'),
                (None, 'mono', 'Mono sound output'),
                (None, 'stereo', 'Stereo sound output'),
                (None, '8bit', '8bit sound output'),
                (None, '16bit', '16bit sound output'),
                (None, 'volume=', 'Set the Volume (0-100)'),
                (None, 'license', "Display the License"),
                )

    def extra_help( self ):
        print """
REQUIRED OPTIONS:
  You must use -l, -k, -a, -m, or -u to choose words that are would be
  appropriate for specific lessons, the exam, morse code, or
  you may use a manually entered list of characters.  You can
  see these list of characters by using the capital version of
  each letter: -L, -K, -A, or -M  (there is no list for -u)

  Alternatively, you can specify text exact text to transmit
  by using -t 'text to play'.  You need quotes to have it
  work correctly.

OTHER USEFUL OPTIONS:
  With no options (other than those reqired and mentioned above)
  a minimum of 60 seconds worth of words is generated.
  You can change this by specifying the number of words (-n) or
  the minimum number of seconds (--seconds) to transmit.

  Also by default, no code is actually generated.  Words are
  chosen and printed.  If you wish to generate actual sound
  you must use an output option.
  Use -e to generate sound for ESound (found on linux systems)
  or use -o <file name> to create a .wav file suitable for
  playing under most systems.

  You can specify an alternate dictionary file.  This is a file
  with one word per line.  Most unix systems come with a large file
  in /usr/share/dict/words or /usr/lib/dict/words.  rndwords will
  use those by default, but if you wish to use your own or the
  rather short 'common_words' that comes with rndwords you can use
  the -d option.

  The -v option will show extra statistics and info about how
  rndword created the word lists.
"""

    def usage( self, error=None ):
        if error:
            print "Errors:\n%s\n" % error
        print "Random Words in Morse   -- Copyright (C) 2002, 2008 Christian Höltje"
        print
        print "Usage: %s [options]" % sys.argv[0]
        print
        print "Args:"
        for opt in self.options:
            short = opt[0]
            long = opt[1]
            desc = opt[2]
            if short:
                short = "-%s" % short.replace( ':', ' <arg>' )
            else:
                short = ""
            if long:

                long = "--%s" % long.replace( '=', ' <arg>' )
            else:
                long = ""
            print "%-8s %-20s  %s" % (short, long, desc)

        print
        if not error:
            self.extra_help()

    dict = None
    errors = None
    dictionary = None
    output = None
    debug = false
    stat_count = 0
    stat_bad = 0
    stat_good = 0
    verbose = None
    stdout = None

    def __init__( self ):
        # Initializing Variables
        self.dict = {}
        self.dictionary = []
        self.errors = []
        self.output = None
        self.stdout = sys.stdout
        self.output_options = { 'is_8bit': false,
                                'is_stereo': false,
                                'volume': 100,
                                'frequency': 720,
                                'transmission_speed': 6,
                                'character_speed': 18,
                                'sample_rate': None }
        random.seed()

        short_opts = []
        long_opts = [ 'debug' ]
        for i in self.options:
            if i[0]: short_opts.append( i[0] )
            if i[1]: long_opts.append( i[1] )
        try:
            (opts, args) = getopt.getopt( sys.argv[1:],
                                          "".join(short_opts),
                                          long_opts )
        except getopt.GetoptError:
            # print help information and exit:
            self.usage( "Invalid Arguments" )
            sys.exit(2)

        output = None
        if len(opts) == 0:
            self.usage()
            sys.exit(1)
        if len(args) > 0:
            self.usage( "Don't know what to do with argument(s): %s" % args )
            sys.exit(2)

        for opt, arg in opts:
            if not self.checkLength( opt, arg ) and\
               not self.checkCharacters( opt, arg ) and\
               not self.checkOutput( opt, arg ) and \
               not self.checkFiles( opt, arg ) and\
               not self.checkPrintings( opt, arg ):
                self.errors.append( 'Unknown option %s %s' % ( opt, arg ) )
        self.verifyOptions()
        if self.errors:
            self.usage( "\n".join( self.errors ) )
            sys.exit(1)
        self.setDefaults()

    def checkLength( self, opt, arg ):
        if opt == '-n':
            self.dict['number_of_words'] = int(arg)
        elif opt == '--seconds':
            self.dict['minimum_seconds'] = int(arg)
        else:
            return false
        return true

    def checkCharacters( self, opt, arg ):
        if opt in ('-l', '--arrl-lesson',
                   '-k', '--koch-lesson' ):
            if opt in ('-k', '--koch-lesson'):
                lessons = KOCH_lessons
            else:
                lessons = ARRL_lessons
            if arg == 'all':
                self.dict['character_list'] = "".join( lessons )
            elif int(arg) >= 1 and int(arg) <= (len(lessons)+1):
                if int(arg) == 1:
                    self.dict['character_list'] = lessons[0]
                else:
                    self.dict['character_list'] = "".join(lessons[:int(arg)])
            else:
                self.errors.append( "Lessons range from 1 and %s" %\
                                    (len(lessons)+1) )
        elif opt in ('-a', '--all-arrl'):
            self.dict['character_list'] = ARRL_list
        elif opt in ('-m', '--all-morse'):
            self.dict['character_list'] = morse_dict.keys()
        elif opt == '-u':
            self.dict['character_list'] = arg.upper()
        elif opt in ('-p','--priority'):
            self.dict['priority_list'] = arg.upper()
        elif opt in ('-c','--no_caps'):
            self.dict['no_caps'] = true
        elif opt in ('-x','--extra'):
            self.dict['extra_characters'] = arg.upper()
        elif opt in ('-h','--hamwords'):
            self.dict['hamwords'] = true
        else:
            return false
        return true

    def checkOutput( self, opt, arg ):
        oopts = self.output_options
        if opt == '-e':
            from OutESD import OutESD
            self.output = OutESD()
        elif opt == '-o':
            if arg == '-':
                fd = sys.stdout
                self.stdout = sys.stderr
            else:
                fd = open( arg, "wb" )
            from OutWav import OutWav
            self.output = OutWav(fd=fd)
        elif opt == '-g':
            from OutPyGame import OutPyGame
            self.output = OutPyGame()
        elif opt in ('--8bit',):
            oopts['is_8bit'] = true
        elif opt in ('--16bit',):
            oopts['is_8bit'] = false
        elif opt in ('--stereo',):
            oopts['is_stereo'] = true
        elif opt in ('--mono',):
            oopts['is_stereo'] = false
        elif opt in ('--volume',):
            vol = int(arg)
            if vol < 0 or vol > 100:
                self.errors.append( "Volume must be between 0 and 100" )
            else:
                oopts['volume'] = vol
        elif opt in ('--frequency',):
            freq = int(arg)
            oopts['frequency'] = freq
        elif opt in ('--transmission_speed',):
            ts = int(arg)
            oopts['transmission_speed'] = ts
        elif opt in ('--character_speed',):
            cs = int(arg)
            oopts['character_speed'] = cs
        elif opt in ('--sample_rate',):
            sr = int(sr)
            if sr not in ( '11025', '22050', '44100' ):
                self.errors.append( "Sample rate must be either "\
                                    "11025hz, 22050hz, or 44100hz" )
            else:
                oopts['sample_rate'] = sr
        else:
            return false
        return true

    def checkFiles(self, opt, arg):
        if opt in ( '-d', '--dict' ):
            try:
                fd = open( arg, "r" )
            except IOError, reason:
                print "Cannot open your dictionary:\n\t%s" % reason
                sys.exit(2)
            self.dict['dict_fd'] = fd
        elif opt in ('-s', '--strip-file'):
            self.dict['strip_file'] = arg
        elif opt in ('-t', '--text'):
            self.dict['raw_text'] = arg
        else:
            return false
        return true

    def checkPrintings(self, opt, arg):
        if opt in ('-v', '--verbose'):
            self.verbose = sys.stderr
        elif opt == '--debug':
            self.debug = true
            self.verbose = sys.stderr
        elif opt == '--license':
            print LICENSE
            sys.exit(0)
        elif opt in ('-L', '--list-arrl-lessons'):
            print "ARRL Lesson List\n"
            count = 1
            for l in ARRL_lessons:
                print "%d: %s" % (count, l)
                count += 1
            sys.exit(0)
        elif opt in ('-K', '--list-koch-lessons'):
            print "Koch Lesson List\n"
            count = 1
            for l in KOCH_lessons:
                print "%d: %s" % (count, l)
                count += 1
            sys.exit(0)
        elif opt in ("-A",'--list-all-arrl'):
            print "ARRL Exam Character Lists\n"
            print ARRL_list
            sys.exit(0)
        elif opt in ('-M','--list-all-morse'):
            print "All Morse Characters\n"
            print
            l = morse_dict.keys()
            l.sort()
            print l
            sys.exit(1)
        else:
            return false
        return true


    def verifyOptions(self):
        d = self.dict
        err = self.errors
        if d.has_key('minimum_seconds') and \
           d.has_key('number_of_words'):
            err.append( "You cannot select a minimal number of seconds and "\
                        "the number of words." )
        if d.has_key('raw_text') and d.has_key('strip_file'):
            err.append( "You cannot specify text and a file to strip" )
        if d.has_key('raw_text'):
            if d.has_key('character_list') or \
               d.has_key('priority_list') or \
               d.has_key('dict_fd'):
                err.append( "If you specify the text to use, then you "\
                            "cannot set the characters, priority or "\
                            "dictionary to use" )
        else:
            if not d.has_key('character_list'):
                err.append( "You must have a character list specified" )

    def setDefaults(self):
        d = self.dict

        self.hamwords = false
        if d.has_key('character_list'):
            self.character_list = d['character_list']
            del d['character_list']
            if d.has_key('extra_characters'):
                self.character_list += d['extra_characters']
                del d['extra_characters']
            self.character_list += " "
            self.priority_list = ""
            if not d.has_key('number_of_words') and \
               not d.has_key('minimum_seconds'):
                d['minimum_seconds'] = 60
            if d.has_key('hamwords'):
                self.hamwords = true
                del d['hamwords']



        if d.has_key('no_caps'):
            self.no_caps = true
            del d['no_caps']
        else:
            self.no_caps = false

        if d.has_key('priority_list'):
            self.priority_list = d['priority_list']
            del d['priority_list']

        if self.output:
            for k in self.output_options.keys():
                v = self.output_options[k]
                if v != None:
                    setattr( self.output, k, v )

        if d.has_key('strip_file'):
            d['raw_text'] = self.stripFile( d['strip_file'] )

        if d.has_key('dict_fd'):
            dict_fd = d['dict_fd']
            del d['dict_fd']
            self.dictionary = dict_fd.readlines()
        else:
            if not d.has_key('raw_text'):
                dict_fd = None
                for file in self.default_dictionaries:
                    try:
                        dict_fd = open( file, "r" )
                        break
                    except IOError:
                        pass
                if not dict_fd:
                    self.errors.append( "Unable to find a dictionary" )
                else:
                    self.dictionary = dict_fd.readlines()

        if self.debug:
            sys.stderr.write( "Config: %s\n" % d )
            sys.stderr.write( "Output: %s\n" % self.output )
            sys.stderr.write( "Output Options: %s\n" % self.output_options )
            sys.stderr.write( "Paris: %s seconds\n" % self.getSeconds('paris') )

    def getSeconds(self, word):
        """
        Get the number of seconds a word takes to transmit.
        """
        total_units = 0
        for char in list(word.upper()):
            units = 0
            if not morse_dict.has_key(char):
                if char == ' ':
                    units += 7
                continue
            trans = morse_dict[char]
            for ditdah in list(trans):
                if ditdah == '.':
                    units += 2
                if ditdah == '-':
                    units += 4
            # correction for trailing unit
            units -= 1
            total_units += units + 3
            del units
        # Word space + correction for trailing word space
        total_units += 7 - 3
        units_per_sec = self.output_options['transmission_speed']*50.0/60.0
        return float(total_units)/units_per_sec

    def getRandomWord( self ):
        retval = None
        if self.hamwords and random.randint( 0, 2 ) == 1:
            self.stat_count += 1
            retval = randomHamWord()
        else:
            word = self.getRandomDictWord()
            if self.no_caps:
                while word[0].isupper():
                    word = self.getRandomDictWord()
            retval = word

        if retval is None:
            raise ProgrammingError, "Null word generated!!"
        else:
            return retval

    def getRandomDictWord( self ):
        if len(self.dictionary) == 0:
            raise OutOfWordsError, "There are no more words left!"

        index = random.randint( 0, len(self.dictionary) - 1 )
        word = self.dictionary[index]
        self.dictionary[index] = self.dictionary[-1]
        del self.dictionary[-1]
        self.stat_count += 1
        return word.strip()

    def getRandomWordWithCharacters( self ):
        found = false
        word = "--ERROR--"
        while not found:
            word = self.getRandomWord()
            if self.debug:
                self.verbose.write( "Checking %-45s  " % ("'%s'" % word) )
            valid = self.isWithinSet( self.character_list, word )
            if valid and self.priority_list:
                valid = self.isWithinSet( word.upper(), self.priority_list )
            if valid:
                self.stat_good += 1
                if self.debug:
                    self.verbose.write( "GOOD\n" )
                found = true
            else:
                self.stat_bad += 1
                if self.debug:
                    self.verbose.write( "reject\n" )
            if self.verbose:
                self.verbose.flush()
        return word

    def isWithinSet(self, set, word):
        for c in word.upper():
            if c not in set: return false
        return true

    def getWords( self ):
        words = []
        if self.dict.has_key('number_of_words'):
            for count in range( 0, self.dict['number_of_words'] ):
                words.append( self.getRandomWordWithCharacters() )

        elif self.dict.has_key('minimum_seconds'):
            seconds = 0
            min = self.dict['minimum_seconds']
            while seconds < min:
                try:
                    word = self.getRandomWordWithCharacters()
                    seconds += self.getSeconds( word )
                    words.append( word )
                except OutOfWordsError:
                    break

        return " ".join( words )

    def stripFile( self, file ):
        fd = open( file, "r" )
        contents = fd.read().split()
        fd.close()

        words = []
        for word in contents:
            self.stat_count += 1
            if self.isWithinSet( self.character_list, word ):
                self.stat_good += 1
                words.append( word )
            else:
                self.stat_bad += 1

        return " ".join(words)

    def transmit(self):
        if self.verbose:
            if self.dictionary:
                has_dict = true
                text = "Words in dictionary: %s\n"\
                       "Character List: %s\n"\
                       "Priority List: %s\n" %\
                       ( len(self.dictionary),
                         self.character_list,
                         self.priority_list )
                self.stdout.write( text )
            else:
                has_dict = false

        if self.dict.has_key('raw_text'):
            words = self.dict['raw_text']
        else:
            words = self.getWords()

        if self.verbose and has_dict:
            text = "Stats: %d searched, %d rejected, %d good\n"\
                   "Length: %d seconds\n" %\
                   ( self.stat_count, self.stat_bad, self.stat_good,
                     self.getSeconds( words ) )
            self.verbose.write( text )

        if self.output:
            if self.verbose:
                text = "Overall Transmission Speed: %s wpm\n"\
                       "Character Transmission Speed: %s wpm\n" %\
                       ( self.output.transmission_speed,
                         self.output.character_speed )
                self.stdout.write( text )
            self.stdout.write( "\nTransmitting Morse....." )
            self.stdout.flush()
            self.output.generate( words )
            self.stdout.write( "Done!\n" )
            self.stdout.flush()
        text = "Words: %s\n" % words
        self.stdout.write(text)

if __name__ == "__main__":
    rndwords = RndWords()
    rndwords.transmit()


