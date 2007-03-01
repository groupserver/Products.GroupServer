## Script (Python) "manageproperties"
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
assert form.has_key('grouptitle')
assert form.has_key('groupSubject')
assert form.has_key('permvisibility')
assert form.has_key('permjoin')
assert form.has_key('permviewfiles')
assert form.has_key('permviewmessages')
assert form.has_key('coach')
assert form.has_key('senderlimit')
assert form.has_key('senderinterval')
assert form.has_key('siteid')
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
    message.append('''<li>There appears to be a group in a different division
    with the same ID, unable to change properties.</li>''')

listManager = site_root.objectValues('XWF Mailing List Manager')[0]
grouplist = getattr(listManager, groupid)

# Change the title of  the list manager object for the group.
groupSubject = form.get('groupSubject')
grouplist.manage_changeProperties(title=groupSubject)

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

group_title = form.get('grouptitle', None)
if group_title:
    if group.getProperty('title') != group_title:
        group.manage_changeProperties(title=group_title)
        message.append('<li>Updated group title.</li>')

coach_id = form.get('coach', None)
if coach_id:
    if group.getProperty('ptn_coach_id') != coach_id:
        group.manage_changeProperties(ptn_coach_id=coach_id)
        message.append('<li>Updated participation coach.</li>')

for property in site_root.GroupProperties.objectValues():
    prop = form.get(property.getId(), None)
    if property.getProperty('property_type') in ('lines', 'ulines'):
        prop = tuple(map(lambda x: x.strip(), prop.split('\n')))
    elif (prop != None):
        prop = prop.strip()
    
    if prop != None and group.getProperty(property.getId()) != prop:
        if hasattr(group, property.getId()):
            group.manage_changeProperties({property.getId(): prop})
        else:
            group.manage_addProperty(property.getId(), prop, property.getProperty('property_type'))
        message.append('<li>Set %s to <q>%s</q>.</li>' % (html_quote(property.title_or_id()), html_quote(prop)))

visibility = context.Scripts.get.group_visibility()
permvisibility = form.get('permvisibility', 'group')
if visibility != permvisibility:
    if permvisibility == 'anyone':
        group.manage_permission('View', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.manage_permission('Access contents information', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated group permissions to make the group visible to anyone</li>')
    elif permvisibility == 'division':
        group.manage_permission('View', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.manage_permission('Access contents information', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated group permissions to make the group visible to only division members</li>')    
    elif permvisibility == 'group':
        group.manage_permission('View', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.manage_permission('Access contents information', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated group permissions to make the group visible to only group members</li>')

joinability = context.Scripts.get.group_joinability()
permjoinability = form.get('permjoin', 'group')
if joinability != permjoinability:
    if group.hasProperty('join_condition'):
        group.manage_changeProperties(join_condition=permjoinability)
    else:
        group.manage_addProperty('join_condition', permjoinability, 'string')
    
    if permjoinability == 'anyone':
        context.Scripts.set.list_property(group.getId(), 'subscribe', 'subscribe')
    else:
        context.Scripts.set.list_property(group.getId(), 'subscribe', '')
    
    message.append('<li>Updated group joinability</li>')

filesvisibility = context.Scripts.get.group_files_visibility()
permviewfiles = form.get('permviewfiles', 'group')
if filesvisibility != permviewfiles:
    if permviewfiles == 'default':
        group.files.manage_permission('View', [], 1)
        group.files.manage_permission('Access contents information', [], 1)
        message.append('<li>Updated file area permissions to restore to group defaults</li>')
    elif permviewfiles == 'anyone':
        group.files.manage_permission('View', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('Access contents information', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated file area permissions to make the files visible to anyone</li>')
    elif permviewfiles == 'division':
        group.files.manage_permission('View', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('Access contents information', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated file area permissions to make the files visible to only division and group members</li>')    
    elif permviewfiles == 'group':
        group.files.manage_permission('View', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('Access contents information', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated file area permissions to make the files visible to only group members</li>')

messagevisibility = context.Scripts.get.group_messages_visibility()
permviewmessages = form.get('permviewmessages', 'group')
if messagevisibility != permviewmessages:
    if permviewmessages == 'default':
        group.messages.manage_permission('View', [], 1)
        group.messages.manage_permission('Access contents information', [], 1)
        message.append('<li>Updated messages area permissions to restore to group defaults</li>')
    elif permviewmessages == 'anyone':
        group.messages.manage_permission('View', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.messages.manage_permission('Access contents information', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated messages area permissions to make the messages visible to anyone</li>')
    elif permviewmessages == 'division':
        group.messages.manage_permission('View', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.messages.manage_permission('Access contents information', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated messages area permissions to make the messages visible to only division and group members</li>')    
    elif permviewmessages == 'group':
        group.messages.manage_permission('View', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.messages.manage_permission('Access contents information', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated messages area permissions to make the messages visible to only group members</li>')

m = '''<p>Updating group %s</p>
  <ul>%s</ul>''' % (html_quote(group.title_or_id()), '\n'.join(message))
retval = {'error': False, 'message': m}
return retval
