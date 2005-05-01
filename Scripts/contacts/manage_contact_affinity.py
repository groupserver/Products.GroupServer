## Script (Python) "manage_contact_affinity"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=user
##title=
##
me = context.REQUEST.AUTHENTICATED_USER

site_root = context.site_root()

try:
    user.getUserName()
except:
    user = None

if (not me.getId()) or (not user) or (not user.getId()):
    return

if not me.hasProperty('contact_affinities'):
    me.manage_addProperty('contact_affinities', [user.getUserName()], 'lines')
else:
    ca = list(me.getProperty('contact_affinities'))
    try:
        ca.remove(user.getUserName())
    except:
        pass
    ca.insert(0, user.getUserName())
    if len(ca) > 7:
        ca = ca[:7]
    me.manage_changeProperties(contact_affinities=ca)

return
