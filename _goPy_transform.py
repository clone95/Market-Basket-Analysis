# to use accented characters in the code
# -*- coding: cp1252 -*-
# ===============================
# version: v04 \ Python3 \ Orange3
# ===============================



#_______________________________________________________________________________
# Modules to Evaluate
import csv
import unicodedata



#_______________________________________________________________________________
# convert string to unicode format
# in Python3 all strings are sequences of Unicode characters
# so there is no need to transform strings into Unicode
# therefore this method is deprecated for Python3
##def to_unicode( obj, encoding='utf-8' ):
##    if isinstance( obj, basestring ):
##        if not isinstance( obj, unicode ):
##            obj = unicode( obj, encoding )
##    return obj


#_______________________________________________________________________________
# remove accents in an unicode string
def remove_accents( aString, encoding='utf-8' ):
    #next instruction is not necessary in Python3
    #aString_unicode = to_unicode( aString, encoding )
    aString_unicode = aString
    nfkd_form = unicodedata.normalize( 'NFKD', aString_unicode )
    only_ascii_form = nfkd_form.encode( 'ascii', 'ignore' ).decode( encoding )
    return only_ascii_form


#_______________________________________________________________________________
# define the "normalize" process that applies to each string
def normalizeString( aString ):
    # substitute "=" symbol because it is used in the basket format
    symbolToReplace = "="
    #symbolNew = "|" #this substitution does not work in Orange3
    symbolNew = "+"
    aString = aString.replace( symbolToReplace, symbolNew )
    
    # eliminate spaces (white characters)
    symbolToReplace = " "
    symbolNew = ""
    aString = aString.replace( symbolToReplace, symbolNew )

    # eliminate quotes (" character)
    symbolToReplace = "\""
    symbolNew = "$"
    aString = aString.replace( symbolToReplace, symbolNew )
    
    # eliminate accent characters
    encoding_windows = "iso-8859-1" #"cp1252" #"latin-1" #"latin9" 
    aString = remove_accents( aString, encoding_windows )
    
    # to lower
    aString = aString.lower()
 
    return aString



#_______________________________________________________________________________
# generate the "basket information" from a dataset file with the format:
# TransactionID;ProductID
def generateBasket( fileNameIN ):
    indexTransaction = 0
    indexItem = 1
    basket = {}
    #with open( fileNameIN, 'rb' ) as f:
    with open( fileNameIN ) as f:
        reader = csv.reader( f, delimiter=';', quoting=csv.QUOTE_NONE )
        for row in reader:
            #print( row )
            
            transactionID = row[ indexTransaction ]
            if transactionID not in basket.keys():
                basket[ transactionID ] = {}

            itemID = row[ indexItem ]
            itemID = normalizeString( str( itemID ) )
            if itemID not in basket[ transactionID ].keys():
                basket[ transactionID ][ itemID ] = 0
                
            basket[ transactionID ][ itemID ] += 1
    return basket



#_______________________________________________________________________________
# generate a dataset file with the ".basket" structure expected by Orange_workflow"
def generateDataFile( basket, fileNameOUT ):
    with open ( fileNameOUT, mode='wt', encoding='utf-8' ) as f:
        for n, transactionID in enumerate(basket.keys()):
            line = ""
            for el in basket[transactionID]:
                if basket[transactionID][el] == 1:
                    line += str(normalizeString(remove_accents(el))) + ","
                else:
                    line += str(normalizeString(remove_accents(el))) + "={}".format(basket[transactionID][el]) + ","

            f.write( line[:-1] + '\n' )



#_______________________________________________________________________________
# the main of this module (in case this module is imported from another module)
if __name__=="__main__":
    # assumption: the CSV file does not contain the header line
    # (make sure that the export script does not generate the CSV header)
    fIN = "Final_Output.txt"
    fOUT = "final_basket.basket"
    print()
    print( ">> 1. Generate Basket structure from CSV file: " + fIN )
    basket = generateBasket( fIN )
    print( ">> 2. Generate .basket dataset file: " + fOUT )
    generateDataFile( basket, fOUT )





