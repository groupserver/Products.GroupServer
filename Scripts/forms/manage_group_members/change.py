## Script (Python) "change"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Change Group Member Details
##

# The job of this script is to fire off the appropriate scripts that
#   add and remove users from different sub-groups, such as the
#   moderated members and group administrators. In many ways it is a
#   marshaling script.

result = {}
result['message'] = ''
result['error'] = False # Uncharastic optimism
form = context.REQUEST.form
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

assert form.has_key('groupid')
groupid = form['groupid']
assert form.has_key('divisionid')
divisionid = form['divisionid']

##############
# Moderators #
##############
# Adding
moderatorsAddUsers = form.has_key('moderators_add_userid') \
                     and form['moderators_add_userid'] \
                     or ''
try:
    moderatorsAddUsers.append
except:
    moderatorsAddUsers = [moderatorsAddUsers]
if moderatorsAddUsers != ['']:
    r = container.moderators.add_users(moderatorsAddUsers,
                                       groupid, divisionid)
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = result['error'] and r['error']
    
# Removing
moderatorsRemoveUsers = form.has_key('moderators_remove_userid')\
                        and form['moderators_remove_userid']\
                      or ''
try:
    moderatorsRemoveUsers.append
except:
    moderatorsRemoveUsers = [moderatorsRemoveUsers]
if moderatorsRemoveUsers != ['']:
    r = container.moderators.remove_users(moderatorsRemoveUsers,
                                          groupid, divisionid)
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = result['error'] and r['error']

##############
# Moderation #
##############
# Adding
moderateAddUsers = form.has_key('moderate_add_userid') \
                   and form['moderate_add_userid'] \
                   or ''
try:
    moderateAddUsers.append
except:
    moderateAddUsers = [moderateAddUsers]
if moderateAddUsers != ['']:
    r = container.moderate.add_users(moderateAddUsers,
                                     groupid, divisionid)
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = result['error'] and r['error']

# Removing
moderateRemoveUsers = form.has_key('moderate_remove_userid')\
                      and form['moderate_remove_userid']\
                      or ''
try:
    moderateRemoveUsers.append
except:
    moderateRemoveUsers = [moderateRemoveUsers]
if moderateRemoveUsers != ['']:
    r = container.moderate.remove_users(moderateRemoveUsers,
                                        groupid, divisionid)
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = result['error'] and r['error']

#######################
# Participation Coach #
#######################
# Adding
ptn_coach_add_userid = form.has_key('ptn_coach_add_userid') \
                       and form['ptn_coach_add_userid'] \
                       or ''
if ptn_coach_add_userid != '':
    r = container.ptn_coach.add_user(ptn_coach_add_userid,
                                     groupid, divisionid)
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = result['error'] and r['error']

# Removing
ptn_coach_remove_userid = form.has_key('ptn_coach_remove_userid') \
                       and form['ptn_coach_remove_userid'] \
                       or ''
if ptn_coach_remove_userid != '' and ptn_coach_add_userid == '':
    r = container.ptn_coach.remove_user(ptn_coach_remove_userid,
                                        groupid, divisionid)
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = result['error'] and r['error']

########################
# Group Administration #
########################
# Adding
group_admin_add_userid = form.has_key('group_admin_add_userid') \
                         and form['group_admin_add_userid'] \
                         or ''
try:
    group_admin_add_userid.append
except:
    group_admin_add_userid = [group_admin_add_userid]
if group_admin_add_userid != ['']:
    r = container.admin.add_users(group_admin_add_userid,
                                  groupid, divisionid)
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = result['error'] and r['error']

# Removing
group_admin_remove_userid = form.has_key('group_admin_remove_userid') \
                         and form['group_admin_remove_userid'] \
                         or ''
try:
    group_admin_remove_userid.append
except:
    group_admin_remove_userid = [group_admin_remove_userid]
if group_admin_remove_userid != ['']:
    r = container.admin.remove_users(group_admin_remove_userid,
                                     groupid, divisionid)
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = result['error'] and r['error']
    
####################
# Group Membership #
####################
group_remove_userid = form.has_key('group_remove_userid') \
                      and form['group_remove_userid'] \
                      or ''
try:
    group_remove_userid.append
except:
    group_remove_userid = [group_remove_userid]
if group_remove_userid != ['']:
    r = container.remove_users(group_remove_userid,
                               groupid, divisionid)
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = result['error'] and r['error']

return result
