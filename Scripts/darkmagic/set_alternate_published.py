## Script (Python) "set_alternate_published"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=published
##title=
##
request = container.REQUEST

request.other['PUBLISHED'] = published

return 1
