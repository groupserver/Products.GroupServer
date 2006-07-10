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

result = {}
assert groupid != None
assert divisionid != None
assert userid != None

site_root = context.site_root()
group = context.Scripts.get.group_by_id(groupid)
assert(group != None)

site_root = context.site_root()
group = context.Scripts.get.group_by_id(groupid)
assert(group != None)

userName = group.Scripts.get.user_realnames(userid,
                                            preferred_name_only=True)

# Set the participation coach.
group.manage_changeProperties(ptn_coach_id='')

result['error'] = False
result['message'] = '''<paragraph>%s has been removed as the
  participation coach for %s; there is no longer any participation coach
  for %s.</paragraph>''' % (userName, group.title_or_id(),
                            group.title_or_id())
return result
