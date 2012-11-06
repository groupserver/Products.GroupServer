Introduction
============

This product contains the ``GroupserverSite`` class, which forms the core
of a GroupServer_ instance. Its main responsibility is for setting up the
initial site during installation.

The ``GroupserverSite`` class is based on ``OFS.OrderedFolder``, but it
provides three extra *methods*.

#.  ``get_site`` returns the ``GroupServerSite`` instance. This is useful
    to find the ``acl_users``, ``Contents``, or ``ListManager`` instances::

      s = self.context.get_site() # Almost everything has self.context
      acl_users = s.acl_users     # Get the acl_users instance.
      contents = s.Contents       # The folder that contains the sites
      ListManager = s.ListManager # The folder that contains the mailing lists

#.  ``standard_error_message`` over-rides the standard Zope2 error message,
    and calls the messages in ``gs.errormesg``.

#.  The ``fail`` method provides the "page" ``/fail``, which is used for
    testing the error-handling system.

This product does little else, as most of the functionality of GroupServer
is provided by the many ``gs.*`` eggs.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/Products.GroupServer
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org
