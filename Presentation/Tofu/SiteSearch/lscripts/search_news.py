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

queries = [{'dc_title': query}, {'dc_description': query}, {'tags': query}, {'dc_creator': query}]

division = context.Scripts.get.division_object()

if not query.strip():
    return createBatch([], start, size)

results = context.Catalog.searchResults(meta_type='XWF News Item',
                                        path=division.getPhysicalPath(),
                                        dc_valid={'query': DateTime.DateTime(),
                                                  'range': 'max'},
                                        sort_order='descending',
                                        dc_description=query)

return createBatch(results, start, size)
