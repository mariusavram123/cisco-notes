## Network Access Control

- Here we can see multiple network access control (NAC) technologies, such as 802.1X, MAC Authentication Bypass (MAB), and Web Authentication (WebAuth), as well as next-generation NAC technologies such as TrustSec and MACSec

### 802.1x

- IEEE 802.1x (referred to as Dot1x) is a standard for port-based network access control (PNAC) that provides an authentication mechanism for local area networks (LANs) and wireless local area networks (WLANs)

- 802.1x comprises the following components:

    - **Extensible Authentication Protocol (EAP)**: This message format and framework, defined by RFC 4187, provides an encapsulated transport for authentication parameters

    - **EAP method (also referred to as EAP type)**: Different authentication methods can be used with EAP

    - **EAP over LAN (EAPoL)**: This Layer 2 encapsulation protocol is defined by 802.1x for the transport of EAP messages over IEEE 802 wired and wireless networks

    - **RADIUS protocol**: This is the AAA protocol used by EAP

- 802.1x devices have the following roles:

    - **Supplicant**: Software on the endpoint communicates and provides identity credentials through EAPoL with the authenticator

    - Common 802.1x supplicants include Windows and macOS native supplicants as well as Cisco Secure Client

    - All these supplicants support 802.1x machine and user authentication

    - **Authenticator**: A network access device (NAD) such as a switch or wireless LAN controller (WLC), controls access of the user based on the authentication status of the user or endpoint

    - The authenticator acts as the liaison, taking the Layer 2 EAP-encapsulated packets from the supplicant and encapsulating them into RADIUS packets for delivery to the authentication server

    - **Authentication server**: A RADIUS server performs authentication of the client

    - The authentication server validates the identity of the endpoint and provides the authenticator with an authentication result, such as accept or deny

- 802.1x users and roles can be seen below

![8021x-roles-components](./8021x-roles-components.png)

- The EAP identity exchange occur between the supplicant and the authentication server

- The authenticator has no idea what EAP type is in use; it simply takes the EAPoL encapsulated frame from the supplicant and encapsulates it withing the RADIUS packet sent to the authentication server and then opens up the port if the authentication server directs it to

- Therefore, the EAP authentication is completely transparent to the authenticator

- Below is seen the process flow of a successful 802.1x authetication

- Below we can see the following steps being performed:

    1. When the authenticator notices a port coming up, it starts the authentication process by sending periodic EAP request/identity frames

    - The supplicant can also initiate the authentication process by sending an EAPoL-start message to the authenticator

    2. The authenticator relays EAP messages between the supplicant and the authentication server, copying the EAP message in the EAPoL frame to an AV-pair inside the RADIUS packet and vice versa until an EAP method is selected
    
    - Authentication then takes place using the selected EAP method

    3. If authentication is successful, the authentication server returns a RADIUS access-accept message with an ecapsulated EAP-success message, as well as an authorization option such as a downloadable ACL (dACL)

    - When this is done, the authenticator opens the port

![successful-8021x-auth-flow](./successful-8021x-authentication-flow.png)

### EAP methods

- Many different EAP methods are available, most of them based on Transport Layer Security (TLS)

- Which one to choose depends on the security requirements and the EAP methods supported by the supplicants and the authentication server

- The following are the most commonly used EAP methods:

    - EAP challenge-based authentication method:

        - Extensible Authentication Protocol - Message Digest 5 (EAP-MD5)

    - EAP TLS authentication method:

        - Extensible Authentication Protocol - Transport Layer Security (EAP-TLS)

    - EAP tunelled TLS authentication methods:

        - Extensible Authentication Protocol Flexible Authentication via Secure Tunneling (EAP-FAST)

        - Extensible Authentication Protocol Tunnelled Transport Layer Security (EAP-TTLS)

        - Protected Extensible Authentication Protocol (PEAP)

    - EAP inner authentication methods:

        - EAP Generic Token Card (EAP-GTC)

        - EAP Microsoft Challenge Handshake Authentication Protocol Version 2 (EAP-MSCHAPv2)

        - EAP TLS

- EAP inner authentication methods are tunneled within PEAP, EAP-FAST, and EAP-TTLS, which are also known as *outer or tunneled TLS authentication methods*

- Tunneled TLS authentication methods establish a TLS outer tunnel between the supplicant and the authentication server; after the encrypted tunnel is established, client authentication credentials are negotiated using one of the EAP inner methods within the TLS outer tunnel

- This tunneling authentication method is similar to the way an HTTPS session is established between a web browser and a secure website (such as a bank's website)

- The HTTPS TLS tunnel is formed after the web browser validates the authenticity of the website's certificate (one-way trust), and when the TLS tunnel is established, the user can enter the login credentials on the website through the secure TLS tunnel

- Following is a description of each of the EAP authentication methods:

    - **EAP-MD5**: Uses MD5 message-digest algorithm to hide the credentials in a hash

    - The hash is sent to the authentication server, where it is compared to a local hash to validate the accuracy of the credentials

    - EAP-MD5 does not have a mechanism for mutual authentication; in other words, the authentication server validates the supplicant, but the supplicant does not validate the authentication server to see if it is trustworthy

    - This lack of mutual authentication makes it a poor choice as an authentication method

    - **EAP-TLS**: Uses the TLS Public Key Infrastructure (PKI) certificate authentication mechanism to provide mutual authentication of supplicant to authentication server and authentication server to supplicant

    - With EAP-TLS, both the supplicant and the authentication server must be assigned a digital certificate signed by a certificate authority (CA) that they both trust

    - Because the Supplicant also requires a certificate, this is the most secure authentication method; however it is also the most difficult to deploy due to the administrative burden of having to install a certificate on the supplicant side

    - **PEAP**: in PEAP, only the authentication server requires a certificate, which reduces the administrative burden of implementing EAP

    - PEAP forms an encrypted TLS tunnel between the supplicant and the authentication server

    - After the tunnel has been established, PEAP uses one of the following authentication inner methods to authenticate the supplicant through the outer PEAP TLS tunnel:

        - **PEAP-MSCHAPv2 (PEAPv0)**: Using this inner method, the client's credentials are sent to the server encrypted within an MSCHAPv2 session

        - This is the most common inner method, because it allows for simple transmission of username and password, or even computer name and computer password, to the RADIUS server, which can then authenticate them using Microsoft's Active Directory

        - **EAP-GTC (PEAPv1)**: This inner method was created by Cisco as an alternative to MSCHAPv2 to allow generic authentication to virtually any identity store, including OTP token servers, LDAP, NetIQ eDirectory, and more

        - **EAP-TLS**: This is the most secure EAP authentication method since it is essentially a TLS tunnel within another TLS tunnel

        - It is rarely used due to it's deployment complexity because it requires certificates to be installed on the supplicants

        - **EAP-FAST**: EAP-FAST, which is similar to PEAP, was developed by Cisco Systems as an alternative to PEAP to allow for faster reauthentications and support for faster wireless roaming

        - Just like PEAP, EAP-FAST forms an TLS outer tunnel and then transmits the client authentication credentials within that TLS tunnel

        - A major difference between FAST and PEAP is the FAST's ability to re-authenticate faster using the protected access credentials (PACs)

        - A PAC is similar to a secure cookie, stored locally on the host, as "proof" of a successful authentication

        - EAP-FAST also supports EAP chaining

        - **EAP-TTLS**: EAP-TTLS is similar in functionality to PEAP but is not as widely supported as PEAP

        - One major difference between them is that PEAP only supports EAP inner authentication methods, while EAP-TTLS can support additional inner methods such as legacy Password Authentication Protocol (PAP), Challenge Handshake Authentication Protocol (CHAP), and Microsoft Challenge Handshake Authentication Protocol (MSCHAP)

#### EAP Chaining

- EAP-FAST includes the option of EAP chaining, which supports machine and user authentication inside a single TLS tunnel

- It enables machine and user authentication to be combined into a single overall authentication result

- This allows the assignment of greater privileges or posture assessments to users who connect to the network using corporate-managed devices

### MAC Authentication Bypass (MAB)

- **MAC Authentication Bypass (MAB)** is an access control technique that enables port-based access control using the MAC address of an endpoint, and it is typically used as a fallback mechanism to 802.1x

- A MAB-enabled port can be dynamically enabled or disabled based on the MAC address of the endpoint that connects to it

- Below is illustrated the process flow of a successful MAB authentication

![successful-mab](./successful-mab.png)

- Steps outlined in the image are the following:

    1. The switch initiates authentication by sending an EAPoL identity request message to the endpint every 30 seconds by default

    - After three timeouts (a period of 90 seconds by default), the switch determines that the endpoint does not have a supplicant and proceeds to authenticate it via MAB

    2. The switch begins MAB by opening the port to accept a single packet from which to learn the source MAC address of the endpoint

    - Packet sent before the port has fallen back to MAB (that is during the IEEE 802.1x timeout phase) are discarded immediately and cannot be used to learn the MAC address

    - After the switch learns the source MAC address, it discards the packet

    - It crafts a RADIUS access-request message using the endpoint's MAC address as the identity

    - The RADIUS server receives the RADIUS access-request message and performs MAC authentication

    3. The RADIUS server determines whether the device should be granted access to the network and, if so, what level of access to provide

    - The RADIUS server sends the RADIUS response (access-accept) to the authenticator, allowing the endpoint to access the network

    - It can also include authorization options such as dACLs, dVLANs, and SGT tags

- If 802.1x is not enabled, the sequence is the same except that MAB authentication starts immediately after linkup, instead of waiting for 802.1x to time out

- MAC addresses can be easily spoofed, which means any endpoint can be configured to use a MAC address other than the burned-in address

- For this reason, MAB authenticated endpoints should be given very restricted access and should only be allowed to communicate to the networks and services that the endpoints are required to speak to

- If the authenticator is a Cisco switch, then many authorization options can be applied as part of the authorization result from the authentication server, including the following:

    - Downloadable ACLs (dACLs)

    - Dynamic VLAN assignment (dVLAN)

    - Security Group Tags (SGT) tags

### Web Authentication (WebAuth)

- In an organization, endpoints that try to connect to the network might not have 802.1x supplicants and might not know the MAC address to perform MAB

- These endpoints can be employees and contractors with misconfigured 802.1x settings that require access to the corporate network or visitors and guests that need access to the Internet

- For these cases, Web Authentication (WebAuth) can be used

- WebAuth, like MAB, can be used as a fallback authentication mechanism for 802.1x

- If both MAB and WebAuth are configured as fallbacks for 802.1x, when 802.1x times out, a switch first attempts to authenticate through MAB, and if it fails, the switch attempts to authenticate with webauth

- With WebAuth, endpoints are presented with a web portal requesting a username and password

- The username and password that are submitted through the web portal are sent from the switch (or wireless controller, firewall, and so on) to the RADIUS server in a standard RADIUS access-request packet

- In a similar way to what occurs with MAB, the switch sends the request on behalf to the endpoint, to the RADIUS server because the endpoint is not authenticating directly to the switch

- Unlike MAB, WebAuth is only for users and not devices because it requires a web browser and manual username and password entry

- There are two types of WebAuth:

    - Local Web Authentication

    - Centralized Web Authentication with Cisco ISE

#### Local Web Authentication

- Local Web Authentication (LWA) is the first form of Web Authentication that was created

- For this type of WebAuth, the switch (or wireless controller) redirects the traffic (HTTP and/or HTTPS) to a locally hosted web portal running on the switch where an end user can enter a username and a password

- When the login credentials are submitted through the web portal, the switch sends a RADIUS access-request message, along with the login credentials to the RADIUS server

- It is important to remember that when the switch sends the login credentials on behalf of the user, it is considered to be LWA

- On Cisco switches, the LWA web portals are not customizable

- Some organizations require that the web portals be customized to match their corporate branding

- For those companies, LWA is not an acceptable solution

- In addition, with the Cisco switches, there is no native support for advanced services such as acceptable use policy (AUP) acceptance pages (for example, a popup requesting acceptance of terms and conditions before access is allowed), password changing capabilities, device registration, and self-registration

- For those advanced capabilities, a centralized web portal is required

- LWA does not support VLAN assignment; it supports only ACL assignment

- It also doesn't support the change of authorization (CoA) feature to apply new policies; therefore, access policies cannot be changed based on posture or profiling state, and even administrative changes cannot be made as a result of malware to quarantine the endpoint

- Cisco switches and a variety of third-party 802.1x-compliant switches have the option to assign a guest VLAN to endpoints that don't have an 802.1x supplicant

- Many production deployments of 802.1x still use this legacy option to provide wired guests access to the Internet; however, it is important to note that guest VLAN and LWA are mutually exclusive

#### Central Web Authentication with Cisco ISE

- Cisco created Centralized Web Authentication (CWA) to overcome LWA's deficiencies

- CWA supports CoA for posture profiling as well as dACL and VLAN authorization options

- CWA also supports all the advanced services, such as client provisioning, posture assessments, acceptable use policies, password changing, self-registration, and device registration

- Just like LWA, CWA is only for endpoints that have a web browser, where the user can manually enter a username and a password

- With CWA, WebAuth and guest VLAN functions remain mutually exclusive

- Authentication with CWA is different from authentication for LWA

- Step details for how CWA authentication takes place:

    1. The endpoint entering the network does not have a configured supplicant or the supplicant is misconfigured

    2. The switch performs MAB, sending the RADIUS access-request to Cisco ISE (the authentication server)

    3. The authentication server (ISE), sends the RADIUS result, including a URL redirection, to the centralized portal on the ISE server itself

    4. The endpoint is assigned and IP address, DNS server, and default gateway using DHCP

    5. The end user opens a browser and enters credentials into the centralized web portal

    - Unlike with LWA, the credentials are stored in ISE and are tied together with the MAB coming from the switch

    6. ISE sends a re-authentication change of authorization (CoA-reauth) to the switch

    7. The switch sends a new MAB request with the same session ID to ISE

    - ISE sends the final authorization result to the switch for the end user, including an authorization option such as downloadable ACL (dACL)

### Enhanced Flexible Authentication (FlexAuth)

- By default, a Cisco switch configured with 802.1x, MAB and WebAuth always attempts 802.1x authentication first, followed by MAB, and finally WebAuth

- If an endpoint that does not support 802.1x tries to connect to the network, it needs to wait for a considerable amount of time before WebAuth is oferred as an authentication option

- Enhanced FlexAuth (also referred to as *Access Session Manager*) addresses this problem by allowing multiple authentication methods concurently (for example, 802.1x and MAB) so that endpoints can be authenticated and brought online more quickly

- Enhanced FlexAuth is a key component of the Cisco Identity-based Networking Services (IBNS) 2.0 integration solutions, which offers authentication, access control, and user policy enforcement

### Cisco Identity-Based Networking Services (IBNS) 2.0

- Cisco IBNS 2.0 is an integrated solution that offers authentication, access control, and user policy enforcement with a common end-to-end access policy that applies to both wired and wireless networks

- It is a combination of the following existing features and products:

    - Enhanced FlexAuth (Access Session Manager)

    - Cisco Common Classification Policy Language (C3PL)

    - Cisco ISE

### Cisco TrustSec

- **Cisco TrustSec** is a next-generation access control enforcement solution developed by Cisco to address the growing operational challenges of traditional network segmentation using VLANs and maintaining firewall rules and ACLs using Security Group Tags (SGT) tags

- TrustSec uses SGT tags to perform ingress tagging and egress filtering to enforce access control policy

- 