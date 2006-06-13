## Script (Python) "accept_user_conditions"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Unverified User Accept Form Processor
##

result = {}

form = context.REQUEST.form
# I cannot assert the following, because of the
# oddities of HTML!
# assert form.has_key('accept')
assert form.has_key('came_from')

result['form'] = form

for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass
    
canonicalHost = context.Scripts.get.option('canonicalHost', None)
cameFrom = form.get('came_from', canonicalHost)

accept = form.get('accept', 0)
try:
    # since accept should be '1' if set
    accept = int(accept) and True or False
except ValueError:
    accept = True


if not accept:
    result['error'] = True
    result['message'] = '''Only people who accept all the terms and
      conditions can become users of OnlineGroups.Net'''
    return result
else:
    # The user has accepted the conditions, so return
    context.REQUEST.RESPONSE.redirect(cameFrom)
