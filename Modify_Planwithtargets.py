import traceback
import datetime
import requests
from os import path
import urllib3
import time
import os
import xml.etree.cElementTree as ET
import xml.dom.minidom

requests.packages.urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

usrname = ""
passwd = ""

# URL for BigFix Environment
bigfixsaurl = "https://bfrootserver:8443/serverautomation"


def fetchplan(ap_id):
    query = '/plan/master/' + str(ap_id)
    response = requests.get(bigfixsaurl + query, auth=(usrname, passwd), verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    # Check and print the response
    if response.status_code == 200:
        return response.text
        print("Plan retrieved successful")
    else:
        print(f"Request failed with status code {response.status_code}")

def targetset(xml_string):
    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Define the namespace
    namespace = {'ns': 'http://iemfsa.tivoli.ibm.com/REST'}
    ET.register_namespace('', 'http://iemfsa.tivoli.ibm.com/REST')

    # Define List of computer names and its ID
    computers = [
        {"name": "bfvlcentapache", "id": "1614536093"}
    ]

    # Find all step elements and add the target-set element
    for step in root.findall('.//ns:step', namespace):
        # Check if the step already has a target-set to avoid duplication
        if step.find('.//ns:target-set', namespace) is None:
            # Create the target-set element
            target_set = ET.SubElement(step, "{http://iemfsa.tivoli.ibm.com/REST}target-set")
            # Create the computer element
            for computer in computers:
                computer_element = ET.SubElement(target_set, "{http://iemfsa.tivoli.ibm.com/REST}computer", {
                    "name": computer["name"],
                    "id": computer["id"]})
                computer_element.text = ' '

        # Update the schedule elements
        schedule = root.find('.//ns:schedule', namespace)
        if schedule is not None:
            # Replace StartDateTimeOffset with StartDateTime
            start_time_offset = schedule.find('ns:StartDateTimeOffset', namespace)
            if start_time_offset is not None:
                start_time_offset.text = 'P0DT0H0M0S'

            # Replace EndDateTimeOffset with EndDateTime
            end_time_offset = schedule.find('ns:EndDateTimeOffset', namespace)
            if end_time_offset is not None:
                end_time_offset.text = 'P0DT1H0M0S'

            # Update HasStartTime and HasEndTime to true
            has_start_time = schedule.find('ns:HasStartTime', namespace)
            if has_start_time is not None:
                has_start_time.text = 'false'

            has_end_time = schedule.find('ns:HasEndTime', namespace)
            if has_end_time is not None:
                has_end_time.text = 'true'

            Use_UTC = schedule.find('ns:UseUTCTime', namespace)
            if Use_UTC is not None:
                Use_UTC.text = 'true'

    # Convert the modified XML tree back to a string
    modified_xml_string = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    return modified_xml_string.decode('utf-8')


def createaction(xml_body, ap_id):
    query = '/plan/master/' + str(ap_id)
    r = requests.post(bigfixsaurl + query, auth=(usrname, passwd), data=xml_body, verify=False)

    if r.status_code == 200:
        print("Plan Deployed Successfully")
        print("Action id - " + str(r.text).strip())
        return str(r.text).strip()
    else:
        print(f"Request failed with status code {r.status_code}")

if __name__ == "__main__":
    xml_input = fetchplan(3573)
    modified_xml_output = targetset(xml_input)
    print(modified_xml_output)
    action_id = createaction(modified_xml_output, 3573)

