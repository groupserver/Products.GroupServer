## Script (Python) "remove_user"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userid=None,groupid=None,divisionid=None
##title=Remove User from Participation Coach List
##
from Products.PythonScripts.standard import html_quote

# --=mpj17=-- This script does not actually remove the user from the
# the participation-coach list: it sets the participation coach field to
# an empty string.

result = {}
assert groupid != None
assert divisionid != None
assert userid != None

site_root = context.site_root()
group = context.Scripts.get.group_by_id(groupid)
assert(group != None), "Group %s not found" % groupid

listManager = site_root.objectValues('XWF Mailing List Manager')[0]
assert (listManager != None), "List manager not found"
groupList = listManager.get_list(groupid)
assert groupList != None, "Email list %s not found" % groupid

userName = group.Scripts.get.user_realnames(userid,
                                            preferred_name_only=True)

# Set the participation coach.
if group.hasProperty('ptn_coach_id'):
    group.manage_changeProperties(ptn_coach_id='')
if groupList.hasProperty('ptn_coach_id'):
    groupList.manage_changeProperties(ptn_coach_id='')

result['error'] = False
result['message'] = '''<paragraph>%s has been removed as the
  participation coach for %s; there is no longer any participation coach
  for %s.</paragraph>''' % (userName, group.title_or_id(),
                            group.title_or_id())
return result
