result = {}

site_root = context.site_root()
form = context.REQUEST.form
assert form.has_key('siteid')
result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

message = []
error = False

if not form.get('zone', None):
    result['error'] = True
    result['message'] = 'You must select a timezone'

if not result.get('error', False):
    siteid = form['siteid']
    zone = form['zone']
    site = context.restrictedTraverse('Content/%s' % siteid)
    div_config = getattr(site, 'DivisionConfiguration')

    try:
        # crude, really crude, way of telling if we're a list
        zone.append
        zone = zone[0]
    except:
        pass

    if not hasattr(div_config, 'timezone'):
        div_config.manage_addProperty('timezone', zone, 'string')
    div_config.manage_changeProperties(timezone=zone)

    result['error'] = False
    result['message'] = 'The site timezone has been changed to <code>%s</code>' % zone

return result

