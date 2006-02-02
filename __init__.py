from App.config import getConfiguration
from Products.FileSystemSite.DirectoryView import registerDirectory

instance_home = getConfiguration().instancehome
registerDirectory('Products/GroupServer/Scripts', instance_home)
registerDirectory('Products/GroupServer/Presentation', instance_home)
