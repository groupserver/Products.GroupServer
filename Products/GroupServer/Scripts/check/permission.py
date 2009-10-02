## Script (Python) "permission"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=objects, roles
##title=
##
try:
    roles.swapcase # it's a string
    roles = [roles]
except:
    pass

allowed = 0
for object in objects:
    roles_in_context = context.REQUEST.AUTHENTICATED_USER.getRolesInContext(object)
    for role in roles_in_context:
        if role in roles:
            allowed = 1

if not allowed:
    context.REQUEST.RESPONSE.redirect('/login/', lock=1)
    return 0
return 1
