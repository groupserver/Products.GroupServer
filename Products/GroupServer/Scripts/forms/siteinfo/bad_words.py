## Script (Python) "bad_words"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=words=""
##title=Bad Words
##

wordsToCheck = filter(lambda c: c in string.letters or c == " ", words)

badWords = ['fuck', 'cunt', 'bitch', 'cock', 'santorum', 'arse',
            'bollocks', 'anal', 'shit', 'whore', 'xxx', 'cock']

for badWord in badWords:
    for word in wordsToCheck.split():
        if badWord == word.lower():
            return badWord

return False
