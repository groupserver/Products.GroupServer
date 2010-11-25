# coding=utf-8
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='Products.GroupServer',
    version=version,
    description="Base GroupServer product",
    long_description=open("README.txt").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Framework :: Zope2",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: GNU General Public License (GPL)",
      "Natural Language :: English",
      "Operating System :: POSIX :: Linux",
      "Programming Language :: Python",
      "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='groupserver',
    author='Richard Waid',
    author_email='richard@iopen.net',
    url='http://groupserver.org',
    license='GNU GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'setuptools',
        'Products.CustomUserFolder',
        'Products.XWFCore',
        'gs.profile.password',
        'gs.group.member.join',
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,)

