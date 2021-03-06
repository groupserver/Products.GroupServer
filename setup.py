# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
# 2014, 2015 OnlineGroups.net and Contributors.
#
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"), encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(name='Products.GroupServer',
    version=version,
    description="Base GroupServer product",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='groupserver',
    author='Richard Waid',
    author_email='richard@iopen.net',
    maintainer='Michael JasonSmith',
    maintainer_email='mpj17@onlinegroups.net',
    url='https://github.com/groupserver/Products.GroupServer/',
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,  # --=mpj17=-- False because of FileSystemSite evil
    install_requires=[  # FIXME: sort out the egg deps.
        'setuptools',
        'zope.component',
        'zope.interface',
        'zExceptions',
        'AccessControl',
        'Products.FileSystemSite',
        'Zope2',
        'Products.CustomUserFolder',
        'Products.XWFCore',
        'gs.core',
        'gs.group.member.join',
        'gs.group.start',
        'gs.profile.email.verify',
        'gs.profile.password',
        'Products.GSProfile',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,)
