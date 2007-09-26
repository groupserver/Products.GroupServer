## Script (Python) "create"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Create Members in Bulk
##
from Products.XWFCore.CSV import CSVFile

form = context.REQUEST.form
site_root = context.site_root()
result = {}
result['form'] = form

assert form.has_key('groupid')
assert form.has_key('divisionid')

for field in form.keys():
    try:
        form[field] = form[field].strip()
    except AttributeError:
        pass
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
    message.append("""<p>You must specify a CSV file to
    process</p>""") 

if key_fields:
    error = 1
    for field in key_fields:
        field_def = getattr(site_root.UserProperties, field, None)
        field_name = field_def and field_def.getProperty('title') or field
        message.append("""<p>Missing compulsory column
        %s</p>""" % field_name) 
        
try:
    results = CSVFile(csvfile, [str]*num_fields)
except AssertionError, x:
    error = 1
    message.append("""<p>The number of columns you have
    defined does not match the number of columns in the CSV file you
    provided</p>""")
    
if error:
    message.insert(0,
                   """<p>The following errors have
                   occurred:</p>""")
                   
    return {'error': True,
            'message': '\n'.join(message)}

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
        # The user already exists, so just add them to the groups.
        result = container.process.siteadmin.adduser_add_user(user,groups)
        assert same_type(result, {})
        if result['error']:
            errors += 1
            msg = """%s\n<li><strong>[Row %d]</strong>
            <ul>
            %s
            </ul>
            </li>""" % (msg, rowcount, result['message'])
        else:
            added += 1
    else:
        # The user does not exist, so create the user
        result = context.process.siteadmin.verifyuserdata(firstName, lastName,
                                        userId, email)
        if result:
            errors += 1
            msg = """%s\n<li><strong>[Row %d]</strong>
            <ul>
            %s
            <li>The user on row %d <bold>has not</bold> been
            created.</li>
            </ul>
            </li>""" % (msg, rowcount, result, rowcount)
        else:
            result = container.process.siteadmin.adduser_create_new_user(firstName, lastName,
                                                       preferredName, email,
                                                       userId, groups, 
                                                       sendVerification, fieldmap)

            if result['error']:
                errors += 1
                msg = """%s\n<li><strong>[Row %d]</strong>
                <ul>
                %s
                </ul>
                </li>""" % (msg, rowcount, result['message'])
            else:
                created += 1
    rowcount += 1

numRows = rowcount -1
retval = """<p>Your %d-row file was processed:</p>
<ul>""" % numRows
textGroups = ', '.join(map(lambda g: g.split('_member')[0], groups[:-1]))
textGroups = '%s and %s' % (textGroups, groups[-1].split('_member')[0])
if created > 0:
    userOrUsers = (created > 1 and 'users') or 'user'
    wereOrWas = (created > 1 and 'were') or 'was'
    retval = """%s
    <li>There %s %d new %s created and
    added to %s""" % (retval, wereOrWas, created, userOrUsers,
                      textGroups)
else:
    retval = """%s
    <li>There were no new users created""" % retval
if added > 0:
    userOrUsers = (added > 1 and 'users') or 'user'
    wereOrWas = (added > 1 and 'were') or 'was'
    retval = '''%s,</li>
    <li>While %d existing %s %s
    added to %s.</li>''' % (retval, added, userOrUsers,
                             wereOrWas, textGroups)
else:
    retval = '''%s.</li>''' % retval
retval = '''%s</ul>''' % retval
if errors > 0:
    errorOrErrors = (errors > 1 and 'errors') or 'error'
    wereOrWas = (errors > 1 and 'were') or 'was'
    isOrAre = (errors > 1 and 'are') or 'is'
    rowOrRows = (errors > 1 and 'rows') or 'row'
    retval = """%s\n<p>There %s also %d %s, which %s
    detailed as  follows.</p>
    <ul>
    %s
    </ul>"""% (retval, wereOrWas, errors, errorOrErrors, isOrAre,
               msg)
retval = """%s
  <p>(The top row was treated as a
   header.)</p>""" % retval

return {'error': errors > 0,
        'message': retval}
