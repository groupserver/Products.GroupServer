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

# Find out the GlobalConfig supportEmail and the DivisionConfig canonicalHost
global_support_email = global_config.getProperty('supportEmail', 'support@onlinegroups.net')
canonical = division_config.getProperty('canonicalHost', 'onlinegroups.net')

# First, check if we're on an instance other than OGN
#  If so, just take the Global supportEmail
if global_support_email != 'support@onlinegroups.net':
    retval = global_config.supportEmail

# If not, we must be on the onlinegroups.net instance
else:
    # First, check if the site uses a subdomain of OGN
    if canonical == '%s.onlinegroups.net' % siteId:
        # Assume the site has a support group: we can't
        #   check because support groups are private and
        #   therefore inaccessible to anyone who wants to
        #   obtain help from them
        retval = '%s_support@onlinegroups.net' % siteId

    # If not, check if the site has a custom domain
    elif canonical != 'onlinegroups.net':
        # Assume the site has a support group: we can't
        #   check because support groups are private and
        #   therefore inaccessible to anyone who wants to
        #   obtain help from them
        retval = '%s_support@%s' % (siteId, canonical)

    # Otherwise, we must be on ogs
    else:
        retval = 'support@onlinegroups.net'

assert retval
assert '@' in retval
return retval

