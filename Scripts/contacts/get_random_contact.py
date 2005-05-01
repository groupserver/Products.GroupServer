## Script (Python) "get_random_contact"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id_only=0, include_staff=1, exclude_affinities=1
##title=
##
import random

contacts = context.get_contacts(id_only, include_staff)
if exclude_affinities:
    affinities = context.get_contact_affinities(id_only)
    contacts = filter(lambda x: x not in affinities, contacts)

if contacts:
    return random.choice(contacts)
return None
