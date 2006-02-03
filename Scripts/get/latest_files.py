## Script (Python) "latest_topics"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=limit=100
##title=
##
site_root = context.site_root()

def sorter(x, y):
    if x.modification_time < y.modification_time:
        return 1
    else:
        return -1

results = []
for (group_title, group_id, group_url) in context.Scripts.get.group_memberships_ids():
     result = site_root.FileLibrary2.find_files({'group_ids': [group_id]})
     if result:
         results += result

results.sort(sorter)

return results[:limit]
