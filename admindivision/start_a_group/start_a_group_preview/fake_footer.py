## Script (Python) "fake_footer"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=groupId="",groupName="",host=""
##title=Generate a Fake Footer
##
import string

def getValueFor(foo):
    return '%s@onlinegroups.net' % groupId

result = {}

site_root = context.site_root()

#host = context.Scripts.get.option('canonical_host', 'onlinegroups.net')
groupPropD = {'canonical_host': host,
              'title': groupName,
              'id': groupId}
listObjD = {'getId' : '19771975'}
gvfD = {'mailto': getValueFor }

user = context.REQUEST.AUTHENTICATED_USER
r = site_root.ListManager.email_footer(group_properties=groupPropD,
                                       list_object=listObjD,
                                       user_object=user,
                                       getValueFor=getValueFor,
                                      files = [])
return r.replace('\n', '<br/>')
