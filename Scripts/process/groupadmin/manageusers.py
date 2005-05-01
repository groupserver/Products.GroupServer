## Script (Python) "manageusers"
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

if not userids:
    return '<paragraph>You must specify at least one user</paragraph>'
# yes, this is a hack assuming that we will never have very short userids
elif len(userids[0]) == 1:
    userids = [userids]

model, method = submit.split('+')
if model == 'addusers':
    groupMethod = 'add_groupWithNotification'
elif model == 'removeusers':
    groupMethod = 'del_groupWithNotification'

for userid in userids:
    user = site_root.acl_users.getUser(userid)
    getattr(user, groupMethod)(*['%s_member' % groupid])

if model == 'addusers':
    return '<paragraph>New users successfully added</paragraph>'
elif model == 'removeusers':
    return '<paragraph>Users successfully removed</paragraph>'
