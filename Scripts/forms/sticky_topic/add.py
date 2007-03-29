## Script (Python) "add"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Add a topic to the list of sticky topics
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
assert groupId != None
siteId = form['siteId']
assert siteId != None

site_root = context.site_root()
site = getattr(site_root.Content, siteId)
assert site
group = getattr(site.groups, groupId)
assert group

if group.hasProperty('sticky_topics'):
    topics = filter(None, group.getProperty('sticky_topics'))
    if topicId not in topics:
        topics.append(topicId)
        group.manage_changeProperties(sticky_topics=topics)
else:
    group.manage_addProperty('sticky_topics', [topicId], 'lines')

assert group.hasProperty('sticky_topics')

result['message'] = '''<p>The topic is now sticky.</p>'''
result['error'] = False
return result

