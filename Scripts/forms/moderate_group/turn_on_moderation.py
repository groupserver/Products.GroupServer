## Script (Python) "turn_on_moderation"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Turn On Group Moderation
##
from Products.PythonScripts.standard import html_quote

result = {}
form = context.REQUEST.form
assert form.has_key('groupid')
assert form.has_key('divisionid')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

site_root = context.site_root()
groupid = form.get('groupid')
divisionid = form.get('divisionid')
group = context.Scripts.get.group_by_id(groupid)
assert(group != None)

if group.Scripts.get.division_object().getId() != divisionid:
    result['error']= True
    result['message'] = '''<paragraph><bold>Properties not
    changed.:<bold>  There appears to be a group in a different
    division with the same  ID; unable to change
    properties.</paragraph>'''

    return result

listManager = site_root.objectValues('XWF Mailing List Manager')[0]
grouplist = getattr(listManager, groupid)
assert(grouplist != None)

if grouplist.hasProperty('moderated'):
    grouplist.manage_changeProperties(moderated=1)
else:
    grouplist.manage_addProperty('moderated', 1, 'boolean')

# Place the mailinlist_members script into the group
if hasattr(grouplist, 'mailinlist_members'):
  try:
    grouplist.manage_delObjects(['mailinlist_members'])
  except:
    pass
assert site_root.CodeTemplates.ListManager
mailinlist_members = getattr(site_root.CodeTemplates.ListManager,
                             'moderated-mailinlist_members')
assert mailinlist_members
grouplist.manage_clone(mailinlist_members, 'mailinlist_members')

result['error'] = False
result['message'] = '''<paragraph>Moderation is
    <em>on.</em></paragraph>'''
return result
