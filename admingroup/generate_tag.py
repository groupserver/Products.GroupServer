## Script (Python) "generate_tag"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=tag_type, tag_fields
##title=Generate XML Tag
##
from Products.PythonScripts.standard import html_quote

assert tag_type, \
    "Did not receive tag_type"
assert tag_fields, \
    "Did not receive tag_fields dictionary for tag_type %s" % tag_type

if tag_fields.has_key('tag_value'):
    if hasattr(tag_fields['tag_value'], 'lower'):
        tag_fields['tag_value'] = html_quote(tag_fields['tag_value'])
    else:
        try:
            tf = []
            for val in tag_fields['tag_value']:
                tf.append(html_quote(val))
            tag_fields['tag_value'] = tf
        except:
            assert False, \
              'Error creating tag for property %s' % tag_fields['tag_id']

if tag_type == 'model_string':
    assert tag_fields.has_key('tag_id'), \
        "No key 'tag_id' in dictionary tag_fields for tag_type 'model_string'"
    assert tag_fields.has_key('tag_value'), \
        "No key 'tag_value' in dictionary 'tag_fields': tag_id %s" % tag_fields['tag_id']
    return """<%(tag_id)s>%(tag_value)s</%(tag_id)s>""" % tag_fields

elif tag_type == 'model_text':
    assert tag_fields.has_key('tag_id'), \
        "No key 'tag_id' in dictionary tag_fields for tag_type 'model_text'"
    assert tag_fields.has_key('tag_value'), \
        "No key 'tag_value' in dictionary 'tag_fields': tag_id %s" % tag_fields['tag_id']
    return """<%(tag_id)s>%(tag_value)s</%(tag_id)s>""" % tag_fields

elif tag_type == 'model_lines':
    assert tag_fields.has_key('tag_id'), \
        "No key 'tag_id' in dictionary tag_fields for tag_type 'model_lines'"
    assert tag_fields.has_key('tag_value'), \
        "No key 'tag_value' in dictionary 'tag_fields': tag_id %s" % tag_fields['tag_id']
    tag_fields['tag_value'] = '\n'.join(tag_fields['tag_value'])
    return """<%(tag_id)s>%(tag_value)s</%(tag_id)s>""" % tag_fields

elif tag_type == 'string':
    return """<xf:input model="%(model)s" ref="%(ref)s" class="text">
    <xf:label>%(label)s</xf:label>
    <xf:hint>%(hint)s</xf:hint>
</xf:input>""" % tag_fields

elif tag_type in ('text', 'lines'):
    return """<xf:textarea model="%(model)s" ref="%(ref)s" class="textarea">
    <xf:label>%(label)s</xf:label>
    <xf:hint>%(hint)s</xf:hint>
</xf:textarea>""" % tag_fields
