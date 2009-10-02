## Script (Python) "check_name"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=realLifeGroup=""
##title=Check Group Name
##

result = {}

if realLifeGroup == '':
    result['error'] = True
    result['message'] = '''<paragraph>The real life group
      field must be specified.</paragraph>'''
    return result

# Check for swearing
badWord = container.Scripts.check.bad_words(realLifeGroup)
if badWord:
    result['error'] = True
    result['message'] = '''<paragraph>No profanities (such as %s)
      are allowed in the real life group field.</paragraph>''' % badWord 
    return result

result['error'] = False
result['message'] = '''<paragraph>The real life group %s
  is valid.</paragraph>''' % realLifeGroup
return result

# --= Unit Tests =--
# >>> check_name('Foo Bar')['error'] == False
# >>> check_name('')['error'] == True
# >>> check_name('Foo Santorum Bar')['error'] == True
# >>> check_name('GroupServer.Org')['error'] == False
