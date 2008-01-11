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
    message.append("""<li>The user ID %s is already taken</li>""" % userid)

if not preferredname:
    error = 1
    message.append("""<li>The user's name was not specified</li>""")

if not email:
    error = 1
    message.append("""<li>The user's email address was not specified</li>""")
else:
    ue = site_root.acl_users.get_userByEmail(email)
    if ue:
        error = 1
        message.append("""<li>A user is already registered with that email address</li>""")
    
if hasattr(site_root.UserProperties, 'givenName'):
    isRequired = getattr(site_root.UserProperties.givenName, 'required').getProperty('required', 0)
    if isRequired and not given_name:
        error = 1
        message.append("""<li>The user's first name was not specified</li>""")

if hasattr(site_root.UserProperties, 'familyName'):
    isRequired = getattr(site_root.UserProperties.familyName, 'required').getProperty('required', 0)
    if isRequired and not family_name:
        error = 1
        message.append("""<li>The user's last name was not specified</li>""")
    
return message
