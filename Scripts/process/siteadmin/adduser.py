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
email = form.get('email','')
sendVerification = form.get('sendVerification', '')

message = context.verifyuserdata(firstname, lastname, userid, email)
if message:
    error = 1
else:
    error = 0

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

if error:
    return '\n'.join(message)

if preferredname:
    userproperties = {'preferredName': preferredname}
else:
    userproperties = {}

user = context.Scripts.registration.register_user(firstname, lastname, email, userid, groups, 0, userproperties, sendVerification)

if not user:
    message.append("<paragraph>An unexpected error occured while creating the user, please report this as a bug.</paragraph>")
else:
    message.append("<paragraph>Created user with ID %s</paragraph>" % user.getId())

return '\n'.join(message)
