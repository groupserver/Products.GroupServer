## Script (Python) "forgottenpassword"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=username='', email=''
##title=
##
site_root = context.site_root()
username = username.strip(); email = email.strip()

user = None
if username:
    user = site_root.acl_users.getUser(username)
elif email:
    user = site_root.acl_users.get_userByEmail(email.lower())

# one last possibility exists, that the username is actually an email address
if not user and username.find('@') > 0:
    user = site_root.acl_users.get_userByEmail(username.lower())

if user:
    # Reset the password and send the user a new one.
    user.reset_password()
    n_dict = {'server', context.REQUEST.SERVER_URL}
    user.send_notification('forgotten_password', 'default', n_dict)
    
    return context.REQUEST.RESPONSE.redirect('/sent_password.xml')

else:
    return context.REQUEST.RESPONSE.redirect('/login/forgotten_password.xml?error=1')
