## Script (Python) "permissions"
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

try:
    objects.swapcase # it's a string
    objects = [objects]
except:
    pass

allowed = 0
nroles = [map(lambda x: x.getId(), objects)]
for object in objects:
    roles_in_context = context.REQUEST.AUTHENTICATED_USER.getRolesInContext(object)
    nroles.append((roles_in_context))
    for role in roles_in_context:
        if role in roles:
            allowed = 1

if not allowed:
    return 'not allowed', nroles
return 'allowed'
