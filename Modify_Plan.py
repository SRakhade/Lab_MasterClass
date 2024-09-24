import requests
import xml.etree.cElementTree as ET

requests.packages.urllib3.disable_warnings()

# Define the namespaces (with a blank prefix for the default namespace)
# Define the namespaces with both the default namespace and xsi namespace
# NSMAP = {'': 'http://iemfsa.tivoli.ibm.com/REST', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

# Register namespaces globally for proper handling
# ET.register_namespace('', NSMAP[''])
# ET.register_namespace('xsi', NSMAP['xsi'])

usrname = "BFadmin"
passwd = "AB1234a!"
# URL for SandBox BigFix Environment
bigfixurl = "https://192.168.128.185:52311/api"
bigfixsaurl = "https://192.168.128.185:8443/serverautomation"

# Function to get Plan XML Structure
def getplan(planid):
    query = '/getbesplan/master/' + str(planid)
    r = requests.get(bigfixsaurl + query, auth=(usrname, passwd), verify=False)
    return r.text
    print(r.text)

# Modify the existing plan if considered as template
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

# Update the exisitng plan
def pplan(modified_xml, planid):
    query = '/plan/master/' + str(planid)
    r = requests.put(bigfixsaurl + query, auth=(usrname, passwd), data=modified_xml, verify=False)
    return r.text
    print(r.text)


if __name__ == "__main__":
    xml_data = getplan(3573)
    print(xml_data)
    modified_xml = modifyplan(xml_data)
    print(modified_xml)
    plan_id = pplan(modified_xml, 3573)
    print(plan_id)
