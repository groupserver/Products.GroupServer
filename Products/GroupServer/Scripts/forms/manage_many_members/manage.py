## Script (Python) "change"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Manage Many Group Members
##

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

mIds = form['member_ids']
url = '/groups/%s/managemembers.html?showOnly=%s' % \
  (groupid, same_type(mIds, []) and ' '.join(mIds) or mIds)
context.REQUEST.RESPONSE.redirect(url)
 
