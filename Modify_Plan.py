import requests
import json
import requests
import datetime
import logging
import xml.etree.cElementTree as ET
import time
import xml.dom.minidom

requests.packages.urllib3.disable_warnings()

usrname = ""
passwd = ""
# URL for  BigFix Environment
bigfixsaurl = "https://bfrootserver:8443/serverautomation"

# Function to get the automation plan XML 
def getplan(planid):
    query = '/getbesplan/master/' + str(planid)
    r = requests.get(bigfixsaurl + query, auth=(usrname, passwd), verify=False)
    return r.text
    print(r.text)

# Function to modify the automation plan xml 
def modifyplan(xml_data):
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Define the namespace
    namespace = {'ns': 'http://iemfsa.tivoli.ibm.com/REST'}
    ET.register_namespace('', 'http://iemfsa.tivoli.ibm.com/REST')

    # Modify the plan name to "Demo_AutomationPlan-Python"
    plan = root.find('{http://iemfsa.tivoli.ibm.com/REST}plan')
    if plan is not None:
        plan.set('name', 'Demo_AutomationPlan-Python')

    # Ensure that empty elements use both opening and closing tags
    for elem in root.iter():
        if elem.text is None:
            elem.text = ' '

    # Return the modified XML string, ensuring proper namespace usage
    return ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')

# Function to post the updated plan and create new plan 
def pplan(modified_xml):
    query = '/plan/master/'
    r = requests.put(bigfixsaurl + query, auth=(usrname, passwd), data=modified_xml, verify=False)
    return r.text
    print(r.text)


if __name__ == "__main__":
    xml_data = getplan(3573)
    print(xml_data)
    modified_xml = modifyplan(xml_data)
    print(modified_xml)
    plan_id = pplan(modified_xml)
    print(plan_id)
