## Foundational Network Programmability Concepts

1. Command-Line Interface (CLI)

2. Application Programming Interface (API)

3. Data Models and Supporting Protocols

4. Cisco DevNet

5. GitHub

6. Basic Python Concepts and Scripts

- Some of the ways the networks have been traditionally managed

- It also focuses on some of the most common network programmability concepts and programmatic methods of management

### Command-Line Interface

- There are many different ways to connect and manage a network

- The most commonly used method for the past 30 years has been by using the *command-line interface* (CLI)

- However, like almost everything else, the CLI has pros and cons

- Perhaps one of the most glaring and biggest flaws with using CLI to manage a network is misconfiguration

- Businesses often have frequent changes in their network environments, and some of the changes can be extremely complex

- When businesses have increased complexity in their networks, the cost of something failing can be very high due to the increased time it takes to troubleshoot the issues in a complex network

- Failure in a network, however, doesn't necessarily mean software or a hardware component is to blame

- A majority of network outages are caused by human beings

- Many outages occur because of misconfigurations due to lack of network understanding

- While not all outages and failures can be avoided, there are tools that can assist in reducing the number of outages that are caused by human error due to misconfigurations in the CLI

- Below we can see a brief list of common pros and cons associated with using the CLI

```
PROs                                                                        CONs

Well known and documented                                                   Difficult to scale

Commonly used method                                                        Large number of commands

Commands can be scripted                                                    Must know IOS command syntax

Syntax help available on each command                                       Executing commands can be slow

Connection to SSH can be encrypted (using SSH)                              Not intuitive

                                                                            Can execute only one command at a time

                                                                            CLI and commands can change between software versions and platforms

                                                                            Using the CLI can pose a security threat if using Telnet (plain text)
```

- Of course there are programatic ways of accomplishing the same configurations that are possible with the CLI

### Application Programming Interface

- Another very popular method with comunicating with and configuring a network is through the use of **application programming interfaces** (APIs)

- APIs are mechanisms used to communicate with applications and other software

- They are also used to communicate with various components of the network through software

- It is possible to use APIs to configure or monitor specific components of a network

- There are multiple different types of APIs

- Two most common APIs are the Northbound API and the Southbound API

![northbound-and-southbound-api](./northbound-and-southbound-api.png)

#### Northbound API

- Northbound APIs are often used to communicate from a network controller to it's management software

- For example, Cisco DNA Center has a software Graphical User Interface (GUI) that is used to manage the network controller

- Typically, when a network operator logs into a controller to manage the network, the information that is being passed from the management software is leveraging a Northbound REST-based API

- Best practices suggest that the traffic should be encrypted using TLS between the software and the controller

- Most types of APIs have the ability to use encryption to secure the data in flight

#### Southbound API

- If a network operator makes a change to a switch's configuration in the management software of the controller, these changes are then pushed down to the individual devices by using a Southbound API

- These devices can be routers, switches, or even wireless access points

- APIs interact with the components of a network through the use of a programmatic interface

#### Representational State Transfer (REST) APIs

- An API that uses REST is often referred to a RESTful API

- RESTful APIs use HTTP methods to gather and manipulate data

- Because there is a defined for how HTTP works, it offers a consistent way to interact with APIs from multiple vendors

- REST uses different HTTP functions to interact with the data

- Below are some of the most common HTTP functions and their associated use cases

```
HTTP Function                       Action                                                              Use Case

GET                                 Request data from a destination                                     Viewing a website

POST                                Submits data to a specific destination                              Submitting login credentials

PUT                                 Replaces data in a specific destination                             Updating an NTP server

PATCH                               Appends data to a specific destination                              Adding an NTP server

DELETE                              Removes data from a specific destination                            Removing an NTP server
```

- HTTP functions are similar to the functions that most applications or database use to store or alter data - whether the data is stored in a database or within the application

- These functions are called "CRUD" functions

- CRUD is an acronym that stands for CREATE, READ, UPDATE and DELETE

- For example, in a SQL database, the CRUD functions are used to interact with and manipulate the data stored in the database

- Below are listed the CRUD functions and their associated actions and use cases

```
CRUD Function                           Action                                                          Use Case

CREATE                                  Inserts data into a database or application                     Updating a customer's home address in a database

READ                                    Retrieves data from a database or application                   Pulling up a customer's home address from a database

UPDATE                                  Modifies or replaces data in a database or application          Changing a street address stored in a database

DELETE                                  Removes data from a database or application                     Removing a customer from a database
```

#### API Tools and Resources

- Whether you are trying to learn how APIs interact with applications or controllers, need to test code and outcomes, or want to become a full-time developer, one of the most important pieces of interacting with any software using APIs is testing

- Testing code helps ensure that developers are accomplishing the outcome that was intended when executing the code

- Below are covered some tools and resources related to using APIs and REST functions

- This information will help hone development skills in order to become a more efficient engineer with coding skills

#### Introduction to Postman

- Keep in mind that APIs are software interfaces into an application or controller

- Many APIs require authentication

- This means that such an API is considered just like any other device to which a user needs to authenticate to gain access to utilize the APIs

- A developer which is authenticated has access to making changes using the API, which can impact the application

- This means that if a REST API call is used to delete data, the data will be removed from the application or controller just as if user logged into the device via CLI and deleted it

- It is best practice to use a test lab or the Cisco DevNet sandbox while learning and practicing any of these concepts to avoid accidental impact to a production or lab environment

- Cisco DevNet is discussed later

- Postman is an application that makes it possible to interact with APIs using a console-based approach

- Postman allows for the use of various data types and formats to interact with REST-based APIs

- Below is shown the main Postman application dashboard

![postman-app-dashboard](./postman-app-dashboard.png)

- The Postman application has various sections that you can interact with

- The focus here is to use the Builder portion of the dashboard

- The following sections are the ones that require the most focus and atention:
    
    - History

    - Collections

    - New Tab

    - URL bar

- The History tab shows a list of all the recent API calls made using Postman

- Users have the option to clear their entire history at any time if they want to remove the complete list of API calls that have been made

- This is done by clicking the Clear All link at the top of the Collections window

- Users also have the ability to remove individual API calls from the history by simply hovering the mouse over the API call and clicking the trash can icon in the submenu that pops up

![postman-history](./postman-history.png)

- API calls can be stored in groups, called collections that are specific to a structure that fits the user's needs

- Collections can follow any naming convention and appear as a folder hierarchy

- For example, it's possible to have a collection called DNA-C to store all the Cisco DNA Center API calls

- Saving API calls to a collection helps during testing phases as the API calls can easily be found and sorted

- It is also possible to select a collection to be a favorite by clicking the star icon to the right of the collection name

- Below is shown a collection called TESTING added to favorites

![postman-testing-collection](./postman-testing-collection.png)

- Tabs provide another very convenient way to work with various API calls

- Each tab can have it's own API call and parameters that are completely independent of any other tab

- For example, a user can have one tab open with API calls that interact with the Cisco DNA Center controller and another tab open that is interacting with a completely different platform, such as a Cisco Nexus switch

- Each tab has it's own URL bar to be able to use a specific API

- Remember that an API call using REST is very much like an HTTP transaction

- Each API call in a RESTful API maps to an individual URL for a particular function

- This means every configuration change or poll to retrieve data a user makes in a REST API has a unique URL - whether it is GET, POST, PUT, PATCH or DELETE function

- Below are shown two different tabs in Postman

![multiple-tabs-postman](./multiple-tabs-postman.png)

![second-tab-postman](./second-tab-postman.png)

#### Data Formats - XML and JSON

- Now that the Postman dashboard has been shown, it's time to discuss two of the most common data formats that are used with APIs

- The first one is called **Extensible Markup Language (XML)** 

- This format may look familiar, as it is the same format that is commonly used when constructing web services

- XML is a tag-based language, and a tag must begin with a < simbol and end with a > simbol

- For example, a start tag of interface would be represented as <interface>

- Another XML rule is that a section that is started must also be ended

- So if a start tag is called <interface>, the section needs to be closed by using an accompanying end tag

- The end tag must be the same as the string of the start tag preceeded by /

- For example, the end tag for <interface> would be </interface>

- Inside the start tag and end tag, you can use different code and parameters

- Below is shown a snippet of XML output with both start and end tags as well as some configuration parameters

```xml
<users>
  <user>
    <name>root</name>
  </user>
  <user>
    <name>Jason</name>
  </user>
  <user>
    <name>Jamie</name>
  </user>
  <user>
    <name>Luke</name>
  </user>
</users>
```

- Notice that each section has a start tag and an end tag

- The data is structured so that it contains a section called "users", and within that section there are four individual users:

    - root

    - Jason

    - Jamie

    - Luke

- Before and after each username is the start tag <user> and the end tag </user>

- The output also contains start tag <name> and end tag </name>

- These tags are used for each user's name

- If it is necessary to create another section to add another user, you can simply follow the same logic as used in the previous example and build out more XML code

- Remember that one of the key features of XML is that it is readable by both humans and applications

- Indentation of XML sections is part of what makes it so readable

- For instance, if indentation is not used, it is harder to read and follow the sections in XML format

- Although indentation is not required, it is certainly a recommended best practice from a legibility perspective

- Below is shown an XML snippet listing available interfaces on a device

- In this case, the XML code snippet has no indentation, so you can see how much less readable the snippet is than the one from above

```xml
<interfaces>
<interface>
<name>GigabitEthernet1</name>
</interface>
<interface>
<name>GigabitEthernet11</name>
</interface>
<interface>
<name>Loopback100</name>
</interface>
<interface>
<name>Loopback101</name>
</interface>
</interfaces>
```

- The second data format that is important to cover is **JavaScript Object Notation (JSON)**

- Although JSON has not been around as long as XML, it is taking the industry by storm, and some say that it will soon replace XML

- The reason that this data format is gaining popularity, is that it can be argued that JSON is much easier to work with than XML

- It is simple to read and create, and the way the data is structured is much cleaner

- JSON stores all it's information in key/value pairs

- As with XML, JSON is easier to read if the data is indented

- However, even without indentation, JSON is extremely easy to read

- As the name suggests, JSON uses objects for it's format

- Each JSON object starts with a { and ends with a } (these are commonly referred to as curly braces)

- Below is shown how JSON can be used to represent the same username example shown for XML

- You can see that it has four separate key/value pairs, one for each user's name:

```json
{
    "user": "root",
    "father": "Jason",
    "mother": "Jamie",
    "friend": "Luke"
}
```

- In this JSON code snippet, you can see that the first key is user, and the value for that key is a unique username, root

- Now that the XML and JSON data formats have been explained, it is important to cycle back to actually using the REST API and the associated responses and outcomes of doing so

- First we need to look at HTTP response status codes

- Most Internet users have experienced the dreaded "404 Not Found" error when navigating to a website

- However, many users don't know what this error actually means

- Below are listed the most common HTTP status codes as well as the reasons users may receive each one

```
HTTP Status Code                            Result                                  Common Reason for Response Code

200                                         OK                                      Using GET or POST to exchange data with an API

201                                         Created                                 Creating resources by using a REST API call

400                                         Bad Request                             Request failed due to client-side issue

401                                         Unauthorized                            Client not authenticated to access site or API call

403                                         Forbidden                               Access not granted based on supplied credentials

404                                         Not Found                               Page at HTTP URL does not exist or is hidden
```

#### Cisco DNA Center APIs

- The Cisco DNA Center Controller expects all incoming data from the REST API to be in JSON format

- It is also important to note that the HTTP POST function is used to send the credentials to the Cisco DNA Center controller

- Cisco DNA Center uses basic authentication to pass a username and password to the Cisco DNA Center Token API to authenticate users

- This API is used to authenticate a user to the Cisco DNA Center Controller to make additional API calls

- Just as users do when logging in to a device via the CLI, if secured properly, they should be prompted for login credentials

- The same method applies when using an API to authenticate to software

- The key steps necessary to successfully set up the API call in Postman/Bruno are the following:

    1. In the URL bar, enter **https://sandboxdnac.cisco.com/api/system/v1/auth/token** to target the token API

    2. Select HTTP POST operation from the dropdown box

    3. Under the Authorization tab, ensure that type is set to Basic Auth

    4. Enter `devnetuser` as the username and `Cisco123!` as the password

    5. Select the Headers tab and enter Content-Type as the key

    6. Select application/json as value

    7. Click the Send button to pass the credentials to the Cisco DNA Center controller via the Token API

![getting-token-dnac](./getting-token-dnac.png)

- You need a token for any future API calls to the Cisco DNA Center controller

- When you are successfully authenticated to the Cisco DNA Center controller, you receive a token that contains a string that will be used for authenticating subsequent API calls

- Think of it as a hash that is generated from the supplied login credentials

- The token changes every time an authentication is made to the Cisco DNA Center controller

- It is important to remember that when you are authenticated, the token you receive is usable only for the current authenticated session to the controller

- If another user authenticates via the Token API, he or she will receive a unique token to be able to utilize the API based on his or her login credentials

![dnac-token-api-response](./dnac-token-api-response.png)

- You can see that the received status code is 200 OK from the Cisco DNA Center controller

- Based on the list from above, you can tell that the API call completed successfully

- In addition you can see how long it took to process the HTTP POST request: 641 ms

- Now we can take a look at some of the other available API calls

- The first API call we can see in this section is the Network Device API, which allows users to retrieve a list of devices that are currently in inventory that are being managed by the Cisco DNA Center Controller

- You need to prepare Postman/Bruno to use the token that was generated when you successfully authenticated to the contoller by following these steps:

    1. Copy the token you received earlier and click a new tab in Postman/Bruno

    2. In the URL bar enter **https://sandboxdnac.cisco.com/api/v1/network-device** in the target URL to target the Network Device API

    3. Select the HTTP GET operation from the dropdown box

    4. In the Headers tab enter Content-Type as the key

    5. Set the application/json as value

    6. Add another key and enter X-Auth-Token

    7. Paste the token as the value

    8. Click Send to pass the token to the Cisco DNA Center controller and perform an HTTP GET to retrieve a device inventory list using the Network Device API

![dna-center-network-device-api](./dna-center-api-get-device-information.png)

- The token is different from user to user. Remember that a token is unique to each authenticated user

- Response received from the DNA center Network Device API is JSON formated:

```json
{
  "response": [
    {
      "memorySize": "NA",
      "family": "Switches and Hubs",
      "lastUpdateTime": 1764536159105,
      "softwareType": "IOS-XE",
      "softwareVersion": "17.12.1prd9",
      "serialNumber": "CML12345",
      "inventoryStatusDetail": "<status><general code=\"SUCCESS\"/></status>",
      "collectionInterval": "Global Default",
      "dnsResolvedManagementAddress": "10.10.20.176",
      "lastManagedResyncReasons": "Periodic",
      "managementState": "Managed",
      "pendingSyncRequestsCount": "0",
      "reasonsForDeviceResync": "Periodic",
      "reasonsForPendingSyncRequests": "",
      "syncRequestedByApp": "",
      "upTime": "134 days, 8:31:33.00",
      "roleSource": "AUTO",
      "platformId": "C9KV-UADP-8P",
      "reachabilityFailureReason": "",
      "reachabilityStatus": "Reachable",
      "series": "Cisco Catalyst 9000 Series Virtual Switches",
      "snmpContact": "",
      "snmpLocation": "",
      "apManagerInterfaceIp": "",
      "bootDateTime": "2025-07-19 12:24:59",
      "collectionStatus": "Managed",
      "hostname": "sw2",
      "locationName": null,
      "managementIpAddress": "10.10.20.176",
      "interfaceCount": "0",
      "lastUpdated": "2025-11-30 20:55:59",
      "apEthernetMacAddress": null,
      "associatedWlcIp": "",
      "errorCode": null,
      "errorDescription": null,
      "lastDeviceResyncStartTime": "2025-11-30 20:55:24",
      "lineCardCount": "0",
      "lineCardId": "",
      "managedAtleastOnce": true,
      "tagCount": "0",
      "tunnelUdpPort": null,
      "uptimeSeconds": 11689767,
      "vendor": "Cisco",
      "waasDeviceMode": null,
      "type": "Cisco Catalyst 9000 UADP 8 Port Virtual Switch",
      "description": "Cisco IOS Software [Dublin], Catalyst L3 Switch Software (CAT9K_IOSXE), Version 17.12.1prd9, RELEASE SOFTWARE (fc1) Technical Support: http://www.cisco.com/techsupport Copyright (c) 1986-2023 by Cisco Systems, Inc. Compiled Tue 15-Aug-23 16:44 by mcpre",
      "deviceSupportLevel": "Supported",
      "macAddress": "52:54:00:07:29:d0",
      "location": null,
      "role": "ACCESS",
      "instanceUuid": "9e7d73bd-3dce-4581-830f-0e022e0c5e41",
      "instanceTenantId": "6737f2670eb9d40013137d83",
      "id": "9e7d73bd-3dce-4581-830f-0e022e0c5e41"
    }
  ],
  "version": "1.0"
}

(...)
```

- We can see that the response received from the Cisco DNA Center controller has a 200 OK status code, and you can see that the device inventory was received in JSON format

- By now, you should see how powerful APIs can be

- Within a few moments, users are able to gather a tremendous amount of information about the devices currently being managed by the Cisco DNA Center controller

- In the time it takes someone to log in to a device using the CLI and issue all the relevant `show` commands to gather data, an API call can be used to gather that data for the entire network

- APIs give network engineers time to do other things

- When using APIs, it is common to manipulate data using filters and offsets

- Say that a user wants to leverage the Network Device API to gather information only on the second device in the inventory

- This is where the API documentation becomes so valuable

- Most APIs have documentation that explains what they can be used to accomplish

- In Postman/Bruno it is possible to modify the Network Device API URL and add **?limit=1** to the end of the URL to show only a single device in the inventory

- It is also possible to add the **&offset=2** to the end of the URL to state that only the second device in the inventory should be shown

- These query parameters are part of the API and can be invoked using a client like Postman/Bruno as well

- Although it may sound confusing, the limit keyword simply states that a user only wants to retrieve one record from the inventory; the offset command states that the user wants that one record to be the second record in the inventory

- Below is shown how to adjust the Network Devices API URL in Bruno to show information on only the second device in the inventory

![get-only-second-device-from-inventory](./get-only-second-device-from-inventory.png)

- You can see from the response that the second device is consistent with the output that was initially shown in the first Network Device API call

- This device is a Cisco Catalyst 9000 switch with the MAC address "52:54:00:07:29:d0"

#### Cisco vManage APIs

- Here we will see the various APIs available in the Cisco SD-WAN (specifically, the vManage controller)

- We will also see how to interact with APIs programatically by using Postman/Bruno

- Leveraging Cisco SD-WAN APIs is a bit different from using the Cisco DNA Center APIs, but the two processes are quite similar

- As when using a Cisco DNA Center API, with a Cisco SD-WAN API you need to provide login credentials to the API in order to be able to utilize the API calls

- Some key pieces of information are necessary to successfully set up the API call in Bruno:

    - The URL bar must have the API call to target the Authentication API

    - The HTTP POST operation is used to send the username and password to Cisco vManage

    - The Header Content-Type must be application/x-www-form-urlencoded

    - The body must contain keys with the j_username devnetuser and thej_password Cisco123!

- The steps for connecting to APIs are different for Cisco SD-WAN than for Cisco DNA Center

- Detailed steps for setting up the Postman/Bruno environment for SD-WAN are available on [sd-wan-api-docs](https://developer.cisco.com/sdwan)

- The Cisco DNA Center Postman/Bruno environemnt setup are available at [DNA-center-API-docs](https://developer.cisco.com/learning/tracks/dnacenter-programmability)

- To set up a Postman/Bruno environment you can simply download steps into Postman from DevNet by going to https://developer.cisco.com/sdwan

- By doing so, you can quickly set up an environment that contains all the necessary authentication details and practice with the APIs without having to spend much time getting familiar with the details of Postman/Bruno

![bruno-environment-cisco-sd-wan](./bruno-environment-cisco-sd-wan.png)

- When the Postman/Bruno environment is set up, you click the Send button, the credentials are passed to vManage using the Authentication API

- The response you receive delivers something called a Java Session ID, which is displayed as JSESSIONID

- This is similar to the Cisco DNA Center token from above examples

- This session ID is passed to vManage for all future API calls from this user

- The HTTP status code 200 OK indicates a successful post to vManage with the proper credentials

- Now let's look at another API call that collects an inventory of fabric devices within Cisco vManage

- Using the HTTP GET operation, this API collects the requested information and displays it in Postman/Bruno

- Below you can see a lot from Cisco vManage's response

- You can see the URL for this API in the URL bar, and you can also see the HTTP GET request

- You can also see that the response is in JSON format, which makes the data easy to read and consume

![vmanage-api-request](./get-device-info-vmanage.png)

- If you scroll down in the response, you can see a list of devices under the "data" key received from the API call

- This list contains a series of information about each fabric device within Cisco vManage

- Some of the information is as follows:

    - Device ID

    - System IP

    - Host name

    - Reachability

    - Status

    - Device type

    - Site ID

![cisco-vmanage-api-response](./device-info-data-sdwan-api.png)

```json
"data": [
    {
      "deviceId": "10.10.1.1",
      "system-ip": "10.10.1.1",
      "host-name": "vmanage",
      "reachability": "reachable",
      "status": "normal",
      "personality": "vmanage",
      "device-type": "vmanage",
      "timezone": "UTC",
      "device-groups": [
        "No groups"
      ],
      "lastupdated": 1764523613453,
      "domain-id": "0",
      "board-serial": "F6963C4202C4B04C",
      "certificate-validity": "Valid",
      "max-controllers": "0",
      "uuid": "81ac6722-a226-4411-9d5d-45c0ca7d567b",
      "controlConnections": "5",
      "device-model": "vmanage",
      "version": "20.10.1",
      "connectedVManages": [
        "10.10.1.1"
      ],
      "site-id": "101",
      "latitude": "37.666684",
      "longitude": "-122.777023",
      "isDeviceGeoData": false,
      "platform": "x86_64",
      "uptime-date": 1764102540000,
      "statusOrder": 4,
      "device-os": "next",
      "validity": "valid",
      "state": "green",
      "state_description": "All daemons up",
      "model_sku": "None",
      "local-system-ip": "10.10.1.1",
      "total_cpu_count": "4",
      "testbed_mode": false,
      "layoutLevel": 1
    }
]
```

- As you can see, a simple API call has the power to gather a significant amount of information

- How the data is used, is up to the person making the API calls and collecting the data

- All the tools, processes and APIs can be leveraged to provide tremendous value to the business - from visibility into the environment to building relevant use cases to be consumed by the business or it's customers

### Data Models and Supporting Protocols

- Here we will see a high level overview of some of the most common data models and tools and how are they leveraged in a programmatic approach

    - Yet Another Next Generation (YANG) modeling language

    - Network Configuration Protocol (NETCONF)

    - RESTCONF

#### YANG Data Models

- SNMP is widely used for fault handling and monitoring

- However, it is not often used for configuration changes

- CLI scripting is used more often than other methods

- YANG data models are an alternative to SNMP MIBs and are becoming the standard for data definition languages

- YANG, which is defined in RFC 6020, uses data models

- Data models are used to describe whatever can be configured on a device, everything that can be monitored on a device, and all the administrative actions that can be executed on a device, such as resetting counters or rebooting the device

- This includes all the notifications that the device is capable of generating

- All these variables can be presented within a YANG model

- Data models are very powerful in that they can create a uniform way to describe data, which can be beneficial across vendors' platforms

- Data models allow network operators to configure, monitor, and interact with network devices holistically across the entire enterprise environment

- YANG models use a tree structure

- Within that structure, the models are similar in format to XML and are constructed in modules

- These modules are hierarchical in nature and contain all the different data and types that make up a YANG device model

- YANG models make a clear distinction between configuration data and state information

- The three structure represents how to reach a specific element of the model, and the elements can be either configurable or not configurable

- Each element has a defined type

- For example, an interface can be configured to be on or off

- However, the operational interface state cannot be changed; for example, if the options are only up or down, it is either up or down, and nothing else is possible

- Below is a simple YANG module taken from RFC 6020

```yang
container food {
    choose snack {
        case sports-arena {
            leaf pretzel {
                type empty;
            }
            lead popcorn {
                type empty;
            }
        }
        case late-night {
            leaf chocolate {
                type enumeration {
                    enum dark;
                    enum milk;
                    enum first-available;
                }
            }
        }
    }
}
```

- The output from above can be read as follows:

- There is food

- Of that food there is a choice of snack

- The snack choices are pretzels and popcorn

- If it is late at night, the snack choices are two different types of chocolate

- A choice must be made to have milk chocolate or dark chocolate, and if the consumer is in a hurry and does not want to wait, the consumer can have the first available chocolate

- Below is shown a network-oriented example that uses the same structure

```yang
list interface {
    key "name";
    leaf name {
        type string;
    }
    leaf speed {
        type enumeration {
            enum 10m,
            enum 100m;
            enum auto
        }
    }
    leaf observed-speed {
        type uint32;
        config false;
    }
}
```

- The YANG model from the above can be read as follows:

- There is a list of interfaces

- Of the available interfaces, there is a specific interface that has three configurable speeds

- Those speeds are 10 Mbps, 100 Mbps and auto, as listed in the leaf named speed

- The leaf named observed-speed cannot be configured due to the config false command

- This is because as the leaf is named, the speeds in the leaf are what was auto-detected (observed); hence, it is not a configurable leaf

- This is because it represents the auto-detected value on the interface, not a configurable value

#### NETCONF

- NETCONF, defined in RFC 4741 and RFC 6241, is an IETF standard protocol that uses YANG data models to communicate with the various devices on the network

- **NETCONF runs over SSH, TLS, and (although not common), Simple Object Access Protocol (SOAP)**

- Some of the key differences between SNMP and NETCONF are listed below

- One of the most important differences is that SNMP can't distinguish between configuration data and operational data, but NETCONF can

- Another key differentiator is that NETCONF uses paths to describe resources, whereas SNMP uses object identifiers (OIDs)

- A NETCONF path can be similar to interfaces/interface/eth0, which is much more descriptive than you would expect from SNMP

- The following is a list of some of the common use cases for NETCONF:

    - Collecting the status of specific fields

    - Changing the configuration of specific fields

    - Taking administrative actions

    - Sending event notifications

    - Backing up and restoring configurations

    - Testing configurations before finalizing the tranzaction

```
Feature                                 SNMP                                                NETCONF

Resources                               OIDs                                                Paths

Data models                             Defined in MIBs                                     YANG core models

Data modeling language                  SMI                                                 YANG

Management operations                   SNMP                                                NETCONF

Encoding                                BER                                                 Either XML or JSON

Transport stack                         UDP                                                 SSH/TCP
```

- Transactions are all of nothing

- There is no order of operations or sequencing within a transaction

- This means there is no part of the configuration that is done first; the configuration is deployed all at the same time

- Transactions are processed in the same order every time on every device

- Transactions, when deployed run in parallel state and do not have any impact on each other

- Parallel transactions touching different areas of the configuration on a device does not overwrite or interfere with each other

- They also do not impact each other if the same transaction is run against multiple devices

- Below is provided an example of a NETCONF element from RFC 4741

- This NETCONF output can be read as follows: 

- There is an XML list of users named users

- In that list, there are individual users named Dave, Rafael, and Dirk

```xml
<rpc-reply message-id="101">
    xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"
    <data>
        <top xmlns="http://example.com/schema/1.2/config">
            <users>
                <user>
                    <name>Dave</name>
                </user>
                <user>
                    <name>Rafael</name>
                </user>
                <user>
                    <name>Dirk</name>
                </user>
            </users>
        </top>
    </data>
</rpc-reply>
```

- An alternative way of looking at this type of NETCONF output is to simply look at it as though it were a shopping list

- Below is provided an example of the shopping list concept

- It can be read as follows:

- There is a group called beverages

- Of these beverages, there are soft drinks and tea

- The available soft drinks are cola and root beer

- Of the available tea, there is sweetened and unsweetened

```
Beverages
    Soft drinks
        Cola
        Root beer
    Tea
        Sweetened
        Unsweetened
```

- Below we can see how NETCONF uses YANG data models to interact with network devices and then talk back with the management applications

- The dotted lines shows how the devices talking back directly to the management applications, and the solid lines illustrates the NETCONF protocol talking between the management applications and the devices

![netconf-and-yang-models](./netconf-and-yang-models.png)

- NETCONF exchanges information called capabilities when the TCP connection has been made

- Capabilities tell the client what the device it's connected to can do

- Furthermore, other information can be gathered by using the common NETCONF operations shown below

```
NETCONF Operation                                               Description

<get>                                                           Requests running configuration and state information of the device

<get-config>                                                    Requests some or all of the configuration from the datastore

<edit-config>                                                   Edits a configuration datastore by using CRUD operations

<copy-config>                                                   Copies the configuration to another datastore

<delete-config>                                                 Deletes the configuration
```

- Information and configurations are stored in datastores

- Datastores can be manipulated by using NETCONF operations listed above

- NETCONF uses Remote Procedure Call (RPC) messages in XML format to send the information between hosts

- Now that we've looked at the basics of NETCONF and XML, let's examine some actual examples of a NETCONF RPC message

- Below is shown an example of an OSPF NETCONF RPC message that provides the OSPF routing configuration of an IOS XE device

```xml
<rpc-reply message-id="urn:uuid:0e2c04cf-9119-4e6a-8c05-238ee7f25208"
xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:
xml:ns:netconf:base:1.0">
  <data>
    <native xmlns="http://cisco.com/ns/yang/ned/ios">
      <router>
        <ospf>
          <id>100</id>
          <redistribute>
            <connected>
                <redist-options>
                    <subnets/>
                </redist-options>
            </connected>
          </redistribute>
          <network>
            <ip>10.0.0.0</ip>
            <mask>0.0.255.355</mask>
            <area>0</area>
          </network>
          <network>
            <ip>20.20.0.0</ip>
            <mask>0.0.255.255</mask>
            <area>0</area>
          </network>
          <network>
            <ip>100.100.0.0</ip>
            <mask>0.0.255.255</mask>
            <area>0</area>
          </network>
        </ospf>
      </router>
    </native>
  </data>
</rpc-reply>
```

- The same OSPF router configuration that would be seen in the command-line interface of a Cisco router can be seen using NETCONF

- The data is just structured in XML format rather than what users are accustomed to seeing in the CLI

- It is easy to read the output in these examples because of how legible XML is

- Below is a configuration save example of a network device by leveraging NETCONF

```xml
<?xml version="1.0" encoding="utf-8"?>
<rpc xmlns="urn:ietf:parms:xml:ns:netconf:base:1.0" message-id="">
    <cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>
</rpc>
```

- NETCONF/YANG configuration Cisco CSR1000V router - need ssh to be enabled:

```
conf t
 netconf-yang
 username marius privilege 15 algorithm-type scrypt secret <secret>
 aaa new-model
 aaa authorization exec default local
 ip domain name TEST
 crypto key generate rsa
 ip ssh version 2
```

- Additional configuration - enable SNMP for netconf yang process:

```
conf t
 snmp-server community TEST RW
 snmp-server trap link ietf
 snmp-server enable traps snmp authentication linkdown linkup
 snmp-server enable traps syslog
 snmp-server manager
 netconf-yang cisco-ia snmp-community-string TEST
```

- Enable logging notifications for NETCONF application

```
conf t
 logging history debugging
 logging snmp-trap emergencies
 logging snmp-trap alerts
 logging snmp-trap critical
 logging snmp-trap errors
 logging snmp-trap warnings
 logging snmp-trap notifications
 logging snmp-trap informational
 logging snmp-trap debugging
```

- Configure netconf-yang traps

```
conf t
 netconf-yang cisco-ia snmp-trap-control trap-list 10.3.6.1.6.3.1.1.5.3 ! linkdown trap
 netconf-yang cisco-ia snmp-trap-control trap-list 10.3.6.1.6.3.1.1.5.4 ! linkup trap
 netconf-yang cisco-ia snmp-trap-control trap-list 10.3.6.1.4.1.9.9.41.2.0.1 ! notification trap
```

- Verification:

```
CSR1(config)#do sh platform software yang-management process             
confd            : Running    
nesd             : Running    
syncfd           : Running    
ncsshd           : Running    
dmiauthd         : Running    
nginx            : Running    
ndbmand          : Running    
pubd             : Running    


```

- SSH using NETCONF to the router:

```
root@83a1160f2ec7:/# ssh marius@10.12.1.0 -p 830 netconf
The authenticity of host '[10.12.1.0]:830 ([10.12.1.0]:830)' can't be established.
RSA key fingerprint is SHA256:aQK6P6/OH2qmUAP7geSFjiMKklXbBG7YGMxA1fDdXUc.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[10.12.1.0]:830' (RSA) to the list of known hosts.
marius@10.12.1.0's password: 
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<capabilities>
<capability>urn:ietf:params:netconf:base:1.0</capability>
<capability>urn:ietf:params:netconf:base:1.1</capability>
<capability>urn:ietf:params:netconf:capability:writable-running:1.0</capability>
<capability>urn:ietf:params:netconf:capability:rollback-on-error:1.0</capability>
<capability>urn:ietf:params:netconf:capability:validate:1.0</capability>
<capability>urn:ietf:params:netconf:capability:validate:1.1</capability>
<capability>urn:ietf:params:netconf:capability:xpath:1.0</capability>
<capability>urn:ietf:params:netconf:capability:notification:1.0</capability>
<capability>urn:ietf:params:netconf:capability:interleave:1.0</capability>
<capability>urn:ietf:params:netconf:capability:with-defaults:1.0?basic-mode=explicit&amp;also-supported=report-all-tagged,report-all</capability>
<capability>urn:ietf:params:netconf:capability:yang-library:1.0?revision=2016-06-21&amp;module-set-id=9a21a4b66ce28c110b54d5a052486d1f</capability>
<capability>http://tail-f.com/ns/netconf/actions/1.0</capability>
<capability>http://cisco.com/ns/cisco-xe-ietf-ip-deviation?module=cisco-xe-ietf-ip-deviation&amp;revision=2016-08-10</capability>
<capability>http://cisco.com/ns/cisco-xe-ietf-ipv4-unicast-routing-deviation?module=cisco-xe-ietf-ipv4-unicast-routing-deviation&amp;revision=2015-09-11</capability>
<capability>http://cisco.com/ns/cisco-xe-ietf-ipv6-unicast-routing-deviation?module=cisco-xe-ietf-ipv6-unicast-routing-deviation&amp;revision=2015-09-11</capability>
<capability>http://cisco.com/ns/cisco-xe-ietf-ospf-deviation?module=cisco-xe-ietf-ospf-deviation&amp;revision=2018-02-09</capability>
<capability>http://cisco.com/ns/cisco-xe-ietf-routing-deviation?module=cisco-xe-ietf-routing-deviation&amp;revision=2016-07-09</capability>
<capability>http://cisco.com/ns/cisco-xe-openconfig-acl-deviation?module=cisco-xe-openconfig-acl-deviation&amp;revision=2017-08-25</capability>
<capability>http://cisco.com/ns/cisco-xe-openconfig-aft-deviation?module=cisco-xe-openconfig-aft-deviation&amp;revision=2018-12-05</capability>
<capability>http://cisco.com/ns/cisco-xe-openconfig-isis-deviation?module=cisco-xe-openconfig-isis-deviation&amp;revision=2018-12-05</capability>
<capability>http://cisco.com/ns/cisco-xe-openconfig-lldp-deviation?module=cisco-xe-openconfig-lldp-deviation&amp;revision=2018-07-25</capability>
<capability>http://cisco.com/ns/cisco-xe-openconfig-mpls-deviation?module=cisco-xe-openconfig-mpls-deviation&amp;revision=2019-06-27</capability>
<capability>http://cisco.com/ns/cisco-xe-openconfig-segment-routing-deviation?module=cisco-xe-openconfig-segment-routing-deviation&amp;revision=2018-12-05</capability>
<capability>http://cisco.com/ns/cisco-xe-routing-openconfig-system-management-deviation?module=cisco-xe-routing-openconfig-system-management-deviation&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/mpls-static/devs?module=common-mpls-static-devs&amp;revision=2015-09-11</capability>
<capability>http://cisco.com/ns/nvo/devs?module=nvo-devs&amp;revision=2015-09-11</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-aaa?module=Cisco-IOS-XE-aaa&amp;revision=2020-07-05</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-aaa-oper?module=Cisco-IOS-XE-aaa-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-acl?module=Cisco-IOS-XE-acl&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-acl-oper?module=Cisco-IOS-XE-acl-oper&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-app-hosting-cfg?module=Cisco-IOS-XE-app-hosting-cfg&amp;revision=2020-07-03</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-app-hosting-oper?module=Cisco-IOS-XE-app-hosting-oper&amp;revision=2020-07-03</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-arp?module=Cisco-IOS-XE-arp&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-arp-oper?module=Cisco-IOS-XE-arp-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-atm?module=Cisco-IOS-XE-atm&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-bba-group?module=Cisco-IOS-XE-bba-group&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-bfd?module=Cisco-IOS-XE-bfd&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-bfd-oper?module=Cisco-IOS-XE-bfd-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-bgp?module=Cisco-IOS-XE-bgp&amp;revision=2020-07-04</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-bgp-common-oper?module=Cisco-IOS-XE-bgp-common-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-bgp-oper?module=Cisco-IOS-XE-bgp-oper&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-bgp-route-oper?module=Cisco-IOS-XE-bgp-route-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-bridge-domain?module=Cisco-IOS-XE-bridge-domain&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-call-home?module=Cisco-IOS-XE-call-home&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-card?module=Cisco-IOS-XE-card&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-cdp?module=Cisco-IOS-XE-cdp&amp;revision=2020-07-01&amp;deviations=Cisco-IOS-XE-cdp-deviation</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-deviation?module=Cisco-IOS-XE-cdp-deviation&amp;revision=2019-07-23</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper?module=Cisco-IOS-XE-cdp-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-cef?module=Cisco-IOS-XE-cef&amp;revision=2019-11-01&amp;features=asr1k-dpi</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-cellular?module=Cisco-IOS-XE-cellular&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-cellular-rpc?module=Cisco-IOS-XE-cellular-rpc&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-cellwan-oper?module=Cisco-IOS-XE-cellwan-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-cfm-oper?module=Cisco-IOS-XE-cfm-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-checkpoint-archive-oper?module=Cisco-IOS-XE-checkpoint-archive-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-common-types?module=Cisco-IOS-XE-common-types&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-controller?module=Cisco-IOS-XE-controller&amp;revision=2020-07-02</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-controller-shdsl-common?module=Cisco-IOS-XE-controller-shdsl-common&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-controller-shdsl-events?module=Cisco-IOS-XE-controller-shdsl-events&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-controller-shdsl-oper?module=Cisco-IOS-XE-controller-shdsl-oper&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-controller-vdsl-oper?module=Cisco-IOS-XE-controller-vdsl-oper&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-crypto?module=Cisco-IOS-XE-crypto&amp;revision=2020-07-02</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-crypto-oper?module=Cisco-IOS-XE-crypto-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-crypto-pki-events?module=Cisco-IOS-XE-crypto-pki-events&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-crypto-pki-oper?module=Cisco-IOS-XE-crypto-pki-oper&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-cts?module=Cisco-IOS-XE-cts&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-cts-rpc?module=Cisco-IOS-XE-cts-rpc&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-dapr?module=Cisco-IOS-XE-dapr&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper?module=Cisco-IOS-XE-device-hardware-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-device-tracking?module=Cisco-IOS-XE-device-tracking&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp?module=Cisco-IOS-XE-dhcp&amp;revision=2020-07-04</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp-oper?module=Cisco-IOS-XE-dhcp-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-diagnostics?module=Cisco-IOS-XE-diagnostics&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-dialer?module=Cisco-IOS-XE-dialer&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-dialer-deviation?module=Cisco-IOS-XE-dialer-deviation&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-dot1x?module=Cisco-IOS-XE-dot1x&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-eem?module=Cisco-IOS-XE-eem&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-efp-oper?module=Cisco-IOS-XE-efp-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-eigrp?module=Cisco-IOS-XE-eigrp&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-eigrp-oper?module=Cisco-IOS-XE-eigrp-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-environment-oper?module=Cisco-IOS-XE-environment-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-eta?module=Cisco-IOS-XE-eta&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet?module=Cisco-IOS-XE-ethernet&amp;revision=2020-07-02</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-event-history-types?module=Cisco-IOS-XE-event-history-types&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ezpm?module=Cisco-IOS-XE-ezpm&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-features?module=Cisco-IOS-XE-features&amp;revision=2020-07-02&amp;features=virtual-template,routing-platform,punt-num,parameter-map,multilink,macsec-common,l2vpn,l2,ezpm,eth-evc,esmc,efp,dhcp-border-relay,crypto</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-fib-oper?module=Cisco-IOS-XE-fib-oper&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-flow?module=Cisco-IOS-XE-flow&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-flow-monitor-oper?module=Cisco-IOS-XE-flow-monitor-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-flow-rpc?module=Cisco-IOS-XE-flow-rpc&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-fw-oper?module=Cisco-IOS-XE-fw-oper&amp;revision=2020-07-02</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-gir-oper?module=Cisco-IOS-XE-gir-oper&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-gnss-oper?module=Cisco-IOS-XE-gnss-oper&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-http?module=Cisco-IOS-XE-http&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-icmp?module=Cisco-IOS-XE-icmp&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-igmp?module=Cisco-IOS-XE-igmp&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-im-events-oper?module=Cisco-IOS-XE-im-events-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-install-events?module=Cisco-IOS-XE-install-events&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-install-oper?module=Cisco-IOS-XE-install-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-install-rpc?module=Cisco-IOS-XE-install-rpc&amp;revision=2020-07-02</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-interface-common?module=Cisco-IOS-XE-interface-common&amp;revision=2020-07-05</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper?module=Cisco-IOS-XE-interfaces-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ios-common-oper?module=Cisco-IOS-XE-ios-common-oper&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ios-events-oper?module=Cisco-IOS-XE-ios-events-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ip-sla-events?module=Cisco-IOS-XE-ip-sla-events&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ip-sla-oper?module=Cisco-IOS-XE-ip-sla-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ipmux?module=Cisco-IOS-XE-ipmux&amp;revision=2019-10-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ipv6-oper?module=Cisco-IOS-XE-ipv6-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-isg?module=Cisco-IOS-XE-isg&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-isis?module=Cisco-IOS-XE-isis&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-iwanfabric?module=Cisco-IOS-XE-iwanfabric&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-l2tp-oper?module=Cisco-IOS-XE-l2tp-oper&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-l2vpn?module=Cisco-IOS-XE-l2vpn&amp;revision=2020-07-02</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-l3vpn?module=Cisco-IOS-XE-l3vpn&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-lisp?module=Cisco-IOS-XE-lisp&amp;revision=2020-07-04</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-lisp-oper?module=Cisco-IOS-XE-lisp-oper&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-lldp?module=Cisco-IOS-XE-lldp&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-lldp-oper?module=Cisco-IOS-XE-lldp-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mdns-gateway?module=Cisco-IOS-XE-mdns-gateway&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg?module=Cisco-IOS-XE-mdt-cfg&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-common-defs?module=Cisco-IOS-XE-mdt-common-defs&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper?module=Cisco-IOS-XE-mdt-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper-v2?module=Cisco-IOS-XE-mdt-oper-v2&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper?module=Cisco-IOS-XE-memory-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mld?module=Cisco-IOS-XE-mld&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mlppp-oper?module=Cisco-IOS-XE-mlppp-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mobileip?module=Cisco-IOS-XE-mobileip&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mpls?module=Cisco-IOS-XE-mpls&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mpls-forwarding-oper?module=Cisco-IOS-XE-mpls-forwarding-oper&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mpls-ldp-oper?module=Cisco-IOS-XE-mpls-ldp-oper&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-mroute-oper?module=Cisco-IOS-XE-mroute-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-multicast?module=Cisco-IOS-XE-multicast&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-nam?module=Cisco-IOS-XE-nam&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-nat?module=Cisco-IOS-XE-nat&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-nat-oper?module=Cisco-IOS-XE-nat-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-native?module=Cisco-IOS-XE-native&amp;revision=2020-07-04&amp;deviations=Cisco-IOS-XE-cdp-deviation,Cisco-IOS-XE-dialer-deviation,Cisco-IOS-XE-nd-deviation,Cisco-IOS-XE-policy-deviation,Cisco-IOS-XE-sanet-deviation</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-nbar?module=Cisco-IOS-XE-nbar&amp;revision=2020-09-28</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ncch-cfg?module=Cisco-IOS-XE-ncch-cfg&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ncch-oper?module=Cisco-IOS-XE-ncch-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-nd?module=Cisco-IOS-XE-nd&amp;revision=2020-07-01&amp;deviations=Cisco-IOS-XE-nd-deviation</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-nd-deviation.yang?module=Cisco-IOS-XE-nd-deviation</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-nhrp?module=Cisco-IOS-XE-nhrp&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ntp?module=Cisco-IOS-XE-ntp&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ntp-oper?module=Cisco-IOS-XE-ntp-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-object-group?module=Cisco-IOS-XE-object-group&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ospf?module=Cisco-IOS-XE-ospf&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ospf-common?module=Cisco-IOS-XE-ospf-common&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ospf-events?module=Cisco-IOS-XE-ospf-events&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ospf-oper?module=Cisco-IOS-XE-ospf-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ospfv3?module=Cisco-IOS-XE-ospfv3&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-otv?module=Cisco-IOS-XE-otv&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-pathmgr?module=Cisco-IOS-XE-pathmgr&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-perf-measure?module=Cisco-IOS-XE-perf-measure&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-perf-measure-events?module=Cisco-IOS-XE-perf-measure-events&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-perf-measure-oper?module=Cisco-IOS-XE-perf-measure-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-pfr?module=Cisco-IOS-XE-pfr&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-pim-oper?module=Cisco-IOS-XE-pim-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-platform?module=Cisco-IOS-XE-platform&amp;revision=2020-07-02</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-platform-oper?module=Cisco-IOS-XE-platform-oper&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-platform-software-oper?module=Cisco-IOS-XE-platform-software-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-pnp?module=Cisco-IOS-XE-pnp&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-policy?module=Cisco-IOS-XE-policy&amp;revision=2020-07-03&amp;deviations=Cisco-IOS-XE-policy-deviation</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-policy-deviation?module=Cisco-IOS-XE-policy-deviation&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ppp?module=Cisco-IOS-XE-ppp&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-ppp-oper?module=Cisco-IOS-XE-ppp-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-pppoe?module=Cisco-IOS-XE-pppoe&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-process-cpu-oper?module=Cisco-IOS-XE-process-cpu-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-process-memory-oper?module=Cisco-IOS-XE-process-memory-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-qfp-classification-oper?module=Cisco-IOS-XE-qfp-classification-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-qfp-resource-utilization-oper?module=Cisco-IOS-XE-qfp-resource-utilization-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-qfp-stats?module=Cisco-IOS-XE-qfp-stats&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-qfp-stats-oper?module=Cisco-IOS-XE-qfp-stats-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-qos?module=Cisco-IOS-XE-qos&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-rip?module=Cisco-IOS-XE-rip&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-rmi-dad?module=Cisco-IOS-XE-rmi-dad&amp;revision=2020-07-02</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-route-map?module=Cisco-IOS-XE-route-map&amp;revision=2020-07-05</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-rpc?module=Cisco-IOS-XE-rpc&amp;revision=2020-07-02</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-rsvp?module=Cisco-IOS-XE-rsvp&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-sanet?module=Cisco-IOS-XE-sanet&amp;revision=2020-07-01&amp;deviations=Cisco-IOS-XE-sanet-deviation</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-sanet-deviation?module=Cisco-IOS-XE-sanet-deviation&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-sd-vxlan-oper?module=Cisco-IOS-XE-sd-vxlan-oper&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-segment-routing?module=Cisco-IOS-XE-segment-routing&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-service-discovery?module=Cisco-IOS-XE-service-discovery&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-service-insertion?module=Cisco-IOS-XE-service-insertion&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-service-routing?module=Cisco-IOS-XE-service-routing&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-site-manager?module=Cisco-IOS-XE-site-manager&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-sla?module=Cisco-IOS-XE-sla&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-sm-enum-types?module=Cisco-IOS-XE-sm-enum-types&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-sm-events-oper?module=Cisco-IOS-XE-sm-events-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-snmp?module=Cisco-IOS-XE-snmp&amp;revision=2020-07-02</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-spanning-tree?module=Cisco-IOS-XE-spanning-tree&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-switch?module=Cisco-IOS-XE-switch&amp;revision=2020-07-06</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-track?module=Cisco-IOS-XE-track&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-trustsec-oper?module=Cisco-IOS-XE-trustsec-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-tunnel?module=Cisco-IOS-XE-tunnel&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-tunnel-oper?module=Cisco-IOS-XE-tunnel-oper&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-tunnel-types?module=Cisco-IOS-XE-tunnel-types&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-types?module=Cisco-IOS-XE-types&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-umbrella?module=Cisco-IOS-XE-umbrella&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-umbrella-oper?module=Cisco-IOS-XE-umbrella-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-umbrella-oper-dp?module=Cisco-IOS-XE-umbrella-oper-dp&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-umbrella-rpc?module=Cisco-IOS-XE-umbrella-rpc&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-utd?module=Cisco-IOS-XE-utd&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-utd-common-oper?module=Cisco-IOS-XE-utd-common-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-utd-oper?module=Cisco-IOS-XE-utd-oper&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-utd-rpc?module=Cisco-IOS-XE-utd-rpc&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-vlan?module=Cisco-IOS-XE-vlan&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-vpdn?module=Cisco-IOS-XE-vpdn&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-vrf-oper?module=Cisco-IOS-XE-vrf-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-vrrp?module=Cisco-IOS-XE-vrrp&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-vrrp-oper?module=Cisco-IOS-XE-vrrp-oper&amp;revision=2019-05-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-vservice?module=Cisco-IOS-XE-vservice&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-vtp?module=Cisco-IOS-XE-vtp&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-vxlan?module=Cisco-IOS-XE-vxlan&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-wccp?module=Cisco-IOS-XE-wccp&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-wsma?module=Cisco-IOS-XE-wsma&amp;revision=2019-07-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-yang-interfaces-cfg?module=Cisco-IOS-XE-yang-interfaces-cfg&amp;revision=2019-05-21</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-zone?module=Cisco-IOS-XE-zone&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/Cisco-IOS-XE-zone-rpc?module=Cisco-IOS-XE-zone-rpc&amp;revision=2019-11-01</capability>
<capability>http://cisco.com/ns/yang/cisco-semver?module=cisco-semver&amp;revision=2019-03-20</capability>
<capability>http://cisco.com/ns/yang/cisco-smart-license?module=cisco-smart-license&amp;revision=2020-07-01</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-bgp-policy-deviation?module=cisco-xe-openconfig-bgp-policy-deviation&amp;revision=2017-07-24</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-ietf-event-notifications-deviation?module=cisco-xe-ietf-event-notifications-deviation&amp;revision=2018-12-03</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-ietf-yang-push-deviation?module=cisco-xe-ietf-yang-push-deviation&amp;revision=2018-12-03</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-openconfig-acl-ext?module=cisco-xe-openconfig-acl-ext&amp;revision=2017-03-30</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-openconfig-bgp-deviation?module=cisco-xe-openconfig-bgp-deviation&amp;revision=2018-05-21</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-openconfig-if-ethernet-ext?module=cisco-xe-openconfig-if-ethernet-ext&amp;revision=2017-10-30</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-openconfig-interfaces-ext?module=cisco-xe-openconfig-interfaces-ext&amp;revision=2018-07-14</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-openconfig-network-instance-deviation?module=cisco-xe-openconfig-network-instance-deviation&amp;revision=2017-02-14</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-openconfig-rib-bgp-ext?module=cisco-xe-openconfig-rib-bgp-ext&amp;revision=2016-11-30</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-openconfig-system-ext?module=cisco-xe-openconfig-system-ext&amp;revision=2018-03-21</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-routing-openconfig-vlan-deviation?module=cisco-xe-routing-openconfig-vlan-deviation&amp;revision=2018-12-12</capability>
<capability>http://cisco.com/ns/yang/cisco-xe-routing-policy-deviation?module=cisco-xe-openconfig-routing-policy-deviation&amp;revision=2017-03-30</capability>
<capability>http://cisco.com/ns/yang/ios-xe/template?module=Cisco-IOS-XE-template&amp;revision=2020-07-02</capability>
<capability>http://cisco.com/yang/cisco-ia?module=cisco-ia&amp;revision=2020-03-01</capability>
<capability>http://cisco.com/yang/cisco-self-mgmt?module=cisco-self-mgmt&amp;revision=2019-07-01</capability>
<capability>http://openconfig.net/yang/aaa?module=openconfig-aaa&amp;revision=2017-09-18</capability>
<capability>http://openconfig.net/yang/aaa/types?module=openconfig-aaa-types&amp;revision=2017-09-18</capability>
<capability>http://openconfig.net/yang/acl?module=openconfig-acl&amp;revision=2017-05-26&amp;deviations=cisco-xe-openconfig-acl-deviation</capability>
<capability>http://openconfig.net/yang/aft?module=openconfig-aft&amp;revision=2017-01-13</capability>
<capability>http://openconfig.net/yang/alarms?module=openconfig-alarms&amp;revision=2017-08-24</capability>
<capability>http://openconfig.net/yang/alarms/types?module=openconfig-alarm-types&amp;revision=2018-11-21</capability>
<capability>http://openconfig.net/yang/bgp?module=openconfig-bgp&amp;revision=2016-06-21</capability>
<capability>http://openconfig.net/yang/bgp-policy?module=openconfig-bgp-policy&amp;revision=2016-06-21&amp;deviations=cisco-xe-openconfig-bgp-policy-deviation</capability>
<capability>http://openconfig.net/yang/bgp-types?module=openconfig-bgp-types&amp;revision=2016-06-21</capability>
<capability>http://openconfig.net/yang/cisco-xe-openconfig-if-ip-deviation?module=cisco-xe-openconfig-if-ip-deviation&amp;revision=2017-03-04</capability>
<capability>http://openconfig.net/yang/cisco-xe-openconfig-interfaces-deviation?module=cisco-xe-openconfig-interfaces-deviation&amp;revision=2018-08-21</capability>
<capability>http://openconfig.net/yang/cisco-xe-routing-csr-openconfig-platform-deviation?module=cisco-xe-routing-csr-openconfig-platform-deviation&amp;revision=2010-10-09</capability>
<capability>http://openconfig.net/yang/cisco-xe-routing-openconfig-system-deviation?module=cisco-xe-routing-openconfig-system-deviation&amp;revision=2017-11-27</capability>
<capability>http://openconfig.net/yang/fib-types?module=openconfig-aft-types&amp;revision=2017-01-13</capability>
<capability>http://openconfig.net/yang/header-fields?module=openconfig-packet-match&amp;revision=2017-05-26</capability>
<capability>http://openconfig.net/yang/interfaces?module=openconfig-interfaces&amp;revision=2018-01-05&amp;deviations=cisco-xe-openconfig-if-ip-deviation,cisco-xe-openconfig-interfaces-deviation,cisco-xe-routing-openconfig-vlan-deviation</capability>
<capability>http://openconfig.net/yang/interfaces/aggregate?module=openconfig-if-aggregate&amp;revision=2018-01-05</capability>
<capability>http://openconfig.net/yang/interfaces/ethernet?module=openconfig-if-ethernet&amp;revision=2018-01-05</capability>
<capability>http://openconfig.net/yang/interfaces/ip?module=openconfig-if-ip&amp;revision=2018-01-05&amp;deviations=cisco-xe-openconfig-if-ip-deviation,cisco-xe-openconfig-interfaces-deviation</capability>
<capability>http://openconfig.net/yang/interfaces/ip-ext?module=openconfig-if-ip-ext&amp;revision=2018-01-05</capability>
<capability>http://openconfig.net/yang/isis-lsdb-types?module=openconfig-isis-lsdb-types&amp;revision=2017-01-13</capability>
<capability>http://openconfig.net/yang/isis-types?module=openconfig-isis-types&amp;revision=2017-01-13</capability>
<capability>http://openconfig.net/yang/lacp?module=openconfig-lacp&amp;revision=2016-05-26</capability>
<capability>http://openconfig.net/yang/ldp?module=openconfig-mpls-ldp&amp;revision=2016-12-15</capability>
<capability>http://openconfig.net/yang/lldp?module=openconfig-lldp&amp;revision=2018-11-21&amp;deviations=cisco-xe-openconfig-lldp-deviation</capability>
<capability>http://openconfig.net/yang/lldp/types?module=openconfig-lldp-types&amp;revision=2016-05-16</capability>
<capability>http://openconfig.net/yang/local-routing?module=openconfig-local-routing&amp;revision=2016-05-11</capability>
<capability>http://openconfig.net/yang/mpls?module=openconfig-mpls&amp;revision=2016-12-15&amp;deviations=cisco-xe-openconfig-mpls-deviation</capability>
<capability>http://openconfig.net/yang/mpls-sr?module=openconfig-mpls-sr&amp;revision=2016-12-15</capability>
<capability>http://openconfig.net/yang/mpls-types?module=openconfig-mpls-types&amp;revision=2016-12-15</capability>
<capability>http://openconfig.net/yang/network-instance?module=openconfig-network-instance&amp;revision=2017-01-13&amp;deviations=cisco-xe-openconfig-aft-deviation,cisco-xe-openconfig-bgp-deviation,cisco-xe-openconfig-isis-deviation,cisco-xe-openconfig-mpls-deviation,cisco-xe-openconfig-network-instance-deviation,cisco-xe-openconfig-segment-routing-deviation</capability>
<capability>http://openconfig.net/yang/network-instance-l3?module=openconfig-network-instance-l3&amp;revision=2017-01-13</capability>
<capability>http://openconfig.net/yang/network-instance-types?module=openconfig-network-instance-types&amp;revision=2016-12-15</capability>
<capability>http://openconfig.net/yang/openconfig-ext?module=openconfig-extensions&amp;revision=2018-10-17</capability>
<capability>http://openconfig.net/yang/openconfig-isis?module=openconfig-isis&amp;revision=2017-01-13</capability>
<capability>http://openconfig.net/yang/openconfig-isis-policy?module=openconfig-isis-policy&amp;revision=2017-01-13</capability>
<capability>http://openconfig.net/yang/openconfig-types?module=openconfig-types&amp;revision=2019-04-16</capability>
<capability>http://openconfig.net/yang/packet-match-types?module=openconfig-packet-match-types&amp;revision=2017-05-26</capability>
<capability>http://openconfig.net/yang/platform?module=openconfig-platform&amp;revision=2018-11-21&amp;deviations=cisco-xe-routing-csr-openconfig-platform-deviation</capability>
<capability>http://openconfig.net/yang/platform-types?module=openconfig-platform-types&amp;revision=2018-11-21</capability>
<capability>http://openconfig.net/yang/policy-types?module=openconfig-policy-types&amp;revision=2016-05-12</capability>
<capability>http://openconfig.net/yang/rib/bgp?module=openconfig-rib-bgp&amp;revision=2017-03-07</capability>
<capability>http://openconfig.net/yang/rib/bgp-ext?module=openconfig-rib-bgp-ext&amp;revision=2016-04-11</capability>
<capability>http://openconfig.net/yang/rib/bgp-types?module=openconfig-rib-bgp-types&amp;revision=2016-04-11</capability>
<capability>http://openconfig.net/yang/routing-policy?module=openconfig-routing-policy&amp;revision=2016-05-12&amp;deviations=cisco-xe-openconfig-bgp-policy-deviation,cisco-xe-openconfig-routing-policy-deviation</capability>
<capability>http://openconfig.net/yang/rsvp?module=openconfig-mpls-rsvp&amp;revision=2016-12-15</capability>
<capability>http://openconfig.net/yang/sr?module=openconfig-segment-routing&amp;revision=2017-01-12</capability>
<capability>http://openconfig.net/yang/system?module=openconfig-system&amp;revision=2018-07-17&amp;deviations=cisco-xe-routing-openconfig-system-deviation,cisco-xe-routing-openconfig-system-management-deviation</capability>
<capability>http://openconfig.net/yang/system/logging?module=openconfig-system-logging&amp;revision=2017-09-18</capability>
<capability>http://openconfig.net/yang/system/management?module=openconfig-system-management&amp;revision=2018-11-21</capability>
<capability>http://openconfig.net/yang/system/procmon?module=openconfig-procmon&amp;revision=2017-09-18</capability>
<capability>http://openconfig.net/yang/system/terminal?module=openconfig-system-terminal&amp;revision=2017-09-18</capability>
<capability>http://openconfig.net/yang/types/inet?module=openconfig-inet-types&amp;revision=2017-08-24</capability>
<capability>http://openconfig.net/yang/types/yang?module=openconfig-yang-types&amp;revision=2018-11-21</capability>
<capability>http://openconfig.net/yang/vlan?module=openconfig-vlan&amp;revision=2016-05-26&amp;deviations=cisco-xe-routing-openconfig-vlan-deviation</capability>
<capability>http://openconfig.net/yang/vlan-types?module=openconfig-vlan-types&amp;revision=2016-05-26</capability>
<capability>http://tail-f.com/ns/common/query?module=tailf-common-query&amp;revision=2017-12-15</capability>
<capability>http://tail-f.com/yang/common?module=tailf-common&amp;revision=2019-05-16</capability>
<capability>http://tail-f.com/yang/common-monitoring?module=tailf-common-monitoring&amp;revision=2019-04-09</capability>
<capability>http://tail-f.com/yang/confd-monitoring?module=tailf-confd-monitoring&amp;revision=2019-10-30</capability>
<capability>http://tail-f.com/yang/netconf-monitoring?module=tailf-netconf-monitoring&amp;revision=2019-03-28</capability>
<capability>urn:cisco:params:xml:ns:yang:cisco-bridge-common?module=cisco-bridge-common&amp;revision=2019-07-01&amp;features=configurable-bd-mac-limit-notif,configurable-bd-mac-limit-max,configurable-bd-mac-limit-actions,configurable-bd-mac-aging-types,configurable-bd-flooding-control</capability>
<capability>urn:cisco:params:xml:ns:yang:cisco-bridge-domain?module=cisco-bridge-domain&amp;revision=2019-07-01&amp;features=parameterized-bridge-domains,configurable-bd-storm-control,configurable-bd-static-mac,configurable-bd-snooping-profiles,configurable-bd-sh-group-number,configurable-bd-mtu,configurable-bd-member-features,configurable-bd-mac-secure,configurable-bd-mac-features,configurable-bd-mac-event-action,configurable-bd-ipsg,configurable-bd-groups,configurable-bd-flooding-mode,configurable-bd-flooding,configurable-bd-dai,clear-bridge-domain</capability>
<capability>urn:cisco:params:xml:ns:yang:cisco-ethernet?module=cisco-ethernet&amp;revision=2016-05-10</capability>
<capability>urn:cisco:params:xml:ns:yang:cisco-routing-ext?module=cisco-routing-ext&amp;revision=2019-11-01</capability>
<capability>urn:cisco:params:xml:ns:yang:cisco-storm-control?module=cisco-storm-control&amp;revision=2019-07-01&amp;features=configurable-storm-control-actions</capability>
<capability>urn:cisco:params:xml:ns:yang:cisco-xe-ietf-yang-push-ext?module=cisco-xe-ietf-yang-push-ext&amp;revision=2020-04-27</capability>
<capability>urn:cisco:params:xml:ns:yang:pim?module=pim&amp;revision=2019-07-01&amp;features=bsr,auto-rp</capability>
<capability>urn:cisco:params:xml:ns:yang:pw?module=cisco-pw&amp;revision=2019-07-01&amp;features=static-label-direct-config,pw-vccv,pw-tag-impose-vlan-id,pw-status-config,pw-static-oam-config,pw-short-config,pw-sequencing,pw-preferred-path,pw-port-profiles,pw-oam-refresh-config,pw-mac-withdraw-config,pw-load-balancing,pw-ipv6-source,pw-interface,pw-grouping-config,pw-class-tag-rewrite,pw-class-switchover-delay,pw-class-status,pw-class-source-ip,pw-class-flow-setting,preferred-path-peer,predictive-redundancy-config,flow-label-tlv-code17,flow-label-static-config</capability>
<capability>urn:ietf:params:xml:ns:netconf:base:1.0?module=ietf-netconf&amp;revision=2011-06-01&amp;features=writable-running,rollback-on-error,validate,xpath</capability>
<capability>urn:ietf:params:xml:ns:yang:c3pl-types?module=policy-types&amp;revision=2019-07-01&amp;features=protocol-name-support,match-wlan-user-priority-support,match-vpls-support,match-vlan-support,match-vlan-inner-support,match-src-mac-support,match-security-group-support,match-qos-group-support,match-prec-support,match-packet-length-support,match-mpls-exp-top-support,match-mpls-exp-imp-support,match-metadata-support,match-ipv6-acl-support,match-ipv6-acl-name-support,match-ipv4-acl-support,match-ipv4-acl-name-support,match-ip-rtp-support,match-input-interface-support,match-fr-dlci-support,match-fr-de-support,match-flow-record-support,match-flow-ip-support,match-dst-mac-support,match-discard-class-support,match-dei-support,match-dei-inner-support,match-cos-support,match-cos-inner-support,match-class-map-support,match-atm-vci-support,match-atm-clp-support,match-application-support</capability>
<capability>urn:ietf:params:xml:ns:yang:cisco-ospf?module=cisco-ospf&amp;revision=2019-07-01&amp;features=graceful-shutdown,flood-reduction,database-filter</capability>
<capability>urn:ietf:params:xml:ns:yang:cisco-policy?module=cisco-policy&amp;revision=2019-07-01</capability>
<capability>urn:ietf:params:xml:ns:yang:cisco-policy-filters?module=cisco-policy-filters&amp;revision=2019-07-01</capability>
<capability>urn:ietf:params:xml:ns:yang:cisco-policy-target?module=cisco-policy-target&amp;revision=2019-07-01</capability>
<capability>urn:ietf:params:xml:ns:yang:common-mpls-static?module=common-mpls-static&amp;revision=2019-07-01&amp;deviations=common-mpls-static-devs</capability>
<capability>urn:ietf:params:xml:ns:yang:common-mpls-types?module=common-mpls-types&amp;revision=2019-07-01</capability>
<capability>urn:ietf:params:xml:ns:yang:iana-crypt-hash?module=iana-crypt-hash&amp;revision=2014-08-06&amp;features=crypt-hash-sha-512,crypt-hash-sha-256,crypt-hash-md5</capability>
<capability>urn:ietf:params:xml:ns:yang:iana-if-type?module=iana-if-type&amp;revision=2014-05-08</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-diffserv-action?module=ietf-diffserv-action&amp;revision=2015-04-07&amp;features=priority-rate-burst-support,hierarchial-policy-support,aqm-red-support</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-diffserv-classifier?module=ietf-diffserv-classifier&amp;revision=2015-04-07&amp;features=policy-inline-classifier-config</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-diffserv-policy?module=ietf-diffserv-policy&amp;revision=2015-04-07&amp;features=policy-template-support,hierarchial-policy-support</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-diffserv-target?module=ietf-diffserv-target&amp;revision=2015-04-07&amp;features=target-inline-policy-config</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-event-notifications?module=ietf-event-notifications&amp;revision=2016-10-27&amp;features=json,configured-subscriptions&amp;deviations=cisco-xe-ietf-event-notifications-deviation,cisco-xe-ietf-yang-push-deviation</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-inet-types?module=ietf-inet-types&amp;revision=2013-07-15</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-interfaces?module=ietf-interfaces&amp;revision=2014-05-08&amp;features=pre-provisioning,if-mib,arbitrary-names&amp;deviations=cisco-xe-ietf-ip-deviation</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-interfaces-ext?module=ietf-interfaces-ext</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-ip?module=ietf-ip&amp;revision=2014-06-16&amp;features=ipv6-privacy-autoconf,ipv4-non-contiguous-netmasks&amp;deviations=cisco-xe-ietf-ip-deviation</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-ipv4-unicast-routing?module=ietf-ipv4-unicast-routing&amp;revision=2015-05-25&amp;deviations=cisco-xe-ietf-ipv4-unicast-routing-deviation</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-ipv6-unicast-routing?module=ietf-ipv6-unicast-routing&amp;revision=2015-05-25&amp;deviations=cisco-xe-ietf-ipv6-unicast-routing-deviation</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-key-chain?module=ietf-key-chain&amp;revision=2015-02-24&amp;features=independent-send-accept-lifetime,hex-key-string,accept-tolerance</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-netconf-acm?module=ietf-netconf-acm&amp;revision=2012-02-22</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring?module=ietf-netconf-monitoring&amp;revision=2010-10-04</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-netconf-notifications?module=ietf-netconf-notifications&amp;revision=2012-02-06</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-netconf-with-defaults?module=ietf-netconf-with-defaults&amp;revision=2011-06-01</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-ospf?module=ietf-ospf&amp;revision=2015-03-09&amp;features=ttl-security,te-rid,router-id,remote-lfa,prefix-suppression,ospfv3-authentication-ipsec,nsr,node-flag,multi-topology,multi-area-adj,mtu-ignore,max-lsa,max-ecmp,lls,lfa,ldp-igp-sync,ldp-igp-autoconfig,interface-inheritance,instance-inheritance,graceful-restart,fast-reroute,demand-circuit,bfd,auto-cost,area-inheritance,admin-control&amp;deviations=cisco-xe-ietf-ospf-deviation</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-restconf-monitoring?module=ietf-restconf-monitoring&amp;revision=2017-01-26</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-routing?module=ietf-routing&amp;revision=2015-05-25&amp;features=router-id,multiple-ribs&amp;deviations=cisco-xe-ietf-ipv4-unicast-routing-deviation,cisco-xe-ietf-ipv6-unicast-routing-deviation,cisco-xe-ietf-ospf-deviation,cisco-xe-ietf-routing-deviation</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-yang-library?module=ietf-yang-library&amp;revision=2016-06-21</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-yang-push?module=ietf-yang-push&amp;revision=2016-10-28&amp;features=on-change&amp;deviations=cisco-xe-ietf-yang-push-deviation</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-yang-smiv2?module=ietf-yang-smiv2&amp;revision=2012-06-22</capability>
<capability>urn:ietf:params:xml:ns:yang:ietf-yang-types?module=ietf-yang-types&amp;revision=2013-07-15</capability>
<capability>urn:ietf:params:xml:ns:yang:nvo?module=nvo&amp;revision=2019-07-01&amp;deviations=nvo-devs</capability>
<capability>urn:ietf:params:xml:ns:yang:policy-attr?module=policy-attr&amp;revision=2019-07-01</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:ATM-FORUM-TC-MIB?module=ATM-FORUM-TC-MIB</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:ATM-MIB?module=ATM-MIB&amp;revision=1998-10-19</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:ATM-TC-MIB?module=ATM-TC-MIB&amp;revision=1998-10-19</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:BGP4-MIB?module=BGP4-MIB&amp;revision=1994-05-05</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:BRIDGE-MIB?module=BRIDGE-MIB&amp;revision=2005-09-19</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-AAA-SERVER-MIB?module=CISCO-AAA-SERVER-MIB&amp;revision=2003-11-17</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-AAA-SESSION-MIB?module=CISCO-AAA-SESSION-MIB&amp;revision=2006-03-21</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-AAL5-MIB?module=CISCO-AAL5-MIB&amp;revision=2003-09-22</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ATM-EXT-MIB?module=CISCO-ATM-EXT-MIB&amp;revision=2003-01-06</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ATM-PVCTRAP-EXTN-MIB?module=CISCO-ATM-PVCTRAP-EXTN-MIB&amp;revision=2003-01-20</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ATM-QOS-MIB?module=CISCO-ATM-QOS-MIB&amp;revision=2002-06-10</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-BGP-POLICY-ACCOUNTING-MIB?module=CISCO-BGP-POLICY-ACCOUNTING-MIB&amp;revision=2002-07-26</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-BGP4-MIB?module=CISCO-BGP4-MIB&amp;revision=2010-09-30</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-BULK-FILE-MIB?module=CISCO-BULK-FILE-MIB&amp;revision=2002-06-10</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-CBP-TARGET-MIB?module=CISCO-CBP-TARGET-MIB&amp;revision=2006-05-24</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-CBP-TARGET-TC-MIB?module=CISCO-CBP-TARGET-TC-MIB&amp;revision=2006-03-24</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-CBP-TC-MIB?module=CISCO-CBP-TC-MIB&amp;revision=2008-06-24</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-CDP-MIB?module=CISCO-CDP-MIB&amp;revision=2005-03-21</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-CEF-MIB?module=CISCO-CEF-MIB&amp;revision=2006-01-30</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-CEF-TC?module=CISCO-CEF-TC&amp;revision=2005-09-30</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-COPY-MIB?module=CISCO-CONFIG-COPY-MIB&amp;revision=2005-04-06</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB?module=CISCO-CONFIG-MAN-MIB&amp;revision=2007-04-27</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONTEXT-MAPPING-MIB?module=CISCO-CONTEXT-MAPPING-MIB&amp;revision=2008-11-22</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-DATA-COLLECTION-MIB?module=CISCO-DATA-COLLECTION-MIB&amp;revision=2002-10-30</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-DIAL-CONTROL-MIB?module=CISCO-DIAL-CONTROL-MIB&amp;revision=2005-05-26</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-DOT3-OAM-MIB?module=CISCO-DOT3-OAM-MIB&amp;revision=2006-05-31</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-DYNAMIC-TEMPLATE-MIB?module=CISCO-DYNAMIC-TEMPLATE-MIB&amp;revision=2007-09-06</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-DYNAMIC-TEMPLATE-TC-MIB?module=CISCO-DYNAMIC-TEMPLATE-TC-MIB&amp;revision=2012-01-27</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-EIGRP-MIB?module=CISCO-EIGRP-MIB&amp;revision=2004-11-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-EMBEDDED-EVENT-MGR-MIB?module=CISCO-EMBEDDED-EVENT-MGR-MIB&amp;revision=2006-11-07</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENHANCED-MEMPOOL-MIB?module=CISCO-ENHANCED-MEMPOOL-MIB&amp;revision=2008-12-05</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-ALARM-MIB?module=CISCO-ENTITY-ALARM-MIB&amp;revision=1999-07-06</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-EXT-MIB?module=CISCO-ENTITY-EXT-MIB&amp;revision=2008-11-24</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-FRU-CONTROL-MIB?module=CISCO-ENTITY-FRU-CONTROL-MIB&amp;revision=2013-08-19</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-QFP-MIB?module=CISCO-ENTITY-QFP-MIB&amp;revision=2014-06-18</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-SENSOR-MIB?module=CISCO-ENTITY-SENSOR-MIB&amp;revision=2015-01-15</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-VENDORTYPE-OID-MIB?module=CISCO-ENTITY-VENDORTYPE-OID-MIB&amp;revision=2014-12-09</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ETHER-CFM-MIB?module=CISCO-ETHER-CFM-MIB&amp;revision=2004-12-28</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ETHERLIKE-EXT-MIB?module=CISCO-ETHERLIKE-EXT-MIB&amp;revision=2010-06-04</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-FIREWALL-TC?module=CISCO-FIREWALL-TC&amp;revision=2006-03-03</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-FLASH-MIB?module=CISCO-FLASH-MIB&amp;revision=2013-08-06</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-FTP-CLIENT-MIB?module=CISCO-FTP-CLIENT-MIB&amp;revision=2006-03-31</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-HSRP-EXT-MIB?module=CISCO-HSRP-EXT-MIB&amp;revision=2010-09-02</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-HSRP-MIB?module=CISCO-HSRP-MIB&amp;revision=2010-09-06</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-ATM2-PVCTRAP-MIB?module=CISCO-IETF-ATM2-PVCTRAP-MIB&amp;revision=1998-02-03</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-ATM2-PVCTRAP-MIB-EXTN?module=CISCO-IETF-ATM2-PVCTRAP-MIB-EXTN&amp;revision=2000-07-11</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-BFD-MIB?module=CISCO-IETF-BFD-MIB&amp;revision=2011-04-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-FRR-MIB?module=CISCO-IETF-FRR-MIB&amp;revision=2008-04-29</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-ISIS-MIB?module=CISCO-IETF-ISIS-MIB&amp;revision=2005-08-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-MPLS-ID-STD-03-MIB?module=CISCO-IETF-MPLS-ID-STD-03-MIB&amp;revision=2012-06-07</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-MPLS-TE-EXT-STD-03-MIB?module=CISCO-IETF-MPLS-TE-EXT-STD-03-MIB&amp;revision=2012-06-06</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-ATM-MIB?module=CISCO-IETF-PW-ATM-MIB&amp;revision=2005-04-19</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-ENET-MIB?module=CISCO-IETF-PW-ENET-MIB&amp;revision=2002-09-22</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-MIB?module=CISCO-IETF-PW-MIB&amp;revision=2004-03-17</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-MPLS-MIB?module=CISCO-IETF-PW-MPLS-MIB&amp;revision=2003-02-26</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-TC-MIB?module=CISCO-IETF-PW-TC-MIB&amp;revision=2006-07-21</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-TDM-MIB?module=CISCO-IETF-PW-TDM-MIB&amp;revision=2006-07-21</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IF-EXTENSION-MIB?module=CISCO-IF-EXTENSION-MIB&amp;revision=2013-03-13</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IGMP-FILTER-MIB?module=CISCO-IGMP-FILTER-MIB&amp;revision=2005-11-29</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IMAGE-LICENSE-MGMT-MIB?module=CISCO-IMAGE-LICENSE-MGMT-MIB&amp;revision=2007-10-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IMAGE-MIB?module=CISCO-IMAGE-MIB&amp;revision=1995-08-15</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IP-LOCAL-POOL-MIB?module=CISCO-IP-LOCAL-POOL-MIB&amp;revision=2007-11-12</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IP-TAP-MIB?module=CISCO-IP-TAP-MIB&amp;revision=2004-03-11</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IP-URPF-MIB?module=CISCO-IP-URPF-MIB&amp;revision=2011-12-29</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPMROUTE-MIB?module=CISCO-IPMROUTE-MIB&amp;revision=2005-03-07</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSEC-FLOW-MONITOR-MIB?module=CISCO-IPSEC-FLOW-MONITOR-MIB&amp;revision=2007-10-24</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSEC-MIB?module=CISCO-IPSEC-MIB&amp;revision=2000-08-07</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSEC-POLICY-MAP-MIB?module=CISCO-IPSEC-POLICY-MAP-MIB&amp;revision=2000-08-17</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSLA-AUTOMEASURE-MIB?module=CISCO-IPSLA-AUTOMEASURE-MIB&amp;revision=2007-06-13</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSLA-ECHO-MIB?module=CISCO-IPSLA-ECHO-MIB&amp;revision=2007-08-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSLA-JITTER-MIB?module=CISCO-IPSLA-JITTER-MIB&amp;revision=2007-07-24</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSLA-TC-MIB?module=CISCO-IPSLA-TC-MIB&amp;revision=2007-03-23</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-LICENSE-MGMT-MIB?module=CISCO-LICENSE-MGMT-MIB&amp;revision=2012-04-19</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-MEDIA-GATEWAY-MIB?module=CISCO-MEDIA-GATEWAY-MIB&amp;revision=2009-02-25</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-MPLS-LSR-EXT-STD-MIB?module=CISCO-MPLS-LSR-EXT-STD-MIB&amp;revision=2012-04-30</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-MPLS-TC-EXT-STD-MIB?module=CISCO-MPLS-TC-EXT-STD-MIB&amp;revision=2012-02-22</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-NBAR-PROTOCOL-DISCOVERY-MIB?module=CISCO-NBAR-PROTOCOL-DISCOVERY-MIB&amp;revision=2002-08-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-NETSYNC-MIB?module=CISCO-NETSYNC-MIB&amp;revision=2010-10-15</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-NTP-MIB?module=CISCO-NTP-MIB&amp;revision=2006-07-31</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-OSPF-MIB?module=CISCO-OSPF-MIB&amp;revision=2003-07-18</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-OSPF-TRAP-MIB?module=CISCO-OSPF-TRAP-MIB&amp;revision=2003-07-18</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-PIM-MIB?module=CISCO-PIM-MIB&amp;revision=2000-11-02</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-PING-MIB?module=CISCO-PING-MIB&amp;revision=2001-08-28</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-PROCESS-MIB?module=CISCO-PROCESS-MIB&amp;revision=2011-06-23</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-PRODUCTS-MIB?module=CISCO-PRODUCTS-MIB&amp;revision=2014-11-06</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-PTP-MIB?module=CISCO-PTP-MIB&amp;revision=2011-01-28</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-QOS-PIB-MIB?module=CISCO-QOS-PIB-MIB&amp;revision=2007-08-29</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-RADIUS-EXT-MIB?module=CISCO-RADIUS-EXT-MIB&amp;revision=2010-05-25</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-RF-MIB?module=CISCO-RF-MIB&amp;revision=2005-09-01</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-RTTMON-MIB?module=CISCO-RTTMON-MIB&amp;revision=2012-08-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-RTTMON-TC-MIB?module=CISCO-RTTMON-TC-MIB&amp;revision=2012-05-25</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-SESS-BORDER-CTRLR-CALL-STATS-MIB?module=CISCO-SESS-BORDER-CTRLR-CALL-STATS-MIB&amp;revision=2010-09-03</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-SESS-BORDER-CTRLR-STATS-MIB?module=CISCO-SESS-BORDER-CTRLR-STATS-MIB&amp;revision=2010-09-15</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-SIP-UA-MIB?module=CISCO-SIP-UA-MIB&amp;revision=2004-02-19</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-SMI?module=CISCO-SMI&amp;revision=2012-08-29</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-SONET-MIB?module=CISCO-SONET-MIB&amp;revision=2003-03-07</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-ST-TC?module=CISCO-ST-TC&amp;revision=2012-08-08</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-STP-EXTENSIONS-MIB?module=CISCO-STP-EXTENSIONS-MIB&amp;revision=2013-03-07</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-SUBSCRIBER-IDENTITY-TC-MIB?module=CISCO-SUBSCRIBER-IDENTITY-TC-MIB&amp;revision=2011-12-23</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-SUBSCRIBER-SESSION-MIB?module=CISCO-SUBSCRIBER-SESSION-MIB&amp;revision=2012-08-08</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-SUBSCRIBER-SESSION-TC-MIB?module=CISCO-SUBSCRIBER-SESSION-TC-MIB&amp;revision=2012-01-27</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-SYSLOG-MIB?module=CISCO-SYSLOG-MIB&amp;revision=2005-12-03</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-TAP2-MIB?module=CISCO-TAP2-MIB&amp;revision=2009-11-06</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-TC?module=CISCO-TC&amp;revision=2011-11-11</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-UBE-MIB?module=CISCO-UBE-MIB&amp;revision=2010-11-29</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-UNIFIED-FIREWALL-MIB?module=CISCO-UNIFIED-FIREWALL-MIB&amp;revision=2005-09-22</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-VLAN-IFTABLE-RELATIONSHIP-MIB?module=CISCO-VLAN-IFTABLE-RELATIONSHIP-MIB&amp;revision=2013-07-15</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-VLAN-MEMBERSHIP-MIB?module=CISCO-VLAN-MEMBERSHIP-MIB&amp;revision=2007-12-14</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-VOICE-COMMON-DIAL-CONTROL-MIB?module=CISCO-VOICE-COMMON-DIAL-CONTROL-MIB&amp;revision=2010-06-30</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-VOICE-DIAL-CONTROL-MIB?module=CISCO-VOICE-DIAL-CONTROL-MIB&amp;revision=2012-05-15</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-VOICE-DNIS-MIB?module=CISCO-VOICE-DNIS-MIB&amp;revision=2002-05-01</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-VPDN-MGMT-MIB?module=CISCO-VPDN-MGMT-MIB&amp;revision=2009-06-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:CISCO-VTP-MIB?module=CISCO-VTP-MIB&amp;revision=2013-10-14</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:DIAL-CONTROL-MIB?module=DIAL-CONTROL-MIB&amp;revision=1996-09-23</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:DIFFSERV-DSCP-TC?module=DIFFSERV-DSCP-TC&amp;revision=2002-05-09</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:DIFFSERV-MIB?module=DIFFSERV-MIB&amp;revision=2002-02-07</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:DISMAN-EVENT-MIB?module=DISMAN-EVENT-MIB&amp;revision=2000-10-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:DISMAN-EXPRESSION-MIB?module=DISMAN-EXPRESSION-MIB&amp;revision=2000-10-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:DRAFT-MSDP-MIB?module=DRAFT-MSDP-MIB&amp;revision=1999-12-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:DS1-MIB?module=DS1-MIB&amp;revision=1998-08-01</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:DS3-MIB?module=DS3-MIB&amp;revision=1998-08-01</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:ENTITY-MIB?module=ENTITY-MIB&amp;revision=2005-08-10</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:ENTITY-SENSOR-MIB?module=ENTITY-SENSOR-MIB&amp;revision=2002-12-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:ENTITY-STATE-MIB?module=ENTITY-STATE-MIB&amp;revision=2005-11-22</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:ENTITY-STATE-TC-MIB?module=ENTITY-STATE-TC-MIB&amp;revision=2005-11-22</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:ETHER-WIS?module=ETHER-WIS&amp;revision=2003-09-19</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:EXPRESSION-MIB?module=EXPRESSION-MIB&amp;revision=2005-11-24</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:EtherLike-MIB?module=EtherLike-MIB&amp;revision=2003-09-19</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:FRAME-RELAY-DTE-MIB?module=FRAME-RELAY-DTE-MIB&amp;revision=1997-05-01</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:HCNUM-TC?module=HCNUM-TC&amp;revision=2000-06-08</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:IANA-ADDRESS-FAMILY-NUMBERS-MIB?module=IANA-ADDRESS-FAMILY-NUMBERS-MIB&amp;revision=2000-09-08</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:IANA-RTPROTO-MIB?module=IANA-RTPROTO-MIB&amp;revision=2000-09-26</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:IANAifType-MIB?module=IANAifType-MIB&amp;revision=2006-03-31</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:IEEE8021-TC-MIB?module=IEEE8021-TC-MIB&amp;revision=2008-10-15</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:IF-MIB?module=IF-MIB&amp;revision=2000-06-14</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:IGMP-STD-MIB?module=IGMP-STD-MIB&amp;revision=2000-09-28</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:INET-ADDRESS-MIB?module=INET-ADDRESS-MIB&amp;revision=2005-02-04</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:INT-SERV-MIB?module=INT-SERV-MIB&amp;revision=1997-10-03</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:INTEGRATED-SERVICES-MIB?module=INTEGRATED-SERVICES-MIB&amp;revision=1995-11-03</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:IP-FORWARD-MIB?module=IP-FORWARD-MIB&amp;revision=1996-09-19</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:IP-MIB?module=IP-MIB&amp;revision=2006-02-02</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:IPMROUTE-STD-MIB?module=IPMROUTE-STD-MIB&amp;revision=2000-09-22</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:IPV6-FLOW-LABEL-MIB?module=IPV6-FLOW-LABEL-MIB&amp;revision=2003-08-28</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:LLDP-MIB?module=LLDP-MIB&amp;revision=2005-05-06</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:MPLS-L3VPN-STD-MIB?module=MPLS-L3VPN-STD-MIB&amp;revision=2006-01-23</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:MPLS-LDP-GENERIC-STD-MIB?module=MPLS-LDP-GENERIC-STD-MIB&amp;revision=2004-06-03</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:MPLS-LDP-STD-MIB?module=MPLS-LDP-STD-MIB&amp;revision=2004-06-03</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:MPLS-LSR-STD-MIB?module=MPLS-LSR-STD-MIB&amp;revision=2004-06-03</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:MPLS-TC-MIB?module=MPLS-TC-MIB&amp;revision=2001-01-04</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:MPLS-TC-STD-MIB?module=MPLS-TC-STD-MIB&amp;revision=2004-06-03</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:MPLS-TE-STD-MIB?module=MPLS-TE-STD-MIB&amp;revision=2004-06-03</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:MPLS-VPN-MIB?module=MPLS-VPN-MIB&amp;revision=2001-10-15</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:NHRP-MIB?module=NHRP-MIB&amp;revision=1999-08-26</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:NOTIFICATION-LOG-MIB?module=NOTIFICATION-LOG-MIB&amp;revision=2000-11-27</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:OSPF-MIB?module=OSPF-MIB&amp;revision=2006-11-10</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:OSPF-TRAP-MIB?module=OSPF-TRAP-MIB&amp;revision=2006-11-10</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:P-BRIDGE-MIB?module=P-BRIDGE-MIB&amp;revision=2006-01-09</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:PIM-MIB?module=PIM-MIB&amp;revision=2000-09-28</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:PerfHist-TC-MIB?module=PerfHist-TC-MIB&amp;revision=1998-11-07</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:Q-BRIDGE-MIB?module=Q-BRIDGE-MIB&amp;revision=2006-01-09</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:RFC-1212?module=RFC-1212</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:RFC-1215?module=RFC-1215</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:RFC1155-SMI?module=RFC1155-SMI</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:RFC1213-MIB?module=RFC1213-MIB</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:RFC1315-MIB?module=RFC1315-MIB</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:RMON-MIB?module=RMON-MIB&amp;revision=2000-05-11</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:RMON2-MIB?module=RMON2-MIB&amp;revision=1996-05-27</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:RSVP-MIB?module=RSVP-MIB&amp;revision=1998-08-25</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:SNMP-FRAMEWORK-MIB?module=SNMP-FRAMEWORK-MIB&amp;revision=2002-10-14</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:SNMP-PROXY-MIB?module=SNMP-PROXY-MIB&amp;revision=2002-10-14</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:SNMP-TARGET-MIB?module=SNMP-TARGET-MIB&amp;revision=1998-08-04</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:SNMPv2-MIB?module=SNMPv2-MIB&amp;revision=2002-10-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:SNMPv2-TC?module=SNMPv2-TC</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:SONET-MIB?module=SONET-MIB&amp;revision=2003-08-11</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:TCP-MIB?module=TCP-MIB&amp;revision=2005-02-18</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:TOKEN-RING-RMON-MIB?module=TOKEN-RING-RMON-MIB</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:TOKENRING-MIB?module=TOKENRING-MIB&amp;revision=1994-10-23</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:TUNNEL-MIB?module=TUNNEL-MIB&amp;revision=2005-05-16</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:UDP-MIB?module=UDP-MIB&amp;revision=2005-05-20</capability>
<capability>urn:ietf:params:xml:ns:yang:smiv2:VPN-TC-STD-MIB?module=VPN-TC-STD-MIB&amp;revision=2005-11-15</capability>
<capability>
        urn:ietf:params:netconf:capability:notification:1.1
      </capability>
</capabilities>
<session-id>26</session-id></hello>]]>]]>
```

![cml-lab-netconf-restconf](./cml-lab-restconf-netconf.png)

- More info and documentation:

[netconf-configuration](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/1717/b_1717_programmability_cg/m_1717_prog_yang_netconf.html#id_84436)

#### RESTCONF

- RESTCONF, defined in RFC 8040 is used to programatically interface with data defined in YANG models while using the datastore concepts defined in NETCONF

- It is a common misconception that RESTCONF is meant to replace NETCONF, but this is not the case

- Both are very common methods used for programmability and data manipulation

- In fact, RESTCONF uses the same YANG models as NETCONF and Cisco IOS XE

- The goal or RESTCONF is to provide a RESTful API experience while leveraging the device abstraction capabilities provided by NETCONF

- RESTCONF supports the following HTTP methods and CRUD operations:

    - GET

    - POST

    - PUT

    - DELETE

    - OPTIONS

- The RESTCONF requests and responses can use either JSON or XML structured data formats

- Below is shown a brief example of a RESTCONF get request on a Cisco router to retrieve the logging severity level that is configured

- This example uses JSON instead of XML

- Notice the HTTP status 200, which indicates that the request was successful

```
RESTCONF GET

.............................

URL: https://10.85.116.59:443/restconf/data/Cisco-IOS-XE-native:native/logging/monitor/severity

Headers: {'Accept-Encoding': 'gzip, deflate', 'Accept': 'application/yang-data+json, application/yang-data.errors+json'}

Body:


RESTCONF RESPONSE

............................

200

{
    "Cisco-IOS-XE-native:severity": "critical"
}
```

- RESTCONF configuration requires the configuration of http server on the router:

- First create an AAA method list

```
conf t
 aaa new-model
 aaa group server radius <servername> ! ISE
  server-private <ip-address> key <key-name>
 aaa authentication login default group ISE local
 aaa authentication login NOAUTH none
 aaa authorization exec default group ISE local
 aaa session-id common
 line console 0
  login authentication NOAUTH
```

- Enable restconf and HTTPS service:

```
conf t
 restconf
 ip http secure-server
```

- Verification:

```
CSR2(config)#do sh platform software yang-management process monitor
COMMAND           PID S    VSZ   RSS %CPU %MEM     ELAPSED
confd           30717 S 155984 132112 3.2  4.3       16:40
confd-startup.s 28634 S   6204  4252  0.0  0.1       16:46
confd-startup.s 30720 S   6204  3384  0.0  0.1       16:40
dmiauthd        29078 S 364724 29880  0.0  0.9       16:45
ncsshd          29417 S 296364  8952  0.0  0.2       16:44
ncsshd_bp       29306 S 171056  8196  0.0  0.2       16:44
ndbmand         28796 S 815812 56672  0.0  1.8       16:46
nginx           32112 S 104420  8148  0.0  0.2       01:34
nginx           32122 S 104992  4088  0.0  0.1       01:33
nginx           32123 S  56384  3508  0.0  0.1       01:33
pubd            18186 S 1174420 64296 0.0  2.1       42:45



CSR2(config)#do sh platform software yang-management process        
confd            : Running    
nesd             : Running    
syncfd           : Running    
ncsshd           : Running    
dmiauthd         : Running    
nginx            : Running    
ndbmand          : Running    
pubd             : Running    

```

- More information:

[restconf-configuration](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/1717/b_1717_programmability_cg/m_1717_prog_restconf.html#id_125840)

#### Cisco DevNet

- Examples and tools discussed are available for use and practice at Cisco DevNet (https://developer.cisco.com)

- Network operators who are looking to enhance or increase their skills with APIs, coding, Python or even controller concepts can find a wealth of help at DevNet

- At DevNet it is easy to find learning labs and content to help solidify current knowledge of network programability 

![devnet-home-page](./devnet-home-page.png)

- High level overview of DevNet

- Options for the home page:

    - Documentation

    - Learn

    - Technologies

    - Community

    - Events

##### Documentation

- The documentation page is a single place to get information on API documentation for a variety of solutions such as Cisco DNA center, Cisco SD-WAN, IoT, Collaboration, and more

- The API references provide information on how to programatically interact with these solutions

- This is a great place to start when learning how to interact with devices and software-defined controllers

##### Learn

- The Learn page is where you can navigate the different offerings that DevNet has available

- Under this tab are subsections for guided learning tracks, which guide you through various technologies and the associated API labs

- Some of the labs you interact with are Programming the Cisco Digital Network Architecture (DNA), ACI programming, Getting started with Cisco WebEx teams APIs, and Introduction to DevNet

- When you choose a learning lab and start a module, the website tracks all your progress so you can go away and come back and continue where you left off

- This is helpful to continue your education over the course of multiple days or weeks

##### Technologies

- The Technologies page allows you to pick relevant content based on the technology you want to study and dive directly into the associated labs and training for that technology

- Networking content currently available

![network-technologies-available](./networking-technologies-available-devnet.png)

##### Community

- Perhaps one of the most important sections of DevNet is the Community page

- This is where users have access to many different people at various stages of learning

- DevNet ambasadors and evangelists are available to help at various stages of your learning journey

- The Community page puts the latest events and news at your fingertips

- This is also the place to read blogs, sign up for developer forums, and follow DevNet on all major social media platforms

- This is a safe zone for asking questions, simple or complex

- The DevNet community page is the place to start for all things Cisco and Network Programmability

- Below are shown some of the available options for users on the Community page

##### Events

- The DevNet events page, provides a full list of events that have happened in the past or that will be happening in the future

- This is where a user can find the upcoming DevNet Express events as well as conferences where DevNet will be presenting

### GitHub

- One of the most efficient and commonly adopted ways of using version control is by using GitHub

- GitHub is a hosted web-based repository for code

- It has capabilities for bug tracking and task management as well

- Using GitHub is one of the easiest ways to track changes in your files, collaborate with other developers, and share code with the online community

- It is a great place to look for code to get started on programmability

- Often times, other engineers or developers are trying to accomplish similar tasks and have already created and tested the code necessary to do so

- One of the most powerful features of using GitHub is the ability to rate and provide feedback on other developers' code

- Peer review is encouraged in the coding community

- GitHub provides a guide that steps through how to create a repository, start a branch, add comments, and open a pull request

- You can also just start a GitHub project when you are more familiar with the GitHub tool and it's associated processes

- Projects are repositories that contain code files

- GitHub provides a single pane to create, edit, and share code files

- Below is shown a repository that contains three files:

    - ENCORE.txt

    - JSON_Example.txt

    - README.md

![github-encore-repo](./github-encore-repo.png)

- GitHub also gives a great summary of commit logs, so when you save a change in one of your files or create a new file

- GitHub shows details about it on the main repository page

- If you drill down into one of the files in the repository, you can see how easy it is to edit and save code

- If you drill down into JSON_Example.txt, for example, GitHub shows it's contents and how to edit the file in the repository

- If you click the filename JSON_Example.txt, you can see that the file has seven lines of code and is 77 bytes in size

- Below is shown the content of the JSON_Example.txt file and the options available with the file

![json-example-file](./json-example-file-github.png)

- The pencil allows you to go into editing mode and modify the file content

- This editor is very similar to any other text editor

- You can simply type into the editor or copy and paste files from other files directly into it

- Below we can see the addition of another user called Zuul

- If the code were to be committed, the changes in the file could be saved with the new user added to the file

- Now that the file is available in the repository, other GitHub users and developers can contribute to this code or add and delete lines of code based on the code that was originally created

- For example, if a user has some code to to add a new user via JSON syntax, someone could use that code and simply modify the usernames or add the code to enhance it

- This is the true power of sharing code

### Basic Python Components and Scripts

- **Python** has by a longshot become one of the most common programming languages in therms of network programmability

- Learning to use programming languages can be daunting

- Python is one of the easiest languages to get started with and interpret

- We will see how to build some of the fundamental skills necessary to be able to interpret Python scripts

- When you understand the basics of interpreting what a Python script is designed to do, it will be easier to understand and leverage other scripts that are available

- GitHub has some amazing Python scripts available for download that come with very detailed instructions and documentation

- Now we can leverage the new knowledge gained about APIs, HTTP operations, DevNet, and GitHub

- Below is shown a Python script that sets up the environment to log in to the Cisco DNA Center sandbox

- This script uses the same credentials used with the Token API used earlier in this chapter

- Env_Lab.py

```py
""" Set the environment information needed to access your lab

The provided sample code in this repository will reference this file to get 
the information needed to connect to your lab backend. You provide this info here once
and the scripts in this repository will access it as needed by the lab

(...)

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
```

- The Env_Lab.py python script starts with three quotation marks

- These three quotation marks begin and end a multiline string

- A string is simply one or more alphanumeric characters

- A string can comprise many numbers or letters, depending on the Python version in use

- In the case of this script, the creator used a multiple-line to put additional overall comments into the script

- This is not mandatory, but you can see that comments are helpful

- The # character indicates a comment in the Python script file

- Some comments usually describe the intent of an action within the code

- Comments often appear right above the action they describe

- Some scripts have a comment for each option, and some are not documented very well, if at all

- The comments in the Env_Lab.py indicate that there are three available options for selecting the lab environment to use:

    - **Sandbox**: The line in this python script that says ENVIRONMENT_IN_USE = "sandbox", corresponds with the selection of the sandbox type of lab environments available throug Cisco DevNet

    - In this instance, "sandbox" refers to the always-on and reserved sandboxes that can be accessed through https://developer.cisco.com

    - **Express**: This is the back end that is used for the DevNet Express Events that are held globally at various locations and Cisco office locations

    - **Custom**: This is used in the event that there is already a Cisco DNA Center installed either in a lab or other facility, and it needs to be accessed using this script

- As you can see in the python script, a few variables are used to target the DevNet Cisco DNA Center sandbox specifically:

```
Variable                        Value                                   Description

host                            sandboxdnac.cisco.com                   Cisco DNA Center sandbox URL

port                            443                                     TCP port to access the URL securely (HTTPS)

username                        devnetuser                              Username to log in to Cisco DNA Center sandbox (via API or GUI)

password                        Cisco123!                               Password to log in to Cisco DNA Center sandbox (via API or GUI) 
```

- The variables shown should look familiar as they are similar to the JSON data format

- Remember that JSON uses key/value pairs and is extremely easy to read and interpret

- In the script you can see the key/value pair "username": "devnetuser" 

- The structure used to hold all the key/value pairs in this script is called dictionary

- In this particular python script, the dictionary is named dnac

- The dictionary named dnac contains multiple key/value pairs, and it starts and ends with curly braces ({})

```py
dnac = {
    "host": "sandboxdnac.cisco.com",
    "port": 443,
    "username": "devnetuser",
    "password": "Cisco123!"
}
```

- Dictionaries can be written in multiple different ways

- Whereas above is shown a multi-line dictionary that is easy redable, below is shown the same dictionary written as a single line:

```py
dnac = {"host": "sandboxdnac.cisco.com", "port": 443, "username": "devnetuser", "password": "Cisco123!"}
```

- Notice that the line `ENVIRONMENT_IN_USE = "sandbox"` is used in this script

- Following that line in the script there is a line that states `if ENVIRONMENT_IN_USE = "sandbox":`

- This is called a condition (if statement)

- A logical if question is asked, and depending on the answer, an action happens

- In this exammple, the developer called out to use the sandbox option with the line of code `ENVIRONMENT_IN_USE = "sandbox"` and then used a condition to say that if the environment in use is sandbox, call a dictionary called dnac to provide the sandbox details that are listed in key/value pairs

- Below is shown the two relevant lines of code to illustrate this

- Now let's look at a script that showcases much of the API information that was covered above and also builds on all the basic Python information that has just been provided

- Python script is called get_dnac_devices.py

```py
# specifies what version and interpreter of python will be used
#!/usr/bin/env python3

# Calls dnac dictionary from the Env_Lab.py script covered earlier
from Env_Lab import dnac
# Imports the json module so that python can understand the data format that contains key/value pairs
import json
# Imports requests module which handle HTTP headers and form data
import requests
# Imports urllib3 module which is an HTTP client
import urllib3
# Imports HTTPBasicAuth method from the requests.auth module to handle authentication with username and password
from requests.auth import HTTPBasicAuth
# Imports prettytable components from PrettyTable module to structure return data in table format
from prettytable import PrettyTable

# Puts return data into a easily readable table with the specified column names 
dnac_devices = PrettyTable(["Hostname", "Platform ID", "Software Type", "Software Version", "Series", 
                            "IP address", "Up Time"])

dnac_devices.padding_width = 1

# Silence the insecure warnings due to SSL Certificates

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Sends specific HTTP headers when issuing HTTP GET to the Network Devices API
headers = {
    "content-type": "application/json",
    "x-auth-token": ""
}


# Get token from DNAC Token API
# This function does an HTTP POST request to the DNAC Token API and uses the
# values built in the key/value pair  formats taken from Env_Lab.py script
# The response is stored as the token that is used to make future API calls
# for the authenticated user
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

```

- It might seem like there is a lot going on in the get_dnac_device.py script

- However many of the details have already been explained

- The first section of code tells the Python interpreter what modules this particular script will use

- Think of a module as a collection of actions and instructions

- To better explain the content, comments are inserted throughout the script to help document each section

- Modules help Python understand what it is capable of

- For example, if a developer tried to do a HTTP GET request without having the requests modules imported, it would be difficult for python how to interpret the HTTP call

- Although there are other ways of doing HTTP calls from python, the requests modules greatly simplify the process

- Functions are blocks of code that are built to perform specific actions

- Functions are very structured in nature and can often be reused later on within a Python script

- Some functions are built into Python and do not have to be created

- A great example of this is the print function which can be used to print data to a terminal screen

- You can see the print function at the end of our script

- Remember that in order to execute any API calls to Cisco DNA Center you must be authenticated using the Token API

- The dnac_login function is used to get the token information from the token API, as we have seen in Postman/Bruno earlier, and be used to make requests to any DNA Center API after this

- The network_device_list function ties the Token API to the Network Device API call to retrieve the information from the Cisco DNA Center

- The line that says `headers["x-auth-token"] = token` is mapping the JSON response from the previous function, which is the token, into the header called x-auth-token

- In addition, the URL for the API was changed to network_device, and the response is sending a requests.get to that URL

- This is exactly the same example made with Postman/Bruno earlier

- The final section of the get_dnac_devices function shows code that ties together the dnac dictionary to the dnac_login function

- In addition, the print function takes the response received from the response.get that was send to the network device API, and puts it into the table format that was specified with the name dnac_devices

- The Python script examples from above makes it easy to see the power and easy-to-use nature of Python

- The tools mentioned here, including Bruno and Python are readily available on the Internet for free

- A great way to practice is by using a sandbox environment and just building code and running it to see what can be accomplished

- You are only limited by your imagination and coding skills
