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

form = context.REQUEST.form
site_root = context.site_root()

submit = form.get('__submit__', '')
if not submit:
    return ''

message = []
error = 0

groupid = form.get('groupid')
divisionid = form.get('divisionid')
group = context.Scripts.get.group_by_id(groupid)
if group.Scripts.get.division_object().getId() != divisionid:
    error = 1
    message.append('<paragraph>There appears to be a group in a different division with the same ID, unable to change properties.</paragraph>')

listManager = site_root.objectValues('XWF Mailing List Manager')[0]
grouplist = getattr(listManager, groupid)

senderlimit = form.get('senderlimit', 0)
try:
    senderlimit = int(senderlimit)
except:
    error = 1
    message.append('<paragraph>The posting limit must be an integer</paragraph>')

senderinterval = form.get('senderinterval', 0)
try:
    senderinterval = int(senderinterval)
except:
    error = 1
    message.append('<paragraph>The posting interval must be an integer</paragraph>')

if error:
    return '\n'.join(message)
    
message.append('<paragraph>Updating group %s</paragraph>' % html_quote(group.title_or_id()))

if getattr(grouplist, 'senderlimit', 0) != senderlimit:
    if grouplist.hasProperty('senderlimit'):
        grouplist.manage_changeProperties(senderlimit=senderlimit)
    else:
        grouplist.manage_addProperty('senderlimit', senderlimit, 'int')
    message.append('<paragraph>Updated sender limit</paragraph>')

if getattr(grouplist, 'senderinterval', 0) != senderinterval:
    if grouplist.hasProperty('senderinterval'):
        grouplist.manage_changeProperties(senderinterval=senderinterval)
    else:
        grouplist.manage_addProperty('senderinterval', senderinterval, 'int')
    message.append('<paragraph>Updated sender interval</paragraph>')

group_title = form.get('grouptitle', None)
if group_title:
    if group.getProperty('title') != group_title:
        group.manage_changeProperties(title=group_title)
        message.append('<paragraph>Updated group title</paragraph>')

coach_id = form.get('coach', None)
if coach_id:
    if group.getProperty('ptn_coach_id') != coach_id:
        group.manage_changeProperties(ptn_coach_id=coach_id)
        message.append('<paragraph>Updated participation coach</paragraph>')

for property in site_root.GroupProperties.objectValues():
    prop = form.get(property.getId(), None)
    if property.getProperty('property_type') in ('lines', 'ulines'):
        prop = tuple(map(lambda x: x.strip(), prop.split('\n')))
    else:
        prop = prop.strip()
    
    if prop != None and group.getProperty(property.getId()) != prop:
        if hasattr(group, property.getId()):
            group.manage_changeProperties({property.getId(): prop})
        else:
            group.manage_addProperty(property.getId(), prop, property.getProperty('property_type'))
        message.append('<paragraph>Updated %s</paragraph>' % html_quote(property.title_or_id()))

visibility = context.Scripts.get.group_visibility()
permvisibility = form.get('permvisibility', 'group')
if visibility != permvisibility:
    if permvisibility == 'anyone':
        group.manage_permission('View', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.manage_permission('Access contents information', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<paragraph>Updated group permissions to make the group visible to anyone</paragraph>')
    elif permvisibility == 'division':
        group.manage_permission('View', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.manage_permission('Access contents information', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<paragraph>Updated group permissions to make the group visible to only division members</paragraph>')    
    elif permvisibility == 'group':
        group.manage_permission('View', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.manage_permission('Access contents information', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<paragraph>Updated group permissions to make the group visible to only group members</paragraph>')

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
    
    message.append('<paragraph>Updated group joinability</paragraph>')

filesvisibility = context.Scripts.get.group_files_visibility()
permviewfiles = form.get('permviewfiles', 'group')
if filesvisibility != permviewfiles:
    if permviewfiles == 'default':
        group.files.manage_permission('View', [], 1)
        group.files.manage_permission('Access contents information', [], 1)
        message.append('<paragraph>Updated file area permissions to restore to group defaults</paragraph>')
    elif permviewfiles == 'anyone':
        group.files.manage_permission('View', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('Access contents information', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<paragraph>Updated file area permissions to make the files visible to anyone</paragraph>')
    elif permviewfiles == 'division':
        group.files.manage_permission('View', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('Access contents information', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<paragraph>Updated file area permissions to make the files visible to only division and group members</paragraph>')    
    elif permviewfiles == 'group':
        group.files.manage_permission('View', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('Access contents information', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<paragraph>Updated file area permissions to make the files visible to only group members</paragraph>')

messagevisibility = context.Scripts.get.group_messages_visibility()
permviewmessages = form.get('permviewmessages', 'group')
if messagevisibility != permviewmessages:
    if permviewmessages == 'default':
        group.messages.manage_permission('View', [], 1)
        group.messages.manage_permission('Access contents information', [], 1)
        message.append('<paragraph>Updated messages area permissions to restore to group defaults</paragraph>')
    elif permviewmessages == 'anyone':
        group.messages.manage_permission('View', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.messages.manage_permission('Access contents information', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<paragraph>Updated messages area permissions to make the messages visible to anyone</paragraph>')
    elif permviewmessages == 'division':
        group.messages.manage_permission('View', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.messages.manage_permission('Access contents information', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<paragraph>Updated messages area permissions to make the messages visible to only division and group members</paragraph>')    
    elif permviewmessages == 'group':
        group.messages.manage_permission('View', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.messages.manage_permission('Access contents information', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<paragraph>Updated messages area permissions to make the messages visible to only group members</paragraph>')

return '\n'.join(message)
