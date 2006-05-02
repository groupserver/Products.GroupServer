## Script (Python) "check_subdomain"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=subdomain=""
##title=Check Subdomain
##
import string

result = {}

# Check to see if the domain name is valid. Dijkstra will hate me for
#   this.

if subdomain == '':
    result['error'] = True
    result['message'] = 'The subdomain must be specified.'
    return result

# Reference: http://www.ietf.org/rfc/rfc2396.txt section 3.2.2
#      domainlabel   = alphanum | alphanum *( alphanum | "-" ) alphanum
alphanum = string.digits + string.lowercase
validDomainChars = alphanum  + '-'
for c in subdomain:
    if c not in validDomainChars:
        result['error'] = True
        result['message'] = '''The character %c is not allowed in the
          subdomain. Please rewrite the subdomain.''' % c
        return result
if subdomain[0] not in alphanum:
    result['error'] = True
    result['message'] = '''The subdomain must start with a number or a
      letter. Please rewrite the subdomain.'''
    return result
if subdomain[-1] not in alphanum:
    result['error'] = True
    result['message'] = '''The subdomain must end with a number or a
      letter. Please rewrite the subdomain.'''
    return result

# If we are here, then all is well in the world
result['error'] = False
result['message'] = '''The subdomain %s is valid.''' % subdomain
return result

# --= Unit Tests =--
# >>> check_subdomain('foobar')['error'] == False
# >>> check_subdomain('foo-bar')['error'] == False
# >>> check_subdomain('foo=bar')['error'] == True
# >>> check_subdomain('-foobar')['error'] == True
# >>> check_subdomain('foobar-')['error'] == True
