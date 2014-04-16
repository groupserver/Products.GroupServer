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
from os.path import dirname, join


def get_import_path(filename=''):
    import Products.GroupServer.imports

    path = dirname(Products.GroupServer.imports.__file__)
    if filename:
        path = join(path, filename)

    return path


def get_groupserver_path(name=''):
    return 'GroupServer/%s' % name
