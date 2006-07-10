## Script (Python) "add_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userid=None,groupid=None,divisionid=None
##title=Add Users to Participation Coach List
##
from Products.PythonScripts.standard import html_quote

result = {}
assert groupid != None
assert divisionid != None
assert userid != None

site_root = context.site_root()
group = context.Scripts.get.group_by_id(groupid)
assert(group != None)

site_root = context.site_root()
group = context.Scripts.get.group_by_id(groupid)
assert(group != None)

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
group.manage_changeProperties(ptn_coach_id=userid)

result['error'] = False
result['message'] = '''<paragraph>%s is now the participation
  coach for %s.</paragraph>''' % (userName, group.title_or_id())
return result
