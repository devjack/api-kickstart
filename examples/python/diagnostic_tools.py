#! /usr/bin/python
# Very basic script demonstrating diagnostic tools functionality
#
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
"""
import requests, logging, json, sys
from http_calls import EdgeGridHttpCaller
from random import randint
from akamai.edgegrid import EdgeGridAuth
from config import EdgeGridConfig
from urlparse import urljoin
import urllib
session = requests.Session()
debug = False
section_name = "default"

# If all parameters are set already, use them.  Otherwise
# use the config
config = EdgeGridConfig({"verbose":debug},section_name)

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

# Request locations that support the diagnostic-tools
print
print "Requesting locations that support the diagnostic-tools API.\n"

location_result = httpCaller.getResult('/diagnostic-tools/v1/locations')

# Select a random location to host our request
location_count = len(location_result['locations'])

print "There are %s locations that can run dig in the Akamai Network" % location_count
rand_location = randint(0, location_count-1)
location = location_result['locations'][rand_location]
print "We will make our call from " + location + "\n"

# Request the dig request the {OPEN} Developer Site IP informantion
print "Running dig from " + location
dig_parameters = { "hostname":"developer.akamai.com", "location":location, "queryType":"A" }
dig_result = httpCaller.getResult("/diagnostic-tools/v1/dig",dig_parameters)

# Display the results from dig
print dig_result['dig']['result']
