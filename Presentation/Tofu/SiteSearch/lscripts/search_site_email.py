## Script (Python) "search_site_email"
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

email_result_set = context.Presentation.Tofu.SiteSearch.lscripts.search_email(groups, query)

# e_b_start, e_b_end, e_b_size, e_result_size, e_result_set 
return createBatch(email_result_set, start, size)
