## Script (Python) "password"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id
##title=
##
user = context.acl_users.getUser(user_id)

if user:
   return user.get_password()

return 'No such user'
