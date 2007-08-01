## Script (Python) "change_group_properties"
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
assert form.has_key('grouptitle')
assert form.has_key('groupSubject')
assert form.has_key('coach')
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

# Change the title of the list manager object for the group.
groupSubject = form.get('groupSubject', None)
if groupSubject:
    if grouplist.getProperty('title') != groupSubject:
        grouplist.manage_changeProperties(title=groupSubject)
        message.append('<li>Updated subject line.</li>')

# Change the title of the group.
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

m = '''<p>Updating group %s</p>
  <ul>%s</ul>''' % (html_quote(group.title_or_id()), '\n'.join(message))
retval = {'error': False, 'message': m}
return retval
