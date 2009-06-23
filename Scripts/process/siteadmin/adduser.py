## Script (Python) "adduser"
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

# groupid is defined we're probably working as a group admin
# otherwise we're probably working as a division or site admin
groupid = form.get('groupid', '')
joingroups = form.get('groups', [])

divisionid = form.get('divisionid')
userid = form.get('userid','')
firstname = form.get('firstname','')
lastname = form.get('lastname','')
email = form.get('email','').lower()
sendVerification = form.get('sendVerification', '')
preferredname = form.get('preferredname', '')

groups = ['%s_member' % divisionid]
try: # check for string/list ness, the hard way
    joingroups.split
    joingroups = [joingroups]
except:
    pass
for group in joingroups:
    groups.append('%s_member' % group)

if form.get('addtogroup', 'no') == 'yes' and groupid:
    groups.append('%s_member' % groupid)

user = site_root.acl_users.get_userByEmail(email)

if user:
    result = container.adduser_add_user(user,groups)
    return '<bulletlist>%s</bulletlist>' % result['message']
else:
    message = context.verifyuserdata(firstname, lastname, userid, email)
    if message:
        return message
    result = container.adduser_create_new_user(firstname, lastname,
                                               preferredname, email,
                                               userid, groups, 
                                               sendVerification)
    return '<bulletlist>%s</bulletlist>' % result['message']
