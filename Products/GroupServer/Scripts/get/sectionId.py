## Script (Python) "sectionId"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use something sane instead.")
return getattr(context, 'section_id', 'home')

