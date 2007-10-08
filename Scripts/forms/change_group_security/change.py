## Script (Python) "change_group_security"
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
assert form.has_key('permjoin')
assert form.has_key('permvisibility')
assert form.has_key('permviewmessages')
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

joinability = group.Scripts.get.group_joinability()
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

visibility = group.Scripts.get.group_visibility()
permvisibility = form.get('permvisibility', 'group')
if visibility != permvisibility:
    if permvisibility == 'anyone':
        group.manage_permission('View', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.manage_permission('Access contents information', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated permissions to make the group visible to anyone</li>')
    elif permvisibility == 'division':
        group.manage_permission('View', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.manage_permission('Access contents information', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated permissions to make the group visible to site members</li>')    
    elif permvisibility == 'group':
        group.manage_permission('View', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.manage_permission('Access contents information', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated permissions to make the group visible to group members only</li>')

messagevisibility = group.Scripts.get.group_messages_visibility()
permviewmessages = form.get('permviewmessages', 'group')
if messagevisibility != permviewmessages:
    if permviewmessages == 'anyone':
        group.messages.manage_permission('View', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.messages.manage_permission('Access contents information', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('View', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('Access contents information', ['Anonymous', 'Authenticated', 'DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated permissions to make the messages and files visible to anyone</li>')
    elif permviewmessages == 'division':
        group.messages.manage_permission('View', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.messages.manage_permission('Access contents information', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('View', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('Access contents information', ['DivisionMember', 'DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated permissions to make the messages and files visible to site and group members only</li>')    
    elif permviewmessages == 'group':
        group.messages.manage_permission('View', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.messages.manage_permission('Access contents information', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('View', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        group.files.manage_permission('Access contents information', ['DivisionAdmin','GroupAdmin','GroupMember','Manager', 'Owner'])
        message.append('<li>Updated permissions to make the messages and files visible to group members only</li>')

m = '''<p>Updating group %s</p>
  <ul>%s</ul>''' % (html_quote(group.title_or_id()), '\n'.join(message))
retval = {'error': False, 'message': m}
return retval
