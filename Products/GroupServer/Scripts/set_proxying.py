## Script (Python) "set_proxying"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
context.REQUEST.RESPONSE.setHeader('Cache-Control', 'private')
