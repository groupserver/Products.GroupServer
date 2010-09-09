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
result = {}

site_root = context.site_root()

#host = context.Scripts.get.option('canonical_host', 'onlinegroups.net')
groupPropD = {'canonical_host': host,
              'title':          groupName,
              'id':             groupId}
listObjD = {'getId' : '19771975'}
mailto = '%s@onlinegroups.net' % groupId
user = context.REQUEST.AUTHENTICATED_USER
r = site_root.ListManager.email_footer(context.REQUEST,
                                       list_object      = listObjD,
                                       group_properties = groupPropD,
                                       title            = 'title',
                                       mailto           = mailto,
                                       mail             = 'mail',
                                       body             = 'body',
                                       user_object      = user,
                                       from_addr        = 'from_addr',
                                       files            = [],
                                       post_id          = 'example',
                                       pap_set          = '')
return r.replace('\n', '<br/>')

