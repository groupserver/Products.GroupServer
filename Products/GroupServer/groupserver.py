# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2008, 2009, 2010, 2011, 2012, 2013, 2014 OnlineGroups.net and
# Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
import datetime
from logging import getLogger
log = getLogger('Products.GroupServer')
import sys
if (sys.version_info < (3, )):
    from urlparse import urlsplit
else:
    from urllib.parse import urlsplit  # lint:ok
from zope.component import getMultiAdapter
from OFS.OrderedFolder import OrderedFolder
from Products.XWFCore.XWFUtils import createRequestFromRequest, rfc822_date
from gs.core import to_ascii


class GroupserverSite(OrderedFolder):
    meta_type = 'Groupserver Site'

    def __init__(self, id, title=''):
        OrderedFolder.__init__(self, id)
        self.title = title

    def get_site(self):
        """ Return ourself."""
        return self
    site_root = get_site

    def setAuthCookie(self, resp, cookie_name, cookie_value):
        """ Persistent authentication cookie support."""
        path = self.cookie_authentication.getCookiePath()
        if self.REQUEST.form.get('__ac_persistent', 0):
            expires = rfc822_date(datetime.datetime.utcnow() +
                                  datetime.timedelta(365))
            resp.setCookie(cookie_name, cookie_value, path=path,
                            expires=expires)
        else:
            resp.setCookie(cookie_name, cookie_value, path=path)

    def getRealContext(self):
        request = self.REQUEST
        p = urlsplit(request.URL1)[2].split('/')
        path = tuple([_f for _f in p if _f])
        virtual_path = request.get('VirtualRootPhysicalPath', ())
        path = virtual_path + path
        context = self.unrestrictedTraverse(path)
        return context

    def index_html(self):
        """ Return the default view"""
        redirect = self.REQUEST.RESPONSE.redirect
        redirectFile = ''

        # ---=mpj17=---
        # If there is a content_en.xml file, then we are working with a
        #   Five GSContent folder, so call index.html. Otherwise call
        #   the ol' Zope 2 index.xml page template
        context = self.getRealContext()
        if (hasattr(context.aq_explicit, 'content_en.xml')
            or hasattr(context.aq_explicit, 'content_en')):
            redirectFile = 'index.html'
        else:
            redirectFile = 'index.xml'

        # ---=mpj17=--- Now construct the URL
        u = '/'.join((self.REQUEST.URL1, redirectFile))
        request = createRequestFromRequest(self.REQUEST)
        if len(request) > 0:
            u = '?'.join((u, request))
        url = to_ascii(u)
        return redirect(url, lock=1)

    def standard_error_message(self, **kw):
        """ Override the default standard_error_message.

        """
        request = self.REQUEST
        context = self.getRealContext()
        if kw['error_type'] == 'NotFound':
            URL = request.get('URL', '')
            HTTP_REFERRER = request.get('HTTP_REFERER', '')
            m = '404: Link from <{referrer}> to <{url}> is broken.'
            log.warn(m.format(referrer=HTTP_REFERRER, url=URL))
            page = getMultiAdapter((context, request), name='not_found.html')
            retval = page()
        # ignore these types
        elif kw['error_type'] in ('Forbidden',):
            raise  # Propogate the error up.
        else:
            request = self.REQUEST
            context = self.getRealContext()
            page = getMultiAdapter((context, request),
                                   name='unexpected_error.html')
            retval = page()
        return retval

    def fail(self):
        """A test for the error-handling system.
        """
        m = 'This is a test of the error-handling system.'
        raise RuntimeError(m)
