""" Set the environment information needed to access your lab

The provided sample code in this repository will reference this file to get 
the information needed to connect to your lab backend. You provide this info here once
and the scripts in this repository will access it as needed by the lab

...

"""

# User Input

# Please select the lab environment that you will be using today
#
#   sandbox - Cisco DevNet Always-On /Reserved sandboxes
#   express - Cisco DevNet Express Lab Backend
#   custom - Your own "Custom" Lab Backend

ENVIRONMENT_IN_USE = "sandbox"

# Set the 'Environment Variables' based on the lab environment in use

if ENVIRONMENT_IN_USE == "sandbox":
    dnac = {
        "host": "sandboxdnac.cisco.com",
        "port": 443,
        "username": "devnetuser",
        "password": "Cisco123!"
    }



