import os
from Products.FileSystemSite.DirectoryView import registerDirectory

GROUPSERVERPATH = os.path.dirname(__file__)
registerDirectory( os.path.join(GROUPSERVERPATH, 'Scripts'), globals() )
registerDirectory( os.path.join(GROUPSERVERPATH, 'Presentation'), globals() )
registerDirectory( os.path.join(GROUPSERVERPATH, 'help'), globals() )
registerDirectory( os.path.join(GROUPSERVERPATH, 'admindivision'), globals() )
registerDirectory( os.path.join(GROUPSERVERPATH, 'admingroup'), globals() )

import groupserver

def initialize( context ):
    context.registerClass( 
        groupserver.GroupserverSite, 
        constructors = ( groupserver.manage_addGroupserverSiteForm, 
                         groupserver.manage_addGroupserverSite ),
        icon='icons/ic-groupserversite.png'

                           )

                           
