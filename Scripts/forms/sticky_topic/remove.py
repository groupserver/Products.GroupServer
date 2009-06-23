## Script (Python) "remove_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Remove Users from the Group Administration List
##
from Products.PythonScripts.standard import html_quote

result = {}

form = context.REQUEST.form
assert form.has_key('groupId')
assert form.has_key('siteId')
assert form.has_key('topicId')
result['form'] = form

for field in form.keys():
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass
topicId = form['topicId']
assert topicId
groupId = form['groupId']
assert groupId
siteId = form['siteId']
assert siteId

site_root = context.site_root()
site = getattr(site_root.Content, siteId)
assert site
group = getattr(site.groups, groupId)
assert group

if group.hasProperty('sticky_topics'):
    topics = list(group.getProperty('sticky_topics'))
    if topicId in topics:
        topics.remove(topicId)
    group.manage_changeProperties(sticky_topics=topics)
else:
    group.manage_addProperty('sticky_topics', [], 'lines')

result['message'] = '''<p>The topic is no longer sticky.</p>'''
result['error'] = False
return result
