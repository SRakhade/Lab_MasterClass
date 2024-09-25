import requests
import xml.etree.cElementTree as ET
requests.packages.urllib3.disable_warnings()

usrname = ""
passwd = ""
# URL for  BigFix Environment
bigfixsaurl = "https://bfrootserver:8443/serverautomation"

# Function to get Plan XML Structure
def getplan(planid):
    query = '/getbesplan/master/' + str(planid)
    response = requests.get(bigfixsaurl + query, auth=(usrname, passwd), verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    # Check and print the response
    if response.status_code == 200:
        return response.text
        print("Plan retrieved successful")
    else:
        print(f"Request failed with status code {response.status_code}")

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
    response = requests.put(bigfixsaurl + query, auth=(usrname, passwd), data=modified_xml, verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    # Check and print the response
    if response.status_code == 200:
        return response.text
        print("Plan modification successful")
    else:
        print(f"Request failed with status code {response.status_code}")


if __name__ == "__main__":
    xml_data = getplan(3573)
    print(xml_data)
    modified_xml = modifyplan(xml_data)
    print(modified_xml)
    plan_id = pplan(modified_xml, 3573)
    print(plan_id)
