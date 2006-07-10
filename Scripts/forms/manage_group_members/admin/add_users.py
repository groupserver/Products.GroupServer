## Script (Python) "add_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userids=[],groupid=None,divisionid=None
##title=Add Users to Group Administration List
##
from Products.PythonScripts.standard import html_quote

result = {}
assert groupid != None
assert divisionid != None
assert userids.append # The userids is a list

site_root = context.site_root()
group = context.Scripts.get.group_by_id(groupid)
assert(group != None)

groupUserIds = map(lambda u: u.getId(), group.Scripts.get.group_members())

names = []
for userid in userids:
    userName = group.Scripts.get.user_realnames(userid,
                                                preferred_name_only=True)
    names.append(userName)

    group.manage_addLocalRoles(userid, ['GroupAdmin'])

userNames = ', '.join(names)
result['error'] = False
m = (len(userids) == 1) and ('member you selected (%s) has' % userNames) \
    or ('%d members you selected (%s) have' % (len(userids), userNames))
result['message'] = '''<paragraph>The %s been given
  group-administrator status.</paragraph>''' % m
return result

