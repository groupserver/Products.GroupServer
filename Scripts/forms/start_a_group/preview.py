## Script (Python) "preview"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Start a Group Preview
##

result = {}
result['error'] = False # --=mpj17=-- uncharastic optimisism
result['message'] = ''

form = context.REQUEST.form
assert form.has_key('siteId')
assert form.has_key('groupType')
assert form.has_key('groupName')
assert form.has_key('groupId')
assert form.has_key('realLifeGroup')
assert form.has_key('privacy')
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
# No error, redirect
gt = 'groupType=%s' % groupType
gn = 'groupName=%s' % groupName.replace(' ', '%20')
gi = 'groupId=%s' % groupId
rlg = 'realLifeGroup=%s' % realLifeGroup.replace(' ', '%20')
p = 'privacy=%s' % privacy
e = [gt,gn, gi, rlg, p]
redir ='start_a_group_preview.xml?%s' % '&'.join(e)

context.REQUEST.RESPONSE.redirect(redir)
 
