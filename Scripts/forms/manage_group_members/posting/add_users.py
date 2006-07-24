## Script (Python) "add_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userids=[],groupid=None,divisionid=None
##title=Add Users to the List of Members that can Post
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

userNames = ', '.join(map(lambda m: group.Scripts.get.user_realnames(m),
                          userids[:-1]))
if (len(userids) > 1):
   userNames = '%s and %s' % (userNames,
                              group.Scripts.get.user_realnames(userids[-1]))
else:
   userNames = group.Scripts.get.user_realnames(userids[-1])
postingMembers = []
if grouplist.hasProperty('posting_members'):
   postingMembers = filter(None, grouplist.getProperty('posting_members'))

l = len(postingMembers)
if ((l >= 5) or (l+len(userids) > 5)):
   haveOrHas = ((len(userids) > 1) and 'have') or 'has'
   result['error'] = True
   result['message'] = '''%s %s not been added to the list of posting
     members, as it would put the number of posting members beyond the
     maximum (five).''' % (userNames, haveOrHas)
   return result
   
   
for member in userids:
    if member not in postingMembers:
        postingMembers.append(member)            

if grouplist.hasProperty('posting_members'):
    grouplist.manage_changeProperties(posting_members=postingMembers)
else:
    grouplist.manage_addProperty('posting_members', postingMembers, 'lines')

result['error'] = False
m = (len(userids) == 1) and ('member you selected (%s) has' % userNames) \
    or ('%d members you selected (%s) have' % (len(userids), userNames))
isOrAre = (len(postingMembers) == 1 and 'is') or 'are'
sOrNul = (len(postingMembers) == 1 and '') or 's'
result['message'] = '''<paragraph>The %s been <em>added</em>
  to the list of posting members for %s.
  There %s now %d posting member%s of
  this group.</paragraph>''' % (m, group.title_or_id(), isOrAre,
                                len(postingMembers), sOrNul)
return result
