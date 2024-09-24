import requests

usrname = ""
passwd = ""
#URL for SandBox BigFix Environment
bigfixurl = "https://bfrootserver:52311/api"
bigfixsaurl = "https://bfrootserver:8443/serverautomation"

def monitorplanstaus(actionid):
    query = '/planaction/' + str(actionid)
    response = requests.get(bigfixsaurl + query, auth=(usrname, passwd), verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    # Check and print the response
    if response.status_code == 200:
        print("Request was successful!")
    else:
        print(f"Request failed with status code {response.status_code}")

def detailedplanstaus(actionid):
    query = '/besplanaction/' + str(actionid)
    response = requests.get(bigfixsaurl + query, auth=(usrname, passwd), verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    # Check and print the response
    if response.status_code == 200:
        print("Request was successful!")
    else:
        print(f"Request failed with status code {response.status_code}")

def bigfixactionstatus(actionid):

    relevance = '(name of computer of it, name of action of it, status of it, time issued of action of it) of results of bes actions whose (name of it contains %22IEMPlan 3610%22)'
    query = '/query?output=json&relevance='
    response = requests.get(bigfixurl + query + relevance, auth=(usrname, passwd), verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    # Check and print the response
    if response.status_code == 200:
        print("Request was successful!")
    else:
        print(f"Request failed with status code {response.status_code}")
if __name__ == "__main__":
    monitorplanstaus(3610), detailedplanstaus(3610), bigfixactionstatus(3610)
