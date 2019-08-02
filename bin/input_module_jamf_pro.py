
# encoding = utf-8

import os
import sys
import time
import datetime
import requests
import json
import splunklib.modularinput as splunk
from xml.etree import ElementTree

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    pass
    
def collect_events(helper, ew):
    name_of_the_modular_input = helper.get_arg('name_of_the_modular_input', None)
    url = helper.get_arg('jss_url', None)
    api_call = helper.get_arg('api_call', None)
    search_name = helper.get_arg('search_name', None)
    username = helper.get_arg('jss_username',None)
    password = helper.get_arg('jss_password',None)
    index = helper.get_arg('index','main')
    host = helper.get_arg('host','ip-10-202-14-66.ec2.splunkit.io')
    
    if api_call == "computer":
        jss_url = "%s/JSSResource/advancedcomputersearches/name/%s" % (url, search_name)
    elif api_call == "mobile_device":
        jss_url = "%s/JSSResource/advancedmobiledevicesearches/name/%s" % (url, search_name)
    else:
        helper.log_debug("api_call: %s not specified correctly" % api_call)
        return

    # Log that we are beginning to retrieve data.
    helper.log_debug("Started retrieving data for user %s" % username)
    response = requests.get(jss_url, auth=(username, password), headers={'accept': 'application/xml'})
    response.raise_for_status()
    #helper.log_debug(response.content)
    tree = ElementTree.fromstring(response.content)
    if api_call == "computer":
        computers_list = tree.find('computers')
        computers = computers_list.findall('computer')
        for computer in computers:
            event = helper.new_event(data=ElementTree.tostring(computer), index=index, host=host)
            # Tell the EventWriter to write this event
            #helper.log_debug(event)
            ew.write_event(event)
    elif api_call == "mobile_device":
        mobile_devices_list = tree.find('mobile_devices')
        mobile_devices = mobile_devices_list.findall('mobile_device')
        for mobile_device in mobile_devices:
            event = helper.new_event(data=ElementTree.tostring(mobile_device), index=index, host=host)
            ew.write_event(event)
