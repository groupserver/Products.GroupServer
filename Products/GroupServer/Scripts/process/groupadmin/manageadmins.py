## Script (Python) "manageadmins"
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

userids = form.get('userid', [])
groupid = form.get('groupid')
group = context.Scripts.get.group_by_id(groupid)

if not userids:
    return '<paragraph>You must specify at least one user</paragraph>'
# yes, this is a hack assuming that we will never have very short userids
elif len(userids[0]) == 1:
    userids = [userids]
    
model, method = submit.split('+')
for userid in userids:
    if model == 'addadmins':
        group.manage_addLocalRoles(userid, ['GroupAdmin'])
    elif model == 'removeadmins':
        roles = list(group.get_local_roles_for_userid(userid))
        try:
            roles.remove('GroupAdmin')
        except:
            pass
        if roles:
            group.manage_setLocalRoles([userid], roles)
        else:
            group.manage_delLocalRoles([userid])
        
if model == 'addadmins':
    return '<paragraph>New users given admin status</paragraph>'
elif model == 'removeadmins':
    return '<paragraph>Admin status successfully removed from %s user/s</paragraph>' % len(userids)
