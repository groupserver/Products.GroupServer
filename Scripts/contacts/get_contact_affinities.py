## Script (Python) "get_contact_affinities"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id_only=0
##title=
##
me = context.REQUEST.AUTHENTICATED_USER
site_root=context.site_root()

def mycmp(x, y):
    return cmp(x.firstName, y.firstName)

user_ids = me.getProperty('contact_affinities', [])
user_ids = filter(None, user_ids)

uid = me.getId()

# even if we just want the IDs, we still need to validate the users exist
results = map(lambda x: site_root.acl_users.getUser(x), user_ids)
r = []
for result in results:
    try:
        rid = result.getId()
    except:
        rid = None

    if rid != None and rid != uid:
        r.append(result)

if id_only:
    r = map(lambda x: x.getId(), r)
    r.sort()
else:
    r.sort(mycmp)

return r
