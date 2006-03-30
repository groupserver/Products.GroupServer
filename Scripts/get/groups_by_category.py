# groups_by_category
#  All the groups have a custom field, "Category" - and I want to sort them
#  by that, to make output pages easier to read

groupdict = {}
for group in groups:
    category = getattr(group,'category','Unclassified')
    if groupdict.has_key(category):
        groupdict[category].append(group)
    else:
        groupdict[category] = [group]
return groupdict
