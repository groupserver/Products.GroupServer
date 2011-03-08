## Script (Python) "next"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Start a Group Next
##
result = {}
result['error'] = False # --=mpj17=-- uncharastic optimisism
result['message'] = ''

form = context.REQUEST.form
assert form.has_key('siteId'), 'No site ID'
assert form.has_key('groupType'), 'No group type'
assert form.has_key('groupName'), 'No group name'
assert form.has_key('groupId'), 'No group id'
assert form.has_key('realLifeGroup'), 'No real-life-group'
assert form.has_key('privacy'), 'No privacy'
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

siteId = form['siteId']
groupType = form['groupType']
groupName = form['groupName']
groupId = form['groupId'].lower()
realLifeGroup = form['realLifeGroup']
privacy = form['privacy']

# The user should not be able to stuff up the division ID as it is set
#   by code.

# The user should not be able to stuff up the group-type, as it is set
#   with a radio-button.

# Check for errors in the group name
r = container.check_name(groupName)
if r['error']:
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = True

# Check for errors in the group id
r = container.check_id(groupId)
if r['error']:
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = True

# Check for errors in the real life group
r = container.check_realLifeGroup(realLifeGroup)
if r['error']:
    result['message'] = '%s%s' % (result['message'], r['message'])
    result['error'] = True

# The user should not be able to stuff up the privacy, as it is set
#   with a radio-button.

if result['error']:
    return result

# No error, redirect
gt = 'groupType=%s' % groupType
gn = 'groupName=%s' % groupName.replace(' ', '%20')
gi = 'groupId=%s' % groupId
rlg = 'realLifeGroup=%s' % realLifeGroup.replace(' ', '%20')
p = 'privacy=%s' % privacy
e = [gt,gn, gi, rlg, p]
redir ='admindivision/start_a_group/start_a_group_preview?%s' % '&'.join(e)

context.REQUEST.RESPONSE.redirect(redir)
 