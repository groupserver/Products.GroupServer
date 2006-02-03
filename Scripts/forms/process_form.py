## Script (Python) "process_form"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
result = {}

form = context.REQUEST.form
result['form'] = form

if not form.get('submitted', False):
    return result

submit = form.get('__submit__')
model, submission = submit.split('+')
model = form.get('model_override', model)

cb_container = getattr(container.aq_explicit, model)
cb = getattr(cb_container, submission)

return cb()
