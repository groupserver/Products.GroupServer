## Script (Python) "all_group_members"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=All members of a group, including unverified
##

def sorter(a,b):
    if a.getProperty('fn', '').lower() > b.getProperty('fn', '').lower():
        return 1
    else:
        return -1

allUsers = context.Scripts.get.unverified_group_members() + context.Scripts.get.group_members() 

u = {}
for user in allUsers:
  u[user] = 1

retval = u.keys()
retval.sort(sorter)

return retval
