## Script (Python) "remove_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userids=[],groupid=None,divisionid=None
##title=Remove Users from the Group Administration List
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

    roles = list(group.get_local_roles_for_userid(userid))
    try:
        roles.remove('GroupAdmin')
    except:
        pass
    if roles:
        group.manage_setLocalRoles(userid, roles)
    else:
        group.manage_delLocalRoles([userid])

userNames = ', '.join(names)
result['error'] = False
m = (len(userids) == 1) and ('member you selected (%s) has' % userNames) \
    or ('%d members you selected (%s) have' % (len(userids), userNames))
result['message'] = '''<paragraph>The %s had
  group-administrator status revoked.</paragraph>''' % m
return result
