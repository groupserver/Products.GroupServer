import os
from Products.FileSystemSite.DirectoryView import registerDirectory

import pathutil

import groupserver

# registerDirectory is also in here to get around some serious chicken-egg
# problems with getting the module path
def initialize( context ):
    registerDirectory( pathutil.get_groupserver_path('Scripts'), globals() )
    registerDirectory( pathutil.get_groupserver_path('Presentation'), globals() )
    registerDirectory( pathutil.get_groupserver_path('help'), globals() )
    registerDirectory( pathutil.get_groupserver_path('admindivision'), globals() )
    registerDirectory( pathutil.get_groupserver_path('admingroup'), globals() )

    context.registerClass( 
        groupserver.GroupserverSite, 
        constructors = ( groupserver.manage_addGroupserverSiteForm, 
                         groupserver.manage_addGroupserverSite ),
        icon='icons/ic-groupserversite.png'

                           )

                           
