#!/usr/bin/python

# Frankenstein's Serval
#
# Copyright: Lars Baumgaertner (c) 2018


import socket
import struct
import threading
import time
import sys
import platform
import fcntl
import urllib2
import base64
import json
import hashlib
import subprocess

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

SERVALPORT = 4110
ANNOUNCEMENT_INTERVAL = 2
USERNAME = "pum"
PASSWORD = "pum123"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
 
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

please_run = True

myself_data = ["FrankenServal", platform.node(), get_ip_address("eth0"), "%s" % SERVALPORT]
mystate = ""

def get_my_bundlelist():
    request = urllib2.Request("http://127.0.0.1:4110/restful/rhizome/bundlelist.json")
    base64string = base64.b64encode('%s:%s' % (USERNAME, PASSWORD))
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(request)
    return json.loads(result.read())

def get_bundle_state():
    id_field_idx = 3
    version_field_idx = 4
    m = hashlib.md5()
    bundles = get_my_bundlelist()
    bids = []
    for i in bundles['rows']:
        bids.append(i[id_field_idx])
        bids.append(str(i[version_field_idx]))

    for i in sorted(bids):
        m.update(i)

    return m.hexdigest()

def announce_thread():
    global please_run
    global myself_data
    global mystate

    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    try:
        while please_run:
            #print get_bundle_state()    
            #print "announcing ", platform.node(), get_ip_address('eth0')
            mystate = get_bundle_state()
            sock.sendto(" ".join(myself_data)+ " " + mystate, (MCAST_GRP, MCAST_PORT))
            time.sleep(ANNOUNCEMENT_INTERVAL)
    except Exception as e:
        print "ending announce thread ", e
        please_run = False
        sys.exit(1)

thread = threading.Thread(target=announce_thread, args=())
try:
    thread.start()
except (KeyboardInterrupt, SystemExit):
    sys.exit()

try:
    while please_run:
        received = sock.recv(1024)
        if received.startswith("FrankenServal"):
            fields = received.split(" ")
            if len(fields) == 5 and fields[0:4] != myself_data:
                node_state = fields[4]
                if mystate == node_state:
                    #print "in sync"
                    pass
                else:
                    print "ANNOUNCE: %s %s %s %s - sync required" % (fields[1], fields[2], fields[3], fields[4])
                    subprocess.call("servald rhizome direct pull http://%s:%s" % (fields[2], fields[3]), shell=True)
except:
    print "ending receive thread "
    please_run = False
    sys.exit(1)
