## Script (Python) "search_email"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=text
##title=
##
from string import find, rfind, join

complete = text.replace('@', ' ( at ) ')

return complete

