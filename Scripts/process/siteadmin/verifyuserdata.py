## Script (Python) "verifyuserdata"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=preferredname=None, userid=None, email=None, given_name=None, family_name=None
##title=
##
site_root = context.site_root()
message = []

if userid and site_root.acl_users.getUser(userid):
    error = 1
    message.append("""<p>The user ID %s is already taken</p>""" % userid)

if not preferredname:
    error = 1
    message.append("""<p>The user's name was not specified</p>""")

if not email:
    error = 1
    message.append("""<p>The user's email address was not specified</p>""")
else:
    ue = site_root.acl_users.get_userByEmail(email)
    if ue:
        error = 1
        message.append("""<p>A user is already registered with that email address</p>""")
    
if getattr(site_root.UserProperties.givenName, 'required', 0) and not given_name:
    error = 1
    message.append("""<p>The user's first name was not specified</p>""")

if getattr(site_root.UserProperties.familyName, 'required', 0) and not family_name:
    error = 1
    message.append("""<p>The user's last name was not specified</p>""")
    
return message
