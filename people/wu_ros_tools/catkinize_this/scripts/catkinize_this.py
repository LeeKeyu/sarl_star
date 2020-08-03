#!/usr/bin/python

import rospy
from xml.dom import minidom
import subprocess
import os.path

found = {}

def get_root(package):
    p = subprocess.Popen(['rospack', 'find', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip()

def is_catkinized(package, root=None):
    if package in found:
        return found[package]

    if root is None:
        root = get_root(package)
    if root=='':
        found[package] = None
        return None
    if os.path.exists('%s/package.xml'%root):
        found[package] = True
        return True
    elif os.path.exists('%s/manifest.xml'%root):
        found[package] = False
        return False
    else:
        found[package] = None
        return None

def get_links(name):
    if not os.path.exists(name):
        return []
    xmldoc = minidom.parse(name)
    if 'package.xml' in name:
        builds = xmldoc.getElementsByTagName('build_depend')
        runs = xmldoc.getElementsByTagName('run_depend')
        return [item.firstChild.nodeValue for item in builds+runs]
    elif 'manifest.xml' in name:
        itemlist = xmldoc.getElementsByTagName('depend') 
        return [item.attributes['package'].value for item in itemlist]
    else:
        None

def check_status(package, depth=0, dlimit=0):
    root = get_root(package)
    is_cat = is_catkinized(package, root)
    if is_cat:
        links = get_links('%s/package.xml'%root)
    elif is_cat==False:
        links = get_links('%s/manifest.xml'%root)
    else:
        return

    s = "%s%s"%(" "*depth, package)
    print s, " "*(50-len(s)), "CATKIN" if is_cat else "ROSPACK"

    if depth < dlimit:
        for p2 in links:
            if p2 not in found:
                check_status(p2, depth+1, dlimit)
        
    
import sys
limit = 0
for arg in sys.argv[1:]:
    if '--n' in arg:
        limit = int(arg[3:])
for arg in sys.argv[1:]:
    check_status(arg, dlimit=limit)

