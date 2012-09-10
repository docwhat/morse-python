# Christian Höltje's Python Morse Tutoring Program

Get the latest information from [github](http://github.com/docwhat/morse-python).

## Original README intro

Hello all!

I wrote this software because a friend of mine, Paul Guido (N5UIT)
was doing a morse course for the San Antonio Radio Club.  The software
he used was not full free.  It had a shareware limited mode and cost
$40 to register.

This seemed to go against the HAM spirit of promoting the hobby and
also offended me in that I know writing morse software isn't hard.
Also as an advocate of Free (as in liberty, something all Texans
care about) Software I thought this was something that should be
free.  (See http://www.gnu.org/ for more info)

So I wrote my own.  It wasn't very hard.  At this time I have spent
significantly less than a week of time to produce a full featured,
correct sounding, perfect timed version that'll help anyone pass
the ARRL and FCC exams.

I hope you like it.

BTW: The webster2 is *not* GPL.  It's technically in the public
domain as it's 1934 copyright has expired.  It's the Webster's
Unabridged dictionary distilled into a word list.  I got this
from NetBSD and seems to have been formatted by a James Woods.

Ciao!

-– Christian Höltje

## Updated information

This apparently works with the Python 2.7.2 that comes with Mac OS X 10.8.1,
who would have guessed that this code would work 10 years later!

To use this, run the `rndwords.py` app.  It has a bunch of flags
to use different outputs. I've only tested the `-o <filename.wav>` output method.

## Requirements
 * [Python](http://python.org/) (version 2.2 or later)

## Suggested Extras

Note: As of 2012, these extra packages may or may not work anymore. I haven't tested them yet.

 * PyGame -- a cross platform game development library for playing sound on a lot of platforms (Windows, Unix, Mac OS, etc...)
 * SDL -- Required for PyGame
 * PyESD -- for playing under ESound in Unix operating systems.
