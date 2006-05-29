## Script (Python) "addbulkusers"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Add Bulk Users from CSV
##
from Products.XWFCore.CSV import CSVFile

request = context.REQUEST
form = request.form
site_root = context.site_root()

submit = form.get('__submit__', '')
if not submit:
    return ''

# groupid is defined we're probably working as a group admin
# otherwise we're probably working as a division or site admin
groupid = form.get('groupid', '')
joingroups = form.get('groups', [])

sendVerification = form.get('sendVerification', [])

divisionid = form.get('divisionid')
csvfile = form.get('csvfile')
fields = {}
num_fields = 0
key_fields = ['email','firstName','lastName']
for key in form:
    parts = key.split('field')
    if len(parts) == 2:
        fields[int(parts[1])] = form[key]
        if form[key] != 'nothing':
            num_fields += 1
        try:
            key_fields.remove(form[key])
        except:
            pass
            
error = 0
message = []
if not csvfile:
    error = 1
    message.append("""<paragraph>You must specify a CSV file to
    process</paragraph>""") 

if key_fields:
    error = 1
    for field in key_fields:
        field_def = getattr(site_root.UserProperties, field, None)
        field_name = field_def and field_def.getProperty('title') or field
        message.append("""<paragraph>Missing compulsory column
        %s</paragraph>""" % field_name) 
        
try:
    results = CSVFile(csvfile, [str]*num_fields)
except AssertionError, x:
    error = 1
    message.append("""<paragraph>The number of columns you have
    defined does not match the number of columns in the CSV file you
    provided</paragraph>""")
    
if error:
    message.insert(0,
                   """<paragraph>The following errors have
                   occurred:</paragraph>""")
    return '\n'.join(message)

groups = ['%s_member' % divisionid]
try: # check for string/list ness, the hard way
    joingroups.split
    joingroups = [joingroups]
except:
    pass
for group in joingroups:
    groups.append('%s_member' % group)

if form.get('addtogroup', 'no') == 'yes' and groupid:
    groups.append('%s_member' % groupid)

rowcount = 1
errors = 0
created = 0
for row in results.mainData:
    field = 1
    fieldmap = {}
    for col in row:
        fieldId = fields[field]
        fieldmap[fieldId] = col
        field += 1

    firstName = fieldmap.get('firstName', '')
    lastName = fieldmap.get('lastName', '')
    userId = fieldmap.get('userId', '')
    email = fieldmap.get('email','')
    
    newmessage = context.verifyuserdata(firstName, lastName,
                                        userId, email)
    if newmessage:
        message += ["""<paragraph>The following error/s occurred in
        row %s:</paragraph>""" % rowcount]
        message += newmessage
        errors += 1
    else:
        # Add the user. We should check if the user is registered
        #   first, and just add them to the group if they are.

        # user = site_root.acl_users.get_userByEmail(email.lower())
        # if user:
        #   for group in groups:
        #     user.add_groupWithNotification(group)
        
        try:
            user = context.Scripts.registration.register_user(firstName,
                                                              lastName,
                                                              userId, email,
                                                              groups, 0,
                                                              fieldmap,
                                                              sendVerification)
            if not user:
                if user == None:
                    message += ["""<paragraph>The following exception
                    occured creating user in row %s:</paragraph>""" % \
                                rowcount]
                    message += ["""<paragraph>The user was unable to be
                    registered. Please report this as a
                    bug.</paragraph>"""]
                    errors += 1
                else:
                    message += ["""<paragraph>The following exception
                    occured creating user in row %s:</paragraph>""" % \
                                rowcount]
                    message += ["""<paragraph>The long and winding road!</paragraph>"""]
                    errors += 1
        except "Bad Request", x:
            message += ["""<paragraph>The following exception occured
            creating user in row %s:</paragraph>""" % rowcount]
            message += ["<paragraph>%s</paragraph>" % str(x)]
            errors += 1
        except Exception, x:
            message += ["""<paragraph>The following exception occured
            creating user in row %s:</paragraph>""" % rowcount]
            message += ["<paragraph>%s</paragraph>" % str(x)]
            errors += 1
        
        created += 1
        
    rowcount += 1

if message:
    if created == 0:
        message.insert(0, """<paragraph>Your file has been processed
        but %s errors occurred.</paragraph>""" % errors)
        message.insert(1,
                       "<paragraph>----------------------------------------------------</paragraph>")
        message.append("<paragraph>----------------------------------------------------</paragraph>")
    else:
        message.insert(0,
                       """<paragraph>Your file has been processed, %s
                       users were created, """
                       """but %s errors occurred with creating the
                       other users.</paragraph>""" % (created, errors))
        message.insert(1,
                       "<paragraph>----------------------------------------------------</paragraph>")
        message.append("<paragraph>----------------------------------------------------</paragraph>")
else:
    message.append("""<paragraph>Your file has been processed, and %s
    users were created.</paragraph>""" % created)
    
return '\n'.join(message)
