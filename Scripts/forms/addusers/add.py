## Script (Python) "add"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Add an Existing Site Member to the Group
##
form = context.REQUEST.form
result = {}
site_root = context.site_root()
assert form.has_key('groupid')

userids = form.get('userid', [])
groupid = form.get('groupid')

if not userids:
    m = '<p>You must specify at least one user to add to the group.</p>'
    result['message'] = m
    result['error'] = True
else:
    if (len(userids[0]) == 1):
        # --=rrw=-- Yes, this is a hack assuming that we will never
        #  have very short userids
        userids = [userids]
    group_memebersip_id = '%s_member' % groupid
    names = []
    for userid in userids:
        user = site_root.acl_users.getUser(userid)
        user.add_groupWithNotification(*[group_memebersip_id])
        names.append('%s %s' % (getattr(user, 'firstName', ''),
                                getattr(user, 'lastName', '')))
    if (len(userids) > 1):
        namesStr = ' and '.join(', '.join(names[:-1]), names[-1])
        result['message'] = """<p>Added %d existing site-members (%s) to 
        the group.</p>""" % (len(userids), namesStr)
    else:
        result['message'] = """<p>Added the existing site-member, %s, to 
        the group.</p>""" % names[0]
    result['error'] = False
    
return result
