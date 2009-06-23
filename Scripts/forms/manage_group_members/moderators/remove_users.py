## Script (Python) "remove_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userids=[],groupid=None,divisionid=None
##title=Remove Users from Group Moderation
##
from Products.PythonScripts.standard import html_quote

assert groupid != None
assert divisionid != None
assert userids.append

result = {}
site_root = context.site_root()
group = context.Scripts.get.group_by_id(groupid)
assert(group != None)

listManager = site_root.objectValues('XWF Mailing List Manager')[0]
grouplist = getattr(listManager, groupid)
assert(grouplist != None)

mmembers = list(grouplist.getProperty('moderator_members', []))

for member in userids:
   if member in mmembers:
      mmembers.remove(member)
      
if grouplist.hasProperty('moderator_members'):
    grouplist.manage_changeProperties(moderator_members=mmembers)
else:
    grouplist.manage_addProperty('moderator_members', mmembers, 'lines')

userNames = ', '.join(map(lambda m: group.Scripts.get.user_realnames(m),
                          userids))
result['error'] = False
m = (len(userids) == 1) and ('member %s has' % userNames)\
    or ('%d members (%s) have' % (len(userids), userNames))
isOrAre = ((len(mmembers) == 1) and 'is') or 'are'
sOrNul =  ((len(mmembers) != 1) and 's') or ''
result['message'] = '''<paragraph>The %s had the moderation status
   for %s <em>revoked</em>.
  There %s now %d moderator%s for
  this group.</paragraph>''' % (m, group.title_or_id(), isOrAre,
                                len(mmembers), sOrNul)
return result
