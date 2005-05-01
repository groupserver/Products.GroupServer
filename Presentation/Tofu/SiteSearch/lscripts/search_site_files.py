## Script (Python) "search_site_files"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=query, start=1, size=10
##title=
##
from Products.XWFCore.XWFUtils import createBatch

groups = context.Scripts.get.groups()

file_result_set = context.search_files(groups, query)
rids = []
nfile_result_set = []
for result in file_result_set:
    rid = result.id
    if rid not in rids:
        rids.append(rid)
        nfile_result_set.append(result)

# e_b_start, e_b_end, e_b_size, e_result_size, e_result_set 
return createBatch(nfile_result_set, start, size)
