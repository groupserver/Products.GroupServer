## Script (Python) "remove_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userids=[],groupid=None,divisionid=None
##title=Remove Users from the list of Posting Members
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

postingMembers = []
if grouplist.hasProperty('posting_members'):
   postingMembers = filter(None, grouplist.getProperty('posting_members'))

for member in userids:
    if member in postingMembers:
        postingMembers.remove(member)

if grouplist.hasProperty('posting_members'):
    grouplist.manage_changeProperties(posting_members=postingMembers)
else:
    grouplist.manage_addProperty('posting_members', postingMembers, 'lines')

userNames = ', '.join(map(lambda m: group.Scripts.get.user_realnames(m),
                          userids))
result['error'] = False
m = (len(userids) == 1) and ('member %s has' % userNames)\
    or ('%d members (%s) have' % (len(userids), userNames))
isOrAre = (len(postingMembers) == 1 and 'is') or 'are'
sOrNul = (len(postingMembers) == 1 and '') or 's'
result['message'] = '''<paragraph>The %s been <em>removed</em>
  from the list of posting members for %s.
  There %s now %d posting member%s of
  this group.</paragraph>''' % (m, group.title_or_id(), isOrAre,
                                len(postingMembers), sOrNul)
return result
