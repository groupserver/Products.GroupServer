========================
``Products.GroupServer``
========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The core GroupServer product
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-05-22
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

Introduction
============

The main task of this product is to `set up`_ the initial
GroupServer_ instance, and the first site.  This product also
contains the `GroupserverSite`_ class, which forms the core of a
GroupServer instance, not a site (despite its name).  This
product does very little, as most of the functionality of
GroupServer is provided by the many ``gs.*`` eggs.


Set up
======

The setup of the initial GroupServer instance and site is handled
by the functions (yes, *functions*) in the
``Products.GroupServer.creation`` module. The entry-point is the
``manage_addGroupserverSite`` function.

``GroupServerSite``
===================

The ``Products.GroupServer.GroupserverSite`` class is based on
``OFS.OrderedFolder``, but it provides three extra *methods*.

#.  ``get_site`` returns the ``GroupServerSite`` instance. This
    is useful to find the ``acl_users``, ``Contents``, or
    ``ListManager`` instances:

    .. code-highlight: python

      s = self.context.get_site() # Almost everything has self.context
      acl_users = s.acl_users     # Get the acl_users instance.
      contents = s.Contents       # The folder that contains the sites
      ListManager = s.ListManager # The folder that contains the mailing lists

#.  ``standard_error_message`` over-rides the standard Zope2
    error message, and calls the messages in ``gs.errormesg``.

#.  The ``fail`` method provides the "page" ``/fail``, which is
    used for testing the error-handling system.

Resources
=========

- Code repository:
  https://github.com/groupserver/Products.GroupServer/
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/
