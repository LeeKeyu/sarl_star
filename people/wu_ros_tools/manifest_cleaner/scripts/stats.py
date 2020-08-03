#!/usr/bin/python

import rospy
import xml.dom.minidom
import os
import os.path
import sys
import collections
import operator
from urlparse import urlparse
import httplib


def get_code(url):
    x = urlparse(url)

    try:
        conn = httplib.HTTPConnection(x.netloc)
        conn.request("HEAD", x.path)
        return conn.getresponse().status
    except StandardError:
        return None


def get_element(doc, name):
    elements = manifest.getElementsByTagName(name)
    if len(elements) == 0:
        return None
    element = elements[0]
    return element    

def get_text(doc, name):
    element = get_element(doc, name)
    if element is None or len(element.childNodes)==0:
        return ''
    return element.childNodes[0].data

def report(name, rdict):
    sorted_report = sorted(rdict.iteritems(), key=operator.itemgetter(1))
    print
    print "=" * 5, name, "="*(40-len(name))
    for (value, count) in sorted_report:
        print value, count
    
def extract_items(s, split=False):
    authors = []
    if 'Maintained by' in s:
        i = s.index('Maintained by')
        s = s[:i] + s[i+1+len('Maintained by'):]
   
    for a in s.split(','):
        for b in a.split('and'):
            if split and '/' in b:
                b = b[:b.index('/')]
            authors.append(b.strip())
    return authors

#diff mainpage.dox ../pr2_sith/mainpage.dox | grep '^>'

authors = collections.defaultdict(list)
descriptions = collections.defaultdict(int)
briefs = collections.defaultdict(int)
reviews = collections.defaultdict(int)
licenses = collections.defaultdict(int)
urls = collections.defaultdict(int)
packages = []
stacks = []

if len(sys.argv)<=1 or '-h' in sys.argv:
    print "Need to specify a directory to search through as the first parameter"
    print "    [use the -web flag to ping the address "
    print "     specified in the URL tag to see if it exists ] " 
    exit(1)

check_urls = '-web' in sys.argv

for root, subFolders, files in os.walk(sys.argv[1]):
    if 'manifest.xml' in files:
        is_package = True
    elif 'stack.xml' in files:
        is_package = False
    else:
        continue

    package = os.path.basename(root)
    if is_package:
        manifest_xml = open("%s/manifest.xml"%root, 'r').read()
    else:
        manifest_xml = open("%s/stack.xml"%root, 'r').read()

    try:
        manifest = xml.dom.minidom.parseString(manifest_xml)
    except:
        continue

    node = {'name': package}

    author = get_text(manifest, 'author')
    for a_name in extract_items(author, True):
        authors[a_name].append(package)   
    node['author'] = author 

    description_xml = get_element(manifest, 'description')
    if not description_xml:
        node['description'] = None
        node['brief'] = None
    else:
        description = get_text(manifest, 'description').strip()
        brief = description_xml.getAttribute('brief').strip()
        node['description'] = 'minimal' if description==package else 'detailed'
        node['brief'] =       'minimal' if       brief==package else 'detailed'

    descriptions[ node['description'] ] += 1
    briefs[ node['brief'] ] += 1    

    review_xml = get_element(manifest, 'review')
    if review_xml is None:
        review = None
    else:
        review = review_xml.getAttribute('status')
    node[ 'review' ] = review
    reviews[review] += 1
     
    license = get_text(manifest, 'license')
    node[ 'license' ] = license
    for lic in extract_items(license):
        licenses[lic] += 1

    url = get_text(manifest, 'url')
    if url is not None:
        if check_urls:
            url = get_code(url)
        else:
            url = 'specified'
    node[ 'url' ] = url
    urls[url] += 1

    if is_package:
        packages.append(node)
    else:
        stacks.append(node)

lengths = collections.defaultdict(int)
for d in packages + stacks:
    for a,b in d.iteritems():
        if type(b)==type(u''):
            b = b.encode('ascii', 'replace')
        if len(str(b)) > lengths[a]:
            lengths[a] = len(str(b))
        if len(str(a)) > lengths[a]:
            lengths[a] = len(str(a))

fields = ['name', 'description', 'brief', 'license', 'url', 'review', 'author']

if len(stacks)>0:
    for field in fields:
        print ("%%-%ds"%lengths[field])%field,
    print

    for field in fields:
        print "=" * lengths[field],
    print

    for d in stacks:
        for field in fields:
            print ("%%-%ds"%lengths[field])%str(d[field]),
        print
    print

if len(packages)>0:
    for field in fields:
        print ("%%-%ds"%lengths[field])%field,
    print

    for field in fields:
        print "=" * lengths[field],
    print

    for d in packages:
        for field in fields:
            val = d[field]
            if type(val)==type(u''):
                val = val.encode('ascii', 'replace')
                print val, 
                n = lengths[field] - len(val)-1
                if n>0:
                    print " "*n,
            else:
                print ("%%-%ds"%lengths[field])%str(val),
        print

report('Descriptions', descriptions)
report('Brief Descriptions', briefs)
report('Reviews', reviews)
report('Licenses', licenses)
report('Urls', urls)
print
name = "Authors"
print "=" * 5, name, "="*(40-len(name))
for a,c in sorted(authors.items()):
    a = a.encode('ascii', 'replace')
    print "%s %4d"%(a.strip(),len(c))
    print '   ',
    for (i,b) in enumerate(c):
        print "%-30s"%b,
        if i%3==2:
            print '\n   ',
    print


