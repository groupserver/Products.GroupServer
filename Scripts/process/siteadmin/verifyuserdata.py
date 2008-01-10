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
message = """<bulletlist>"""
if userid and site_root.acl_users.getUser(userid):
    error = 1
    message = message + '<listitem>The user ID %s is already taken</listitem>' % userid

if not preferredname:
    error = 1
    message = message + "<listitem>The user's name was not specified</listitem>"

if not email:
    error = 1
    message = message + "<listitem>The user's email address was not specified</listitem>"

ue = site_root.acl_users.get_userByEmail(email)
if ue:
    error = 1
    message = message + "<listitem>A user is already registered with that email address</listitem>"
    
if hasattr(site_root.UserProperties, 'givenName') and not given_name:
    error = 1
    message = message + "<listitem>The user's first name was not specified</listitem>"

if hasattr(site_root.UserProperties, 'familyName') and not family_name:
    error = 1
    message = message + "<listitem>The user's last name was not specified</listitem>"

message = message + """</bulletlist>"""

if message == """<bulletlist></bulletlist>""":
    message = None

return message
