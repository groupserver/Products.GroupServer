## Script (Python) "adduser_create_new_user"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=preferredname=None,email=None,userid=None,siteid=None,groups=None,sendVerification=None,userproperties={}
##title="Add User: Create New User"
##
site_root = context.site_root()

assert not site_root.acl_users.get_userByEmail(email)

result = {}

userproperties['preferredName'] = preferredname

firstname=''
lastname=''

user = context.Scripts.registration.register_user(firstname, lastname, preferredname,
                                                  email, userid, siteid,
                                                  groups, 0,
                                                  userproperties,
                                                  sendVerification)

if not user:
    result['error'] = True
    result['message'] = '''<listitem>An unexpected error occurred
    while creating the user with the email address %s, please report
    this as a bug.</listitem>''' % email
else:
    textGroups = ', '.join(map(lambda g: g[:-7], groups))
    result['error'] = False
    result['message'] = '''<listitem>Created a user with ID
    %s and the email address %s; the user has been added
    to %s.</listitem>''' % (user.getId(), email, textGroups)

return result

