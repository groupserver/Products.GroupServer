## Script (Python) "dowire_start"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=DoWire.Org Start a Group Start
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
groupId = form['groupId']
groupId = groupId.lower()
realLifeGroup = form['realLifeGroup']
privacy = form['privacy']

# The user should not be able to stuff up the division ID as it is set
#   by code.

# The user should not be able to stuff up the group type, as it is set
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

# No error, start the group
# DoWire uses the standard template for all group types
if groupType == 'announcement':
    group = container.edem_add_announcement_group(siteId, 'standard', groupId, groupName,
                                                 realLifeGroup, privacy)
else:
    group = container.edem_add_discussion_group(siteId, groupType, groupId, groupName,
                                                 realLifeGroup, privacy)

if group != None:
    groupPage = '/groups/%s' % groupId
    context.REQUEST.RESPONSE.redirect(groupPage)
else:
    result['message'] = '''The group %s could not be started due to an 
      unexpected error'''
    result['error'] = True
    return result
