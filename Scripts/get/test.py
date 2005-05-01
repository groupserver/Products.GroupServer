## Script (Python) "test"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
return 'user '+str(context.REQUEST.AUTHENTICATED_USER.getId())
return 'foo'
