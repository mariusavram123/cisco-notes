## Authenticating Wireless Clients

1. Open Authentication

2. Authenticating with Pre-Shared Key

3. Authenticating with EAP

4. Authenticating with WebAuth

- Wireless networks can leverage many technologies and protocols and protect the information that is sent over the air

- For example, the WPA, WPA2 and WPA3 security suites can be used to protect data privacy and integrity

- Beyond that, it is also important to identify the two endpoints (the AP and the client device) that use a wireless connection, as well as the end user

- To join and use a wireless network, wireless clients must first discover a basic service set (BSS) and then request permission to associate with it

- At that point, clients should be authenticated by some means before they can become functioning members of a wireless LAN. Why?

- Suppose that your wireless network connects to corporate resources where confidential information can be accessed

- In that case, only devices known to be trusted and expected should be given access

- Guest users, if they are permitted at all, should be allowed to join a different guest WLAN where they can access nonconfidential or public resources

- Rogue clients, which are not expected or welcomed, should not be permitted to associate at all

- After all, they are not affiliated with the corporate network and are likely to be unknown devices that happens to be within range of your network

- To control access, wireless networks can authenticate the client devices before they are allowed to associate

- Potential clients must identify themselves by presenting some form of credentials to the APs

- Below is shown a basic client authentication process

![basic-client-auth](./basic-client-auth.png)

- Wireless authentication can take many forms

- Some methods require only a static text string that is common across all trusted clients and APs

- The text string is stored on the client device and is presented directly to the AP when needed

- What might happen if the device is stolen or lost?

- Most likely, any user who possesses the device would still be able to authenticate to the network

- One more stringent authentication methods require interaction with a corporate user database

- In those cases, the end user must enter a valid username and password - something that would not be known to a thief or an imposter

- Below are presented four types of client authentication that can be enountered in the real world

- With each type, you can begin by creating a new WLAN on the wireless LAN controller, assigning a controller interface and enabling the WLAN

- Because wireless security is configured on a per-WLAN basis, all of the configuration tasks will occur in the WLAN -> Edit security tab

### Open Authentication

- Recall that a wireless client device must send 802.11 authentication request and association request frames to an AP when it asks to join a wireless network

- The original 802.11 standard offered only two choices to authenticate a client: Open Authentication and WEP

- Open Authentication is true to it's name; it offers open access to a WLAN 

- The only requirement is that a client must use an 802.11 authentication request before it attempts to associate with an AP

- No other credentials are needed

- When would you want to use open authentication? 

- After all it does not sound very secure (and it is not)

- With no challenge, any 802.11 client may authenticate to access the network

- That is, in fact the whole purpose of Open Authentication - to validate that a client is a valid 802.11 device by authenticating the wireless hardware and the protocol

- Authenticating the user's identity is handled as a true security process through other means

- You have probably seen a WLAN with Open Authentication when you have visited a public location

- If any client screening is used at all, it comes in the form of Web Authentication (WebAuth) which is described later

- A client can associate right away but must open a web browser to see and accept the terms for use and enter basic credentials

- From that point, network access is opened up for the client

- To create a WLAN with Open Authentication on a IOS XE WLC, you can navigate to Configuration -> Wireless Setup -> WLAN wizard

![wlan-wizard](./wlan-wizard-wlc.png)

- You can also create a WLAN directly from Configuration -> Tags and profiles -> WLANs -> Add

![add-wlan-mode2](./add-wlan-mode2.png)

- Under the General tab enter the SSID string, then select the Security tab to configure WLAN security and user authentication parameters

- Select Layer 2 and then use the Layer 2 Security Mode dropdown menu to select None for Open Authentication, as shown below

- In this example the WLAN is named 'guest' and the SSID is 'Guest'

![open-auth-wlan](./l2-none-security.png)

- Then click the 'Apply to device' button

- Don't forget that you still have to configure a policy profile to identify the appropriate VLAN number that the WLAN will map to and then apply the WLAN an Policy profiles to the AP

- You can verify the WLAN and it's security settings from the list of of WLANs shown under Configuration -> Tags and profiles -> WLANs

- The security is shown as [open]

- You can also verify the WLAN status is enabled and active

![verify-wlans](./verify-WLANs.png)

- Set a policy profile and associate it with a WLAN

![policy-profile-vlan](./policy-profile-assign-vlan.png)

- Add site tag

- Configuration -> Tags and Profiles -> Tags -> Site

![site-tag](./add-site-tag.png)

- Add a policy tag

- Configuration -> Tags and Profiles -> Tags -> Policy

![add-policy-tags](./add-policy-tag.png)

- (click on the check mark to add it to the AP)

- Assign policy tag to the policy profile added early

- Configuration -> Tags and Profiles -> Tags -> Edit a tag -> Set WLAN profile and Policy profile

![policy-maps](./wlan-policy-maps.png)

- Assign the profiles to the AP

- Configuration -> Tags and profiles -> Tags -> AP -> Assign policy tag, site tag and the RF tag to the AP

![](./assign-tags-to-ap.png)

- Do not forget to "save configuration"

![save-configuration](./save-configuration.png)

- UPDATE- To set this WLAN correctly you have to configure the VLAN in the Policy profile -> Access Policy tab as the VLAN you want the Clients to be part on

![set-correct-vlan-nt](./set-correct-vlan-nr.png)

- Network topology

![topology-wireless-lab](./topology-wireless-lab.png)


### Authenticating with Pre-Shared Key

- To secure wireless connections on a WLAN, you can leverage one of Wi-Fi Protected Access (WPA) versions - WPA (also known as WPA1), WPA2 or WPA3

- Each version is certified by the Wi-Fi Aliance so that wireless clients and APs using the same version are known to be compatible

- The WPA versions also specify encryption and data integrity methods to protect data passing over the wireless connections

- All three WPA versions support two client authentication modes, preshared key (PSK) or 802.1X, depending on the scale of the deployment

- These are also known as Personal mode and Enterprise mode, respectively

- With personal mode, a key string must be shared or configured on every client and AP before the clients can connect to the wireless network

- The pre-shared key is normally kept confidential so that unauthorized users have no knowledge of it

- The key string is never sent over the air

- Instead, clients and APs work through a four-way handshake procedure that uses the pre-shared key string to construct and exchange encryption key material that can be openly exchanged 

- When that process is successful, the AP can authenticate the client, and the two can secure data frames that are sent over the air

- With WPA-Personal and WPA2-Personal modes, a malicious user can eavesdrop and capture the four-way handshake between a client and an AP

- That user then can use a dictionary attack to automate the guessing of the pre-shared key

- If the malicious user is successful, that user can then decrypt the wireless data or even join the network, posing as a legitimate user

- WPA3-Personal avoids such an attack by strengthening the key exchange between the clients and APs through a method known as Simultaneous Authentication of Equals (SAE)

- Rather than a client authenticating against a server or AP, the client and AP can initiate the authentication process equally and even simultaneously

- Even if a password or key is compromised, WPA3-Personal offers forward secrecy which prevents attackers from being able to use a key to unencrypt data that has already been transmitted over the air

- The personal mode of any WPA version is usually easy to deploy in a small environment or with clients that are embedded in certain devices because a simple key string is all that is needed to authenticate the clients

- Be aware that every device using the WLAN must be configured with an identical pre-shared key, unless PSK with Identity Services Engine (ISE) is used

- If you ever need to update or change the key, you must touch every device to do so

- In addition, the pre-shared key should remain a well-kept secret; you should never divulge the pre-shared key to any unauthorized person

- To maximize security, you should use the highest WPA version available on the WLCs, APs and client devices in your network

- You can configure WPA2 or WPA3 personal mode and the pre-shared key in one step

- Configuration -> Tags and Profiles -> WLANs and select Add or select an existing WLAN to edit

- Make sure the parameters on the General tab are set appropriately

- Next, select the Security -> Layer 2 in tabs 

- In the Layer 2 security mode drop-down menu, select the appropriate WPA version for the WLAN

![add-wlan-devices](./add-wlan-devices.png)

- Under WPA + WPA2 parameters, the WPA version has been narrowed down to only WPA2 by unchecking the box next to WPA policy and checking both WPA2 policy and WPA2 encryption AES

![wpa2-personal-security](./wlan-wpa2-security.png)

- Next add devices policy tag and map it to WLAN and policy profile

![devices-policy-tag](./add-devices-policy-tag.png)

- Next assign tags to AP

![assign-tags-to-ap](./assign-tags-to-ap2.png)

- For WPA2 personal mode, look under the Auth Key Mgmt section and check only the box next to PSK

- You should then enter the Pre-Shared key string in the box next to Pre-Shared key

- An ASCII text string has been entered

- Be sure to click the "Apply to device" button to apply the WLAN changes you have made

- Settings on a WLAN for WPA2 and WPA3 policy with SAE

![wpa2-wpa3-personal](./wpa2-wpa3-personal-auth.png)

- The controller allows you to enable both WPA and WPA2 checkboxes

- You should do that only if you have legacy clients that require WPA support and are mixed in with newer WPA2 clients

- Be aware that the WLAN will only be as secure as the weakest security suite you configure on it

- Ideally, you should use WPA2 or WPA3 with AES/CCMP and try to avoid any other hybrid mode

- Hybrid modes such as WPA with AES and WPA2 with TKIP can cause compatibility issues; in addition, they have been deprecated

- You can verify the WLANs and their security settings from Configuration -> Tags and Policies -> WLANs

- The security column for the "devices" WLAN is shown as [WPA2][PSK][AES]

![wlan-security-modes](./wlan-security-modes.png)

- For the WPA2+WPA3 authentication the security is shown as [WPA2 + WPA3][PSK][SAE][AES]

- You can also verify the WLAN status is enabled and active

### Authenticating with EAP
