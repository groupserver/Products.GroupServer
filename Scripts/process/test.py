## Script (Python) "test"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
val = context.process.getProperty('title',0)
if not val:
    val = 0
else:
    val = int(val)

val += 1

context.manage_changeProperties(title=str(val))

return val
