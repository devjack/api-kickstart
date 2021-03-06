#! /usr/bin/python
""" Copyright 2015 Akamai Technologies, Inc. All Rights Reserved.
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.

 You may obtain a copy of the License at 

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.


Sample client for CCU
Note that in order for this to work you need to provision credentials
specifically for CCU - you cannot extend existing credentials to add
CCU as it's managed under "CCU" in the API credential system.

Configure->Organization->Manage APIs
Select "CCU APIs"
Create client collections/clients
Add authorization

Put the credentials in ~/.edgerc as demonstrated by api-kickstart/sample_edgerc
"""

import requests, logging, json
from http_calls import EdgeGridHttpCaller
from random import randint
from akamai.edgegrid import EdgeGridAuth
from config import EdgeGridConfig
from urlparse import urljoin
import urllib
import os
session = requests.Session()
debug = False
section_name = "ccu"


# If all parameters are set already, use them.  Otherwise
# use the config
config = EdgeGridConfig({"verbose":False},section_name)

if hasattr(config, "debug") or hasattr(config, "verbose"):
	debug = True


# Set the config options
session.auth = EdgeGridAuth(
            client_token=config.client_token,
            client_secret=config.client_secret,
            access_token=config.access_token
)

if hasattr(config, 'headers'):
	session.headers.update(config.headers)

baseurl = '%s://%s/' % ('https', config.host)
httpCaller = EdgeGridHttpCaller(session, debug, baseurl)


def getQueue():
	print
	purge_queue_result = httpCaller.getResult('/ccu/v2/queues/default')
	print "The queue currently has %s items in it" % int(purge_queue_result['queueLength'])

def checkProgress(resource):
  purge_queue_result =  httpCaller.getResult(resource)
  return purge_queue_result

def postPurgeRequest():
	purge_obj = {
			"objects" : [
				"https://developer.akamai.com/stuff/Akamai_Time_Reference/AkamaiTimeReference.html"
			]
		    }
	print "Adding %s to queue" % json.dumps(purge_obj)
	purge_post_result = httpCaller.postResult('/ccu/v2/queues/default', json.dumps(purge_obj))
	return purge_post_result

if __name__ == "__main__":
	Id = {}
	getQueue()
	purge_post_result = postPurgeRequest()
	
	check_result = checkProgress(purge_post_result["progressUri"])
	seconds_to_wait = check_result['pingAfterSeconds']
	print "You should wait %s seconds before checking queue again..." % seconds_to_wait
