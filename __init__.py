from App.config import getConfiguration
from Products.FileSystemSite.DirectoryView import registerDirectory

instance_home = getConfiguration().instancehome
registerDirectory( 'Products/GroupServer/Scripts', instance_home )
registerDirectory( 'Products/GroupServer/Presentation', instance_home )
registerDirectory( 'Products/GroupServer/help', instance_home )
registerDirectory( 'Products/GroupServer/admindivision', instance_home )

import groupserver

def initialize( context ):
    context.registerClass( 
        groupserver.GroupserverSite, 
        constructors = ( groupserver.manage_addGroupserverSiteForm, 
                         groupserver.manage_addGroupserverSite ),
        icon='icons/ic-groupserversite.png'

                           )

                           
