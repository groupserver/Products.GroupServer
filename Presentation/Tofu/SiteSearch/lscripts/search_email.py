## Script (Python) "search_email"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groups, search_term
##title=
##
from Products.XWFMailingListManager.queries import MessageQuery

m = MessageQuery(context, context.zsqlalchemy)

#queries = [{'mailSubject': search_term},
#           {'mailBody': search_term},
#           {'mailFrom': '*%s*' % search_term}]

division_object = context.Scripts.get.division_object()

groups = context.Scripts.get.groups()

group_id_titles = {}
for group in groups:
    try:
        group.messages.getId()
    except:
        continue

    group_id_titles[group.getId()] = group.title_or_id()

if not group_id_titles:
    return []

group_ids = group_id_titles.keys()

results = m.topic_search(search_term, division_object.getId(), group_ids=group_ids)
for result in results:
    result['group_title'] = group_id_titles[result['group_id']]
    result['url'] = '/groups/%s/messages/topic/%s' % (result['group_id'], result['last_post_id'])
    
return results
