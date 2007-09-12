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
#group = context.Scripts.get.group_by_id(groupid)
site = getattr(site_root.Content, divisionid)
assert(site != None)
group = getattr(site.groups, groupid)
assert(group != None)

groupUserIds = map(lambda u: u.getId(), group.Scripts.get.group_members())
unverifiedGroupUserIds = map(lambda u: u.getId(), 
                             group.Scripts.get.unverified_group_members()) 

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
    
    if userid in unverifiedGroupUserIds:
        # If the user is unverified, then remove them entirely.
        #   This may cause issues if the unverified user is queued to join
        #   more than one group; I know of no way for this to easily
        #   happen, so I am not too worried.
        site_root.acl_users.userFolderDelUsers([userid])
    else:
        # We may be removing a member who is also a posting
        #   member. Try and remove them from posting members
        #   so that they don't stay on the list of posting
        #   members after they've been removed from the group.
        container.posting.remove_users([userid], groupid, divisionid)
    
        # Otherwise, remove the user from the group.
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
