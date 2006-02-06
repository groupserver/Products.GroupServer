## Script (Python) "search_files"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groups, query
##title=
##
queries = [{'title': query}, {'indexable_content': query}, {'tags': query}]
#,
#           , {'topic': query},
#           {'dc_creator': query}]

site_root = context.site_root()

def sorter(x, y):
    if x.modification_time < y.modification_time:
        return 1
    else:
        return -1

results = []
for (group_title, group_id, group_url) in context.Scripts.get.group_memberships_ids():
     for query in queries:
         query['group_ids'] = [group_id]
         result = site_root.FileLibrary2.find_files(query)
         results += result
         #for result in results:
         #    if result not in results:
         #        results.append(result)

results.sort(sorter)

return results
