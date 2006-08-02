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
for config in [user, division_config]:
    try:
        value = config.getProperty(key, None)
        if value != None:
            retval = value
            break
    except:
        pass

# Try in the settings dB
if retval == None:
    try:
        site = context.Scripts.get.division_object()
        r = context.LocalScripts.settings.get_settings(site_id=site.getId())
        if r:
            d = r.dictionaries()
            retval = filter(lambda i: i['item'] == key, d)[0]['value']
        else:
            retval = default
    except:
        retval = None

if retval == None:
    try:
        retval = global_config.getProperty(key, None)
    except:
        retval = None

if retval == None:
    retval = default
return retval

