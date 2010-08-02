## Script (Python) "change"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Change Group Delivery Settings
##

#--=mpj17=-- Based on the forms/specific_delivery/change_method.py script.

result = {}

form = context.REQUEST.form
assert form.has_key('group_id')
assert form.has_key('delivery_setting')
result['form'] = form
user =  context.REQUEST.AUTHENTICATED_USER
for field in form:
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass

delivery_setting = form.get('delivery_setting')
assert delivery_setting in 'dtr'
group_id = form.get('group_id')
assert group_id != ''
group_title = form.get('group_title')
assert group_id != ''
user = context.REQUEST.AUTHENTICATED_USER
assert user != None

if delivery_setting == 'd':
    # Disable delivery so posts are sent from this group
    user.set_disableDeliveryByKey(group_id)
    result['message'] = '''<paragraph>You will not receive any 
      posts from %s to you.</paragraph>''' % group_title
else:
    # Enable delivery so posts are sent from this group
    user.set_enableDeliveryByKey(group_id)

    if delivery_setting == 't':
        # Send out a topic digest, or\ldots
        result['message'] = '''<paragraph>The posts from %s will now
          be delivered to you in the form of a daily digest of
          topics.</paragraph>''' % group_title
        user.set_enableDigestByKey(group_id)
    else:
        result['message'] = '''<paragraph>You will now receive an
          email message whenever someone posts to
          %s.</paragraph>''' % group_title
        # Send out one message per post
        user.set_disableDigestByKey(group_id)

assert result.has_key('message')
result['error'] = False
return result
