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
    try:
        site = context.Scripts.get.division_object()
        sid = site.getId()
        r = context.LocalScripts.settings.get_object_from_settings(site_id=sid,
                                                                   object_id=key)
        if r:
            item = r.dictionaries()[0]
            retval = item['value']
        else:
            retval = default
    except:
        retval = default

return retval

