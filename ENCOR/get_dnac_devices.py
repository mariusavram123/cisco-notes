#!/usr/bin/env python3

from Env_Lab import dnac
import json
import requests
import urllib3
from requests.auth import HTTPBasicAuth
from prettytable import PrettyTable

dnac_devices = PrettyTable(["Hostname", "Platform ID", "Software Type", "Software Version", "Series", 
                            "IP address", "Up Time"])

dnac_devices.padding_width = 1

# Silence the insecure warnings due to SSL Certificates

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "content-type": "application/json",
    "x-auth-token": ""
}


# Get token from DNAC api
def dnac_login(host, username, password):
    url = f"https://{host}/api/system/v1/auth/token"
    response = requests.request("POST", url, auth=HTTPBasicAuth(username, password),
                                headers=headers, verify=False)

    return response.json()["Token"]

# Get network devices information and add them to the table
def network_device_list(dnac, token):
    url = f"https://{dnac['host']}/api/v1/network-device"
    headers['x-auth-token'] = token
    response = requests.get(url, headers=headers, verify=False)
    data = response.json()
    # print(f"Data is:\n {data}")
    for item in data["response"]:
        dnac_devices.add_row([item['hostname'], item["platformId"], item["softwareType"], item["softwareVersion"], 
                             item["series"], item["managementIpAddress"], item["upTime"]])

login = dnac_login(dnac["host"], dnac["username"], dnac["password"])

network_device_list(dnac, login)

print(dnac_devices)