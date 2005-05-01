## Script (Python) "blockusers"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
form = context.REQUEST.form
site_root = context.site_root()

submit = form.get('__submit__', '')
if not submit:
    return ''

userids = form.get('blockeduserids', [])
if not userids:
    return '<paragraph>You must specify at least one user</paragraph>'
# yes, this is a hack assuming that we will never have very short userids
elif len(userids[0]) == 1:
    userids = [userids]

groupid = form.get('groupid')
group = context.Scripts.get.group_by_id(groupid)
listManager = site_root.objectValues('XWF Mailing List Manager')[0]
grouplist = getattr(listManager, groupid)

message = []

model, method = submit.split('+')
if model == 'addblockedusers':
    if grouplist.hasProperty('blocked_members'):
        grouplist.manage_changeProperties(blocked_members=userids)
    else:
        grouplist.manage_addProperty('blocked_members',userids,'lines')
    message.append('<paragraph>Added user/s to blocked users</paragraph>')
elif model == 'removeblockedusers':
    if grouplist.hasProperty('blocked_members'):
        blocked_members = list(grouplist.getProperty('blocked_members'))
        obml = len(blocked_members)
        for userid in userids:
            if userid in blocked_members:
                blocked_members.remove(userid)
        if len(blocked_members) != obml:
            grouplist.manage_changeProperties(blocked_members=blocked_members)
            message.append('<paragraph>Removed user/s from blocked list</paragraph>')

return '\n'.join(message)
