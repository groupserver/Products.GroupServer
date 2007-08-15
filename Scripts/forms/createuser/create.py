## Script (Python) "create"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Create a New Group Memeber
##
form = context.REQUEST.form
site_root = context.site_root()
result = {}
result['form'] = form

assert form.has_key('groupid')
assert form.has_key('divisionid')

for field in form.keys():
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

groupid = form['groupid']
divisionid = form['divisionid']
joingroups = form.get('groups', [])
userid = form.get('userid','')
firstname = form.get('firstname','')
lastname = form.get('lastname','')
email = form.get('email','').lower()
sendVerification = form.get('sendVerification', '')
preferredname = form.get('preferredname', '')

groups = ['%s_member' % divisionid]
try: # check for string/list ness, the hard way
    joingroups.split
    joingroups = [joingroups]
except:
    pass
for group in joingroups:
    groups.append('%s_member' % group)

if form.get('addtogroup', 'no') == 'yes' and groupid:
    groups.append('%s_member' % groupid)

user = site_root.acl_users.get_userByEmail(email)

if user:
    retval = container.process.siteadmin.adduser_add_user(user,groups)
    result['message'] = '<ul>%s</ul>' % retval['message']
    result['error'] = retval['error']
else:
    message = context.process.siteadmin.verifyuserdata(firstname, lastname, userid, email)
    if message:
        result['message'] = '<p>%s</p>' % message
        result['error'] = True
    else:
        retval = container.process.siteadmin.adduser_create_new_user(firstname, lastname,
                                                   preferredname, email,
                                                   userid, groups, 
                                                   sendVerification)
        result['message'] = '<ul>%s</ul>' % retval['message']
        result['error'] = retval['error']
                                               
return result
