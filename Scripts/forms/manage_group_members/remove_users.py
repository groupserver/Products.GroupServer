## Script (Python) "remove_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userids=[],groupid=None,divisionid=None
##title=Remove Users from the Group
##
from Products.PythonScripts.standard import html_quote

result = {}
assert groupid != None
assert divisionid != None
assert userids.append # The userids is a list

site_root = context.site_root()
group = context.Scripts.get.group_by_id(groupid)
assert(group != None)

groupUserIds = map(lambda u: u.getId(), group.Scripts.get.group_members())

ptnCoachId = group.getProperty('ptn_coach_id', '')
ptnCoach = site_root.acl_users.getUser(ptnCoachId)

# Only inform the participation coach if he or she is *not* the user
#   who is removing all the people at the moment.
requestingUser = context.REQUEST.AUTHENTICATED_USER
notifyPtnCoach = ptnCoach and (ptnCoach.getId() != requestingUser.getId())
names = []
for userid in userids:
    user = site_root.acl_users.getUser(userid)
    userName = user.getProperty('preferredName')
    names.append(userName)
    
    user.del_groupWithNotification('%s_member' % groupid)
    if notifyPtnCoach:
        ptnCoach.send_notification('leave_group_admin', groupid,
                                   n_dict={'joining_user': user,
                                           'joining_group': group})
    
userNames = ', '.join(names)
result['error'] = False
m = (len(userids) == 1) and ('member you selected (%s) has' % userNames) \
    or ('%d members you selected (%s) have' % (len(userids), userNames))
result['message'] = '''<paragraph>The %s been removed from
  %s.</paragraph>''' % (m, group.title_or_id())
return result
