#!/usr/bin/env python
# -*- python; coding: utf-8 -*-

from Characters import ARRL_prosigns
import random
random.seed()

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
bands = [ '160 meter',
          '80 meter',
          '40 meter',
          '30 meter',
          '20 meter',
          '17 meter',
          '15 meter',
          '12 meter',
          '10 meter',
          '6 meter',
          '2 meter',
          '1.25 meter',
          '70 cm',
          '33 cm',
          '23 cm' ]

qsignals = [ 'QRG',
             'QRL',
             'QRM',
             'QRN',
             'QRO',
             'QRP',
             'QRQ',
             'QRS',
             'QRT',
             'QRU',
             'QRV',
             'QRX',
             'QRZ',
             'QSB',
             'QSK',
             'QSL',
             'QSN',
             'QSO',
             'QSP',
             'QST',
             'QSX',
             'QSY',
             'QTB',
             'QTC',
             'QTH',
             'QTR', ]

def callSign():
    p1 = random.randint( 1, 2 )
    p2 = random.randint( p1, p1+1 )
    sign = ""
    for i in range(0, p1):
        if i == 0:
            c = "WK"
            sign += c[random.randint( 0, len(c)-1 )]
        else:
            sign += alphabet[random.randint( 0, len(alphabet)-1 )]
    sign += str( random.randint( 1, 9 ) )
    for i in range(0, p2):
        sign += alphabet[random.randint( 0, len(alphabet)-1 )]

    return sign

def radioModel():
    models = ['Rasu','Fennwood','Ikon','Realist']

    model_number = ""
    for i in range(0, random.randint( 1, 3 ) ):
        index = random.randint( 0, len(alphabet) - 1 )
        model_number += alphabet[index]
    for i in range(0, random.randint( 1, 2 ) ):
        model_number += str( random.randint( 1, 9 ) )
    model_number += '0'*random.randint( 1, 5 )

    index = random.randint( 0, len(models) - 1 )
    model = models[index]

    if random.randint(0,1):
        return "%s %s" % ( model, model_number )
    else:
        return "%s %s" % ( model_number, model )

def hamBand():
    index = random.randint( 0, len(bands) - 1 )
    return bands[index]
    
def bandList():
    b = bands[:]
    band_list = []
    for i in range(0, random.randint( 1, 4 ) ):
        index = random.randint( 0, len(b) - 1 )
        band_list.append( b[index] )
        b[index] = b[-1]
        del b[-1]
    return ", ".join( band_list )

def prosign():
    index = random.randint( 0, len(ARRL_prosigns) - 1 )
    return ARRL_prosigns[index]

def qsignal():
    index = random.randint( 0, len(qsignals) - 1 )
    return qsignals[index]

def randomHamWord():
    choices = [ callSign,
                radioModel,
                hamBand,
                prosign,
                qsignal ]
    index = random.randint( 0, len(choices) - 1 )

    return choices[index]()
    
if __name__ == '__main__':
    print "callSign: %s" % callSign()
    print "radioModel: %s" % radioModel()
    print "hamBand: %s" % hamBand()
    print "bandList: %s" % bandList()
    print "prosign: %s" % prosign()
    print "qsignal: %s" % qsignal()
    print "randomHamWord: %s" % randomHamWord()
