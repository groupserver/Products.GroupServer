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
    username=email

# one last possibility exists, that the username is actually an email address
providedEmailAddress = False
if not user and username.find('@') > 0:
    providedEmailAddress = True
    user = site_root.acl_users.get_userByEmail(username.lower())

if user:
    # Reset the password and send the user a new one.
    password = user.reset_password()
    n_dict = {'server': context.REQUEST.SERVER_URL,
              'password': password}
    addresses = user.get_emailAddresses()
    user.send_notification('forgotten_password', 'default', n_dict, 
      addresses)
        
url = '/sentpassword.html?user_or_address=%s&providedInfo=%s' % \
      (providedEmailAddress and 'email%20address' or 'user%20name',
       username)
return context.REQUEST.RESPONSE.redirect(url)
