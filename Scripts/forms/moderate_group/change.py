## Script (Python) "change"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Change Group Moderation
##
from Products.PythonScripts.standard import html_quote

result = {}
form = context.REQUEST.form
assert form.has_key('groupid')
assert form.has_key('siteid')
assert form.has_key('moderation_level')
assert form['moderation_level'] in ('none', 'specified_and_new', 
                                    'specified_only')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

site_root = context.site_root()
groupid = form.get('groupid')
siteid = form.get('siteid')

listManager = site_root.objectValues('XWF Mailing List Manager')[0]
grouplist = getattr(listManager, groupid)
assert(grouplist != None)

if (not grouplist.hasProperty('moderated')):
    grouplist.manage_addProperty('moderated', 0, 'boolean')
if (not grouplist.hasProperty('moderate_new_members')):
    grouplist.manage_addProperty('moderate_new_members', 0, 'boolean')

assert(grouplist.hasProperty('moderated'))
assert(grouplist.hasProperty('moderate_new_members'))

moderation_level = form['moderation_level']

if (moderation_level == 'none'):
    grouplist.manage_changeProperties(moderated=0)
    grouplist.manage_changeProperties(moderate_new_members=0)
    if hasattr(grouplist, 'mailinlist_members'):
        grouplist.manage_delObjects(['mailinlist_members'])
    message = "Moderation has been turned off: no posts will be moderated."
elif (moderation_level == 'specified_and_new'):
    grouplist.manage_changeProperties(moderated=1)
    grouplist.manage_changeProperties(moderate_new_members=1)
    # Place the mailinlist_members script into the group
    if hasattr(grouplist, 'mailinlist_members'):
        grouplist.manage_delObjects(['mailinlist_members'])
    assert site_root.CodeTemplates.ListManager
    mailinlist_members = getattr(site_root.CodeTemplates.ListManager,
                                 'moderated-mailinlist_members')
    assert mailinlist_members
    grouplist.manage_clone(mailinlist_members, 'mailinlist_members')
    message = '''Moderation has been turned on: posts from specified
    members will be moderated, and any new members will automatically
    be moderated.'''
elif (moderation_level == 'specified_only'):
    grouplist.manage_changeProperties(moderated=1)
    grouplist.manage_changeProperties(moderate_new_members=0)
    # Place the mailinlist_members script into the group
    if hasattr(grouplist, 'mailinlist_members'):
        grouplist.manage_delObjects(['mailinlist_members'])
    assert site_root.CodeTemplates.ListManager
    mailinlist_members = getattr(site_root.CodeTemplates.ListManager,
                                 'moderated-mailinlist_members')
    assert mailinlist_members
    grouplist.manage_clone(mailinlist_members, 'mailinlist_members')
    message = '''Moderation has been turned on: posts from specified
    members will be moderated.'''

result['error'] = False
result['message'] = "<p>%s</p>" % message

return result
