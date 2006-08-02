## Script (Python) "option"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=key, default=None
##title=
##
site_root = context.site_root()

user = context.REQUEST.AUTHENTICATED_USER
global_config = getattr(context, 'GlobalConfiguration', None)
division_config = getattr(context, 'DivisionConfiguration', None)

retval = None
for config in [user, division_config, global_config]:
    try:
        value = config.getProperty(key, None)
        if value != None:
            retval = value
            break
    except:
        pass

# Try in the settings dB
if retval == None:
    retval = default

return retval

