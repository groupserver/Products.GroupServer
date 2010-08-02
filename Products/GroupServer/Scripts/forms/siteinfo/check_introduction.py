## Script (Python) "check_introduction"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=introduction=""
##title=Check Introduction
##

result = {}

badWord = container.bad_words(introduction)
if badWord:
    result['error'] = True
    result['message'] = '''No profanities (such as %s) are allowed in
      the introduction text. Please rewrite your introduction.''' % badWord 
    return result

result['error'] = False
result['message'] = '''The introduction is acceptable.'''
return result

# --= Unit Tests =--
# >>> check_introduction('')['error'] == False
# >>> check_introduction('Foo bar wibble blarg.')['error'] == False
# >>> check_introduction('Foo bar santorum blarg.')['error'] == True

