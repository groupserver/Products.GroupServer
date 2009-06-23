## Script (Python) "group_moderators"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=ids_only=False
##title=Get Moderators for Group
##

def sorter(a,b):
    if a.getProperty('lastName') > b.getProperty('lastName'):
        return 1
    else:
        return -1

site_object = context.site_root()
group_object = context.Scripts.get.group_object()
assert group_object != None
group_id = group_object.getId()


mailingList = getattr(site_object.ListManager, group_object.getId(), None)
assert mailingList != None
moderatorEmailAddresses = list(mailingList.getProperty('moderator', []))

moderators = []
for address in moderatorEmailAddresses:
    obj = site_object.acl_users.get_userByEmail(address)
    if obj:
        moderators.append(obj)

moderators.sort(sorter)

if ids_only:
    return map(lambda m: m.getId(), moderators)
else:
    return moderators
