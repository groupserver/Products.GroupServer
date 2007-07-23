## Script (Python) "support_email"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=siteId
##title=Get Support Email
##

site_root = context.site_root()
site = getattr(site_root.Content, siteId, None)
division_config = getattr(context, 'DivisionConfiguration', None)
assert division_config, 'Division Config set to %s' % division_config
global_config = getattr(context, 'GlobalConfiguration', None)
assert global_config, 'Global Config set to %s' % global_config

global_support_email = global_config.getProperty('supportEmail', 'support@onlinegroups.net')
canonical = division_config.getProperty('canonicalHost', 'onlinegroups.net')

if global_support_email != 'support@onlinegroups.net':    # if we're on an instance other than onlinegroups.net
    retval = global_config.supportEmail
else:                                                     # if we're on the onlinegroups.net instance
    if canonical == '%s.onlinegroups.net' % siteId:       # if the site uses a subdomain of onlinegroups.net
        if hasattr(site.groups, '%s_support' % siteId):
            retval = '%s_support@onlinegroups.net' % siteId   # and if the site has a support group
        else:
            retval = 'support@onlinegroups.net'               # otherwise support@onlinegroups.net
    elif canonical != 'onlinegroups.net':                 # if the site is has a custom domain
        if hasattr(site.groups, '%s_support' % siteId):
            retval = '%s_support@%s' % (siteId, canonical)    # and if the site has a support group
        else:
            retval = 'support@onlinegroups.net'               # otherwise support@onlinegroups.net
    else:
        retval = 'support@onlinegroups.net'

assert retval
assert '@' in retval
return retval

