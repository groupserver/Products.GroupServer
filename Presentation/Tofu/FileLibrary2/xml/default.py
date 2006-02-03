return container.REQUEST.RESPONSE.redirect(container.REQUEST.URL1+'/view_files?message=%s' % container.REQUEST.form.get('message', ''))
