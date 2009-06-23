## Script (Python) "send"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Send the User a Verification Reminder
##
from Products.PythonScripts.standard import html_quote
import DateTime

result = {}

form = context.REQUEST.form
assert form.has_key('siteid')
assert form.has_key('groupid')
assert form.has_key('userid')
assert form.has_key('adminid')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

siteId = form['siteid']
groupId = form['groupid']
userId = form['userid']
adminId = form['adminid']

retval = container.send_verification_reminder(siteId, groupId, 
                                              userId, adminId)
if retval[0]:
    result['error'] = False
    result['message'] = '''The verification reminder has been sent.'''
else:
    result['error'] = True
    result['message'] = '''The verification reminder has not been sent, as
    %s.''' % retval[1]
    
return result

