## Script (Python) "search_news"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=query, start=1, size=10
##title=
##
import DateTime
from Products.XWFCore.XWFUtils import createBatch

division = context.Scripts.get.division_object()

if not query.strip():
    return createBatch([], start, size)

results = context.Catalog.searchResults(meta_type='XML Template',
                                        sort_order='descending',
                                        indexable_content=query)

valid_results = []
for result in results[:30]:
    try:
        obj = result.getObject()
        obj.title
        valid_results.append(result)
    except:
        pass

return createBatch(valid_results, start, size)
