## Script (Python) "add_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userid=None,groupid=None,divisionid=None
##title=Add User to the Participation Coach List
##
from Products.PythonScripts.standard import html_quote

result = {}
assert groupid != None
assert divisionid != None
assert userid != None

site_root = context.site_root()
group = context.Scripts.get.group_by_id(groupid)
assert(group != None)

listManager = site_root.objectValues('XWF Mailing List Manager')[0]
assert (listManager != None), "List manager not found"
groupList = listManager.get_list(groupid)
assert groupList != None, "Email list %s not found" % groupid

userName = group.Scripts.get.user_realnames(userid,
                                            preferred_name_only=True)

# Check that the user is a member of the group.
userIds = map(lambda u: u.getId(), group.Scripts.get.group_members())
if userid not in userIds:
   result['error'] = True
   result['message'] = '''%s (%s) does not belong to the group %s,
     so cannot be a participation coach.''' % (userName, userid,
                                               group.title_or_id())
   return result
# Check that the user is not moderated
moderatedMembers = group.Scripts.get.group_members_moderated()
moderatedMembersIds = map(lambda m: m.getId(), moderatedMembers)
if userid in moderatedMembersIds:
   result['error'] = True
   result['message'] = '''%s (%s) is currently a moderated
     member of the group %s, so cannot be a participation
     coach.''' % (userName, userid, group.title_or_id())

# Set the participation coach.
if group.hasProperty('ptn_coach_id'):
   group.manage_changeProperties(ptn_coach_id=userid)
else:
   group.manage_addProperty('ptn_coach_id', userid, 'string')
# ...and for the mailing list
if groupList.hasProperty('ptn_coach_id'):
   groupList.manage_changeProperties(ptn_coach_id=userid)
else:
   groupList.manage_addProperty('ptn_coach_id', userid, 'string')

result['error'] = False
result['message'] = '''<paragraph>%s is now the participation
  coach for %s.</paragraph>''' % (userName, group.title_or_id())
return result
