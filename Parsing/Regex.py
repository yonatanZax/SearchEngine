
import re

'''
.       - Any Character Except New Line
\d      - Digit (0-9)
\D      - Not a Digit (0-9)
\w      - Word Character (a-z, A-Z, 0-9, _)
\W      - Not a Word Character
\s      - Whitespace (space, tab, newline)
\S      - Not Whitespace (space, tab, newline)

\b      - Word Boundary
\B      - Not a Word Boundary
^       - Beginning of a String
$       - End of a String

[]      - Matches Characters in brackets
[^ ]    - Matches Characters NOT in brackets
|       - Either Or
( )     - Group

Quantifiers:
*       - 0 or More
+       - 1 or More
?       - 0 or One
{3}     - Exact Number
{3,4}   - Range of Numbers (Minimum, Maximum)


#### Sample Regexs ####

[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+





'''




def getRegexMatches(expression, text):
    pattern = re.compile(expression)
    matches = pattern.findall(text)
    print(matches)

    return matches


def runExpression(regexFunction):
    print("\n\n***      Running         ***\n")

    regexFunction()

    print("\n\nDONE")




def tokenizeRegex(text):

    tokenizerExpression = "[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+"

    getRegexMatches(tokenizerExpression,text)




def precentRegex():

    s1 = "blabla 23% blabla blabla 17.3 percentage blabla 51 percent blabla"

    # percentExpression = "\d+(.?)(\d+)?( percentage| percent|\S%)"
    numberWithDocExpression = '\d+.?\d+?'
    percentExpression = numberWithDocExpression + " percentage|" + \
                        numberWithDocExpression + " percent"
    # numberWithDocExpression + "%"

    matches = getRegexMatches(numberWithDocExpression,s1)

    for match in matches:
        number = match.split(' ')[0]
        s1 = s1.replace(match,number + '%')

    print(s1)



def dollarRegex():

    #dollarExpression = "(\d{1,3})(,\d{3})?"
    dollarExpression = "(\d{1,3})(,\d{3})?"
    s2 = "blabla 20,000 blabla 200 bla bla 5,200,455"


    pattern = getRegexMatches(dollarExpression,s2)




#runExpression(precentRegex)
#runExpression(dollarRegex)

'''

#ALL THESE REQUIRE THE WHOLE STRING TO BE A NUMBER
#For numbers embedded in sentences, see discussion below

#### NUMBERS AND DECIMALS ONLY ####
#No commas allowed
#Pass: (1000.0), (001), (.001)
#Fail: (1,000.0)
^\d*\.?\d+$

#No commas allowed
#Can't start with "."
#Pass: (0.01)
#Fail: (.01)
^(\d+\.)?\d+$

#### CURRENCY ####
#No commas allowed
#"$" optional
#Can't start with "."
#Either 0 or 2 decimal digits
#Pass: ($1000), (1.00), ($0.11)
#Fail: ($1.0), (1.), ($1.000), ($.11)
^\$?\d+(\.\d{2})?$

#### COMMA-GROUPED ####
#Commas required between powers of 1,000
#Can't start with "."
#Pass: (1,000,000), (0.001)
#Fail: (1000000), (1,00,00,00), (.001)
^\d{1,3}(,\d{3})*(\.\d+)?$

#Commas required
#Cannot be empty
#Pass: (1,000.100), (.001)
#Fail: (1000), ()
^(?=.)(\d{1,3}(,\d{3})*)?(\.\d+)?$

#Commas optional as long as they're consistent
#Can't start with "."
#Pass: (1,000,000), (1000000)
#Fail: (10000,000), (1,00,00)
^(\d+|\d{1,3}(,\d{3})*)(\.\d+)?$

#### LEADING AND TRAILING ZEROES ####
#No commas allowed
#Can't start with "."
#No leading zeroes in integer part
#Pass: (1.00), (0.00)
#Fail: (001)
^([1-9]\d*|0)(\.\d+)?$

#No commas allowed
#Can't start with "."
#No trailing zeroes in decimal part
#Pass: (1), (0.1)
#Fail: (1.00), (0.1000)
^\d+(\.\d*[1-9])?$



'''

