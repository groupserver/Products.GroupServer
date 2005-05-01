## Script (Python) "get_user"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user_id
##title=
##
try:
    return context.acl_users.getUser(user_id)
except:
    return None
