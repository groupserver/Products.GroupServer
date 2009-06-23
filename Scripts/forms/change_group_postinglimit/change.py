## Script (Python) "change_group_postinglimit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.PythonScripts.standard import html_quote

result = {}
form = context.REQUEST.form
assert form.has_key('groupid')
assert form.has_key('siteid')
assert form.has_key('senderlimit')
assert form.has_key('senderinterval')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

message = []
error = False

site_root = context.site_root()
groupid = form.get('groupid')
siteid = form.get('siteid')
group = context.Scripts.get.group_by_id(groupid)

if group.Scripts.get.division_object().getId() != siteid:
    error = True
    message.append('''<li>Unable to change properties:
    there appears to be a group with the same ID in a different site.</li>''')

listManager = site_root.objectValues('XWF Mailing List Manager')[0]
grouplist = getattr(listManager, groupid)

senderlimit = form.get('senderlimit', 0)
try:
    senderlimit = int(senderlimit)
except:
    error = True
    message.append('<li>The posting limit must be an integer</li>')

secInHour = 3600
origSenderinterval = form.get('senderinterval', 0)
try:
    senderinterval = int(origSenderinterval) * secInHour
except:
    error = True
    message.append('<li>The posting interval must be an integer</li>')

if error:
    retval = {'error': error, 'message': "<ul>%s</ul>" % '\n'.join(message)}
    return retval
    
senderLimitChanged = False
senderIntervalChanged = False
if getattr(grouplist, 'senderlimit', 0) != senderlimit:
    if grouplist.hasProperty('senderlimit'):
        grouplist.manage_changeProperties(senderlimit=senderlimit)
    else:
        grouplist.manage_addProperty('senderlimit', senderlimit, 'int')
    message.append('<li>Set sender limit to %d posts.</li>' % senderlimit)
    senderLimitChanged = True

if getattr(grouplist, 'senderinterval', 0) != senderinterval:
    if grouplist.hasProperty('senderinterval'):
        grouplist.manage_changeProperties(senderinterval=senderinterval)
    else:
        grouplist.manage_addProperty('senderinterval', senderinterval, 'int')
    m = '<li>Set sender interval to %s hours.</li>' % origSenderinterval
    message.append(m)
    senderIntervalChanged = True

if senderIntervalChanged or senderLimitChanged:
    sI = context.Scripts.get.list_property(grouplist.getId(), 
                                           'senderinterval')
    sL = context.Scripts.get.list_property(grouplist.getId(),
                                           'senderlimit')
    secInHour = 3600
    duration = sI/ secInHour
    plural = duration > 1
    if plural:
      interval = '%d hours' % duration
    else:
      interval = 'hour'
        
    m = '<li>Posting limit is now %d posts every %s.</li>' % (sL,interval)
    message.append(m)


m = '''<p>Updating group %s</p>
  <ul>%s</ul>''' % (html_quote(group.title_or_id()), '\n'.join(message))
retval = {'error': False, 'message': m}
return retval
