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

mmembers = []
if grouplist.hasProperty('moderated_members'):
   mmembers = filter(None, grouplist.getProperty('moderated_members'))

for member in userids:
    if member in mmembers:
        mmembers.remove(member)

if grouplist.hasProperty('moderated_members'):
    grouplist.manage_changeProperties(moderated_members=mmembers)
else:
    grouplist.manage_addProperty('moderated_members', mmembers, 'lines')

userNames = ', '.join(map(lambda m: group.Scripts.get.user_realnames(m),
                          userids))
result['error'] = False
m = (len(userids) == 1) and ('member %s has' % userNames)\
    or ('%d members (%s) have' % (len(userids), userNames))
result['message'] = '''<paragraph>The %s been <em>removed</em>
  from the moderation list for %s.
  There are now %d moderated members of
  this group.</paragraph>''' % (m, group.title_or_id(), len(mmembers))
return result
