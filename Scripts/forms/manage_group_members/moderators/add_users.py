## Script (Python) "add_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userids=[],groupid=None,divisionid=None
##title=Add Users to the List of Moderators
##
from Products.PythonScripts.standard import html_quote

result = {}
assert groupid != None
assert divisionid != None
assert userids.append # The userids is a list

site_root = context.site_root()
group = context.Scripts.get.group_by_id(groupid)
assert(group != None)

listManager = site_root.objectValues('XWF Mailing List Manager')[0]
grouplist = getattr(listManager, groupid)
assert(grouplist != None)

mmemberIds = list(grouplist.getProperty('moderator_members', []))

for userId in userids:
   userObj = site_root.acl_users.getUser(userId)
   userEmail = userObj.get_defaultDeliveryEmailAddresses()
   if ((userId not in mmemberIds) and userEmail):
      mmemberIds.append(userObj)

if grouplist.hasProperty('moderator_members'):
    grouplist.manage_changeProperties(moderator_members=mmemberIds)
else:
    grouplist.manage_addProperty('moderator_members', mmemberIds, 'lines')

userNames = ', '.join(map(lambda m: group.Scripts.get.user_realnames(m),
                          userids))
result['error'] = False
m = (len(userids) == 1) and ('member you selected (%s)' % userNames) \
    or ('%d members you selected (%s)' % (len(userids), userNames))
isOrAre = ((len(mmemberIds) == 1) and 'is') or 'are'
sOrNul =  ((len(mmemberIds) != 1) and 's') or ''
result['message'] = '''<paragraph>The %s can now <em>moderate</em> messages
  for %s.
  There %s now %d moderator%s for
  this group.</paragraph>''' % (m, group.title_or_id(), isOrAre, len(mmemberIds),
                                sOrNul)

return result
