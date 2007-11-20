## Script (Python) "subscribe_group"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=division_id, group_id, unsubscribe=0
##title=
##
from Products.XWFCore.XWFUtils import getOption
user = context.REQUEST.AUTHENTICATED_USER
user_id = user.getUserName()
site_root = context.site_root()
subscribe = not unsubscribe

listManager = site_root.objectValues('XWF Mailing List Manager')[0]

joinable = context.Scripts.get.group_joinability(division_id, group_id) == 'anyone' and True or False
leaveable = getattr(getattr(listManager, group_id),'unsubscribe', None) and True or False

if subscribe and not joinable:
    raise 'Forbidden', 'You cannot join this list'
if unsubscribe and not leaveable:
    raise 'Forbidden', 'You cannot unsubscribe from this list'

site = getattr(site_root.Content, division_id)
group = getattr(site.groups, group_id)

# Get the participation-coach for the group
ptnCoachId = group.getProperty('ptn_coach_id', '')
ptnCoach = site_root.acl_users.getUser(ptnCoachId)

# The dictionary of values for the admin notifications.
#  The last two keys are superfluous on OGN, but included
#  for backwards-compatibility (for eDem, effectively).
if ptnCoach:
    n_dict = {
                'groupId'      : group_id,
                'groupName'    : group.title_or_id(),
                'siteName'     : site.title_or_id(),
                'canonical'    : getOption(group, 'canonicalHost'),
                'supportEmail' : site.GlobalConfiguration.getProperty('supportEmail'),
                'memberId'     : user_id,
                'memberName'   : user.getProperty('preferredName'),
                'joining_user' : user,
                'joining_group': group
              }

if int(unsubscribe):
    user.del_groupWithNotification('%s_member' % group_id)
    if ptnCoach:
        ptnCoach.send_notification('leave_group_admin', group_id, n_dict)
    return context.REQUEST.RESPONSE.redirect('%s/groups/' % (getOption(group, 'canonicalHost')))

if joinable:
    user.add_groupWithNotification('%s_member' % group_id)
    if ptnCoach:
        ptnCoach.send_notification('join_group_admin', group_id, n_dict)

    return context.REQUEST.RESPONSE.redirect('%s/groups/%s/' % (getOption(group, 'canonicalHost'), group_id))

return context.REQUEST.RESPONSE.redirect(context.REQUEST.SESSION['last_url'])
