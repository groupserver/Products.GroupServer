## Script (Python) "check_name"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groupId=""
##title=Check Group Name
##
import string

result = {}

if groupId == '':
    result['error'] = True
    result['message'] = '''<paragraph>The group name must
      be specified.</paragraph>'''
    return result

# Check for swearing
badWord = container.Scripts.check.bad_words(groupId)
if badWord:
    result['error'] = True
    result['message'] = '''<paragraph>No profanities (such as %s)
      are allowed in the group ID.</paragraph>''' % badWord 
    return result

goodChars = string.letters + string.digits + '_-'
for char in groupId:
    if char not in goodChars:
        result['error'] = True
        result['message'] = '''<paragraph>The character &#8220;%s&#8221;
          is not allowed in a group identifier.</paragraph>''' % char
        return result

entityExists = container.Scripts.check.entity_exists(groupId)
if entityExists:
    messages = [''] # The empty string in position 0 is delibarate

    m = '''<paragraph>The identifier &#8220;%s&#8221; cannot be used
      for the group as a site exists with the same ID.
      Please pick a new ID.</paragraph>''' % groupId
    messages.append(m)
    
    m = '''<paragraph>The identifier &#8220;%s&#8221; cannot be used
      for the group as a group exists with the same ID.
      Please pick a new ID.</paragraph>''' % groupId
    messages.append(m)

    m = '''<paragraph>The identifier &#8220;%s&#8221; cannot be used
      for the group as a user exists with the same ID.
      Please pick a new ID.</paragraph>''' % groupId
    messages.append(m)

    m = '''<paragraph>The identifier &#8220;%s&#8221; cannot be used
      for the group as a user-group exists with the same ID.
      Please pick a new ID.</paragraph>''' % groupId 
    messages.append(m)

    m = '''<paragraph>The identifier &#8220;%s&#8221; cannot be used
      for the group as a user-group exists with the same ID.
      This is a very odd occurance, please contact
      <link url="mailto:support@onlinegroups.net">support@onlinegroups.net</link>.</paragraph>''' % groupId
    messages.append(m)

    m = '''<paragraph>The identifier &#8220;%s&#8221; cannot be used
      for the group as a group-notification exists with the same ID.
      This is a very odd occurance, please contact
      <link url="mailto:support@onlinegroups.net">support@onlinegroups.net</link>.</paragraph>''' % groupId
    messages.append(m)

    result['error'] = True
    result['message'] = messages[entityExists]
    return result
    
result['error'] = False
result['message'] = '''<paragraph>The group name %s is
  valid.</paragraph>''' % groupId
return result

# --= Unit Tests =--
# >>> check_name('Foo Bar')['error'] == False
# >>> check_name('')['error'] == True
# >>> check_name('Foo Santorum Bar')['error'] == True
# >>> check_name('GroupServer.Org')['error'] == False
