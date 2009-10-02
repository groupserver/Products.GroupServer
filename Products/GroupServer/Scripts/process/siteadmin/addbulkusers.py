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

msg = ''
rowcount = 2
errors = 0
created = 0
added = 0
for row in results.mainData:
    field = 1
    fieldmap = {}
    for col in row:
        fieldId = fields[field]
        fieldmap[fieldId] = col
        field += 1

    firstName = fieldmap.get('firstName', '')
    lastName = fieldmap.get('lastName', '')
    preferredName = fieldmap.get('preferredName', '')
    email = fieldmap.get('email','').lower()
    userId = fieldmap.get('userId', '')

    user = site_root.acl_users.get_userByEmail(email)

    if user:
        result = container.adduser_add_user(user,groups)
        assert same_type(result, {})
        if result['error']:
            errors += 1
            msg = '''%s\n<listitem><bold>[Row %d]</bold>
            <bulletlist>
            %s
            </bulletlist>
            </listitem>''' % (msg, rowcount, result['message'])
        else:
            added += 1
    else:
        # The user does not exist, so create the user
        result = context.verifyuserdata(firstName, lastName, userId,
                                        email)
        if result:
            errors += 1
            msg = '''%s\n<listitem><bold>[Row %d]</bold>
            <bulletlist>
            %s
            <listitem>The user on row %d <bold>has not</bold> been
            created.</listitem>
            </bulletlist>
            </listitem>''' % (msg, rowcount, result, rowcount)
        else:
            result = container.adduser_create_new_user(firstName, lastName,
                                                       preferredName, email,
                                                       userId, groups, 
                                                       sendVerification, fieldmap)

            if result['error']:
                errors += 1
                msg = '''%s\n<listitem><bold>[Row %d]</bold>
                <bulletlist>
                %s
                </bulletlist>
                </listitem>''' % (msg, rowcount, result['message'])
            else:
                created += 1
    rowcount += 1

numRows = rowcount -1
retval = '''<paragraph>Your %d-row file was processed:</paragraph>
<bulletlist>''' % numRows
textGroups = ', '.join(map(lambda g: g.split('_member')[0], groups[:-1]))
textGroups = '%s and %s' % (textGroups, groups[-1].split('_member')[0])
if created > 0:
    userOrUsers = (created > 1 and 'users') or 'user'
    wereOrWas = (created > 1 and 'were') or 'was'
    retval = '''%s
    <listitem>There %s %d new %s created and
    added to %s''' % (retval, wereOrWas, created, userOrUsers,
                      textGroups)
else:
    retval = '''%s
    <listitem>There were no new users created''' % retval
if added > 0:
    userOrUsers = (added > 1 and 'users') or 'user'
    wereOrWas = (added > 1 and 'were') or 'was'
    retval = '''%s,</listitem>
    <listitem>While %d existing %s %s
    added to %s.</listitem>''' % (retval, added, userOrUsers,
                                  wereOrWas, textGroups)
else:
    retval = '''%s.</listitem>''' % retval
retval = '''%s</bulletlist>''' % retval
if errors > 0:
    errorOrErrors = (errors > 1 and 'errors') or 'error'
    isOrAre = (errors > 1 and 'are') or 'is'
    rowOrRows = (errors > 1 and 'rows') or 'row'
    retval = '''%s\n<paragraph>Thre were also %d %s, which %s
    detailed as  follows.</paragraph>
    <bulletlist>
    %s
    </bulletlist>'''% (retval, errors, errorOrErrors, isOrAre,
                       msg)
retval = '''%s
  <paragraph>(The top row was treated as a
   header.)</paragraph>''' % retval

return retval
