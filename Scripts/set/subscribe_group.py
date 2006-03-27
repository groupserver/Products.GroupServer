## Script (Python) "subscribe_group"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=division_id, group_id, unsubscribe=0
##title=
##
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
    raise 'Forbidden', 'You cannot unsubscribe from thist list'

division = getattr(site_root.Content, division_id)
group = getattr(division.groups, group_id)

# Get the participation-coach for the group
ptnCoachId = group.getProperty('ptn_coach_id', '')
ptnCoach = site_root.acl_users.getUser(ptnCoachId)

if int(unsubscribe):
    user.del_groupWithNotification('%s_member' % group_id)
    ptnCoach.send_notification('leave_group_admin', group_id, n_dict={'joining_user': user, 'joining_group': group})
    return context.REQUEST.RESPONSE.redirect('/%s/groups/' % (division_id))

if joinable:
    try:
        user.add_groupWithNotification('%s_member' % group_id)
        ptnCoach.send_notification('join_group_admin', group_id, n_dict={'joining_user': user, 'joining_group': group})
    except:
        pass
    return context.REQUEST.RESPONSE.redirect('/%s/groups/%s/' % (division_id, group_id))

return context.REQUEST.RESPONSE.redirect(context.REQUEST.SESSION['last_url'])
