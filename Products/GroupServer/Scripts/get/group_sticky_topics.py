## Script (Python) "group_sticky_topics"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get the Sticky Topics for the Group
##
from Products.XWFCore.XWFUtils import deprecated
deprecated(context, script, "Use gs.group.messages.topic instead.")
group = context.Scripts.get.group_object()
assert group
assert group.messages
retval = []
          
stickyTopicsIds = group.getProperty('sticky_topics')
if stickyTopicsIds:
    for stickyTopicId in stickyTopicsIds:
        query = {'id': stickyTopicId}
        result = group.messages.find_email(query)[0]
        threadInfo = {'id':     result.id,
                      'name':   result.mailSubject,
                      'date':   result.mailDate,
                      'length': ''}
        retval.append(threadInfo)
return retval
