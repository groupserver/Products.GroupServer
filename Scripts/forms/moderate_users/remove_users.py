## Script (Python) "remove_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Remove Users from Group Moderation
##
from Products.PythonScripts.standard import html_quote

result = {}
form = context.REQUEST.form
assert form.has_key('groupid')
assert form.has_key('divisionid')
# -=mpj17=-- "userids" is checked below
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

site_root = context.site_root()
groupid = form.get('groupid')
divisionid = form.get('divisionid')
group = context.Scripts.get.group_by_id(groupid)
assert(group != None)

userids = form.get('userid', [])
if not userids:
    result['error'] = True
    result['message'] = '''<paragraph>You must specify at least one
    user to remove from moderation.</paragraph>'''
    return result
# --=rrw=-- yes, this is a hack assuming that we will never have very
#   short userids
elif len(userids[0]) == 1:
    userids = [userids]

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

result['error'] = False
m = (len(userids) == 1) and 'member' or 'members'
result['message'] = '''<paragraph>The %d %s have been <em>removed</em>
  from the moderation list for %s</paragraph>''' % (len(userids), m,
                                                    group.title_or_id())
return result
