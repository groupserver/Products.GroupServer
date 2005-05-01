## Script (Python) "verifyuserdata"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=firstname=None, lastname=None, userid=None, email=None
##title=
##
site_root = context.site_root()
message = []
if userid and site_root.acl_users.getUser(userid):
    error = 1
    message.append('<paragraph>The user ID %s is already taken</paragraph>' % userid)

if not firstname:
    error = 1
    message.append("<paragraph>The user's first name was not specified</paragraph>")

if not lastname:
    error = 1
    message.append("<paragraph>The user's last name was not specified</paragraph>")

if not email:
    error = 1
    message.append("<paragraph>The user's email address was not specified</paragraph>")

ue = site_root.acl_users.get_userByEmail(email)
if ue:
    error = 1
    message.append("<paragraph>A user (%s) was already registered with that email address</paragraph>" % ue.getId())

return message
