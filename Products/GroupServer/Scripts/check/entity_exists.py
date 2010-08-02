## Script (Python) "entity_exists"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=entityId=""
##title=Check if an Entity Exists
##
from Products.XWFCore.XWFUtils import entity_exists as true_entity_exists

return true_entity_exists(context, entityId)
