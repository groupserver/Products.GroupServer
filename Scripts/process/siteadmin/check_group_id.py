## Script (Python) "check_group_id"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groupId='',divisionId=''
##title=Check Group ID
##
import string

result = {}
site_root = context.site_root()
division = context.Scripts.get.division_object()
groups = getattr(division, 'groups')

groupId=groupId.lower()

if groupId == '':
    result['error'] = True
    result['message'] = 'The group id must be specified.'
    return result

# Check for swearing
badWord = context.Scripts.forms.siteinfo.bad_words(groupId)
if badWord:
    result['error'] = True
    result['message'] = '''No profanities (such as %s) are allowed in
      the group ID.''' % badWord 
    return result

validChars = string.digits + string.lowercase + '-._'
for c in groupId:
    if c not in validChars:
        result['error'] = True
        result['message'] = '''The character &#8220;%c&#8221; is not
          allowed in the group ID. Please rewrite the group ID.''' % c
        return result

userGroups = site_root.acl_users.getGroupNames()
newUsergroupName = '%s_member' % groupId
if newUsergroupName in userGroups:
    result['error'] = True
    result['message'] = '''There is already a user-group with the ID
      &#8220;%s&#8221;. Please pick another ID''' % groupId
    return result

# If we are here, then all is well in the world
result['error'] = False
result['message'] = '''The group ID %s is valid.''' % groupId
return result
