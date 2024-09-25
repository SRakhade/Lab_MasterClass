import requests

usrname = ""
passwd = ""
# URL for  BigFix SA API Environment
bigfixsaurl = "https://bfrootserver:8443/serverautomation"

def create_plan(xml_input):
    query = '/plan/master/'
    # query = '/plan/{customsitename}/'
    response = requests.post(bigfixsaurl + query, auth=(usrname, passwd), data=xml_input, verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    # Check and print the response
    if response.status_code == 200:
        print("Request was successful!")
    else:
        print(f"Request failed with status code {response.status_code}")
        
if __name__ == "__main__":
    xml_input = '''<?xml version="1.0" encoding="UTF-8"?>
    <sa-rest xmlns="http://iemfsa.tivoli.ibm.com/REST" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <plan name="Demo_CreatePlan" domain="ALL CONTENT" pending-restart="PausePlan" version="2.0" source-plan-id="undefined" prefetch="false" source-plan-site-url="undefined">
        <description>API Create Plan</description>
        <category></category>
        <source></source>
        <source-severity></source-severity>
        <source-release-date>2024-09-24</source-release-date>
        <plan-steps>
            <step id="101">
                <fixlet fixlet-id="126" site-type="external" site-name="Server Automation"></fixlet>
                <!-- <targets><target-group name="myGroup" id="123"/><target-computer name="nameOnlyTarget"/><target-computer name="nameAndIDTarget" id="123"/></targets> -->
            </step>
        </plan-steps>
        <execution-order>
            <step id="101" depends="">
                <on-failure action="StopPlan" targets="IncludeFailed" threshold="0"></on-failure>
            </step>
        </execution-order>
        <plan-settings>
            <boolean-setting name="exclude-non-reporting-endpoint">
                <![CDATA[true]]>
            </boolean-setting>
        </plan-settings>
    </plan>
    </sa-rest>'''

  # Function to create a Plan 
    planid = create_plan(xml_input)
  # Print the Plan id post creation
    print(planid)
    
