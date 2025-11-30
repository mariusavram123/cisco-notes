### Control Plane Policing (CoPP)

- A **control plane policing (CoPP)** policy is a QoS policy that is applied to traffic to or sourced by the router's control plane CPU

- CoPP policies are used to limit known traffic to a given rate while protecting the CPU from unexpected extreme rates of traffic that could impact the stability of the router

- Typically CoPP implementations use only an input policy that allows traffic to the control plane to be policed to a desired rate

- In a properly planned CoPP policy, network traffic is placed into various classes, based on the type of traffic (management, routing protocols or known IP addresses)

- The CoPP policy is then implemented to limit traffic to the control plane CPU to a specific rate for each class

- When a rate is defined for a CoPP policy, the rate for a class may not be known without further investigation

- The QoS `police` command uses `conform`, `exceed` and `violate` actions, which can be configured to transmit or drop traffic

- By choosing to transmit traffic that exceeds the policed rate and monitor CoPP, you can adjust the policy over time to meet day-to-day requirements

- Understanding what is needed to define a traffic class can be achieved from protocol documentation or by performing network protocol analysis

- You can use the Cisco Embedded Packet Capture (EPC) feature for this purpose because it allows you to capture network traffic and export it to a PCAP file to identify the necessary traffic classes

#### Configuring ACLs for CoPP

- After the network traffic has been identified, ACLs can be built for matching in a class map

- Below are demonstrated a list of ACLs matching traffic identified by EPC and network documentation

- Notice that these ACLs do not restrict access and are open, allowing anyone to send traffic matching the protocols

- For some types of external network traffic (such as BGP), the external network address can change and is better managed from a ZBFW perspective

- A majority of these protocols are accessed only using controlled internal prefixes, minimizing the intrusion surface

- Management protocols are an area that can easily be controlled by using a few jump boxes for direct access and limiting SNMP and other management protocols to a specific range of addresses residing in the NOC

```
conf t
 ip access-list extended ACL-CoPP-ICMP
  permit icmp any any echo-reply
  permit icmp any any ttl-exceeded
  permit icmp any any unreachable
  permit icmp any any echo
  permit udp any any range 33434 33463 ttl eq 1

 ip access-list extended ACL-CoPP-IPsec
  permit esp any any
  permit gre any any
  permit udp any eq isakmp any eq isakmp
  permit udp any any eq non500-isakmp
  permit udp any eq non500-isakmp any

 ip access-list extended ACL-CoPP-Initialize
  permit udp any eq bootps any eq bootpc

 ip access-list extended ACL-CoPP-Management
  permit udp any eq ntp any
  permit udp any any eq snmp
  permit tcp any any eq 22
  permit tcp any eq 22 any established

 ip access-list extended ACL-CoPP-Routing
  permit tcp any eq bgp any established
  permit eigrp any host 224.0.0.10
  permit ospf any host 224.0.0.5
  permit ospf any host 224.0.0.6
  permit pim any host 224.0.0.13
  permit igmp any any
```

- The ACL-CoPP-Routing ACL does not classify unicast routing protocol packets such as unicast PIM, unicast OSPF and unicast EIGRP

#### Configuring Class Maps for CoPP

- The class configuration for CoPP uses the ACLs to match known protocols being used

```
conf t
 class-map match-all CLASS-CoPP-IPsec
  match access-group name ACL-CoPP-IPsec
 
 class-map match-all CLASS-CoPP-Routing
  match access-group name ACL-CoPP-Routing

 class-map match-all CLASS-CoPP-Initialize
  match access-group name ACL-CoPP-Initialize

 class-map match-all CLASS-CoPP-Management
  match acess-group name ACL-CoPP-Management

 class-map match-all CLASS-CoPP-ICMP
  match access-group-name ACL-CoPP-ICMP
```

#### Configuring the Policy Map for CoPP

- The policy map for how the classes operate shows how to police traffic to a given rate in order to minimize any ability to overload the router

- However, finding the correct rate without impacting network stability is not a simple task

- To guarantee that CoPP does not introduce issues, the `violate` action is set to `transmit` for all vital classes until a baseline for normal traffic flows is established

- Over time, the rate can be adjusted

- Other traffic, such as ICMP and DHCP traffic, is set to `drop` because it should have low packet rates

- Under normal conditions, nothing should exist with the class default, but allowing a minimal amount of traffic within the class and monitoring the policy permits discovery of new or unknown traffic that would have otherwise been denied

- Below is shown the CoPP policy:

```
conf t
 policy-map POLICY-CoPP
  class CLASS-CoPP-ICMP
   police 8000 conform-action transmit exceed-action transmit violate-action drop

  class CLASS-CoPP-IPsec
   police 64000 conform-action transmit exceed-action transmit violate-action transmit

  class CLASS-CoPP-Initialize
   police 8000 conform-action transmit exceed-action transmit violate-action drop

  class CLASS-CoPP-Management
   police 32000 conform-action transmit exceed-action transmit violate-action transmit

  class CLASS-CoPP-Routing
   police 64000 conform-action transmit exceed-action transmit violate-action transmit

  class class-default
   police 8000 conform-action transmit exceed-action transmit violate-action drop
```

- Keep in mind that the policy needs to be tweaked based on the routing protocols in use in the network

#### Applying the CoPP Policy Map

- The CoPP policy map needs to be applied to the control plane with the command `service-policy <input|output> <policy-name>` under control plane configuration mode

```
conf t
 control-plane
  service-policy input POLICY-CoPP
```

#### Verifying the CoPP Policy

- After the policy map has been applied to the control plane, it needs to be verified

- If the policy reports traffic exceeded and traffic is matching the default class, the policy should be adjusted

- To identify what is happening EPC should be used again to tweak the policies

- This time the access-lists can be reversed from the permit to deny as the filter to gather unexpected traffic

```
R2-COPP#show policy-map control-plane input 
 Control Plane 

  Service-policy input: POLICY-CoPP

    Class-map: CLASS-CoPP-ICMP (match-all)  
      0 packets, 0 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: access-group name CLASS-CoPP-ICMP
      police:
          cir 8000 bps, bc 1500 bytes, be 1500 bytes
        conformed 0 packets, 0 bytes; actions:
          transmit 
        exceeded 0 packets, 0 bytes; actions:
          transmit 
        violated 0 packets, 0 bytes; actions:
          drop 
        conformed 0000 bps, exceeded 0000 bps, violated 0000 bps

    Class-map: CLASS-CoPP-IPsec (match-all)  
      0 packets, 0 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: access-group name ACL-CoPP-IPsec
      police:
          cir 64000 bps, bc 2000 bytes, be 2000 bytes
        conformed 0 packets, 0 bytes; actions:
          transmit 
        exceeded 0 packets, 0 bytes; actions:
          transmit 
        violated 0 packets, 0 bytes; actions:
          transmit 
        conformed 0000 bps, exceeded 0000 bps, violated 0000 bps

    Class-map: CLASS-CoPP-Initialize (match-all)  
      0 packets, 0 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: access-group name ACL-CoPP-Initialize
      police:
          cir 8000 bps, bc 1500 bytes, be 1500 bytes
        conformed 0 packets, 0 bytes; actions:
          transmit 
        exceeded 0 packets, 0 bytes; actions:
          transmit 
        violated 0 packets, 0 bytes; actions:
          drop 
        conformed 0000 bps, exceeded 0000 bps, violated 0000 bps

    Class-map: CLASS-CoPP-Routing (match-all)  
      50 packets, 4652 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: access-group name ACL-CoPP-Routing
      police:
          cir 32000 bps, bc 1500 bytes, be 1500 bytes
        conformed 50 packets, 4652 bytes; actions:
          transmit 
        exceeded 0 packets, 0 bytes; actions:
          transmit 
        violated 0 packets, 0 bytes; actions:
          transmit 
        conformed 0000 bps, exceeded 0000 bps, violated 0000 bps

    Class-map: class-default (match-any)  
      21 packets, 5716 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: any 
      police:
          cir 8000 bps, bc 1500 bytes, be 1500 bytes
        conformed 21 packets, 5716 bytes; actions:
          transmit 
        exceeded 0 packets, 0 bytes; actions:
          transmit 
        violated 0 packets, 0 bytes; actions:
          drop 
        conformed 0000 bps, exceeded 0000 bps, violated 0000 bps
```

- Some Cisco platforms, such as the Catalyst 9000 series, have a default CoPP policy that typically does not require modification

- If a default CoPP policy needs to be modified, please consult the Cisco documentation for restrictions, caveats and configuration details specific to your platform

### Device Hardening

- In addition to all features shown until now, ACLs, AAA, CoPP and ZBFW on the routers, disabling unused services and features improves the overall security posture by minimizing the amount of information exposed externally

- In addition, hardening a router reduces the amount of router CPU and memory utilization that would be required to process these unnecessary packets

- Below is a list of additional commands that can be used to harden a router

- All interface-specific commands are applied only to the interface connected to the public network

- Consider the following device hardening measures:

    - **Disable topology discovery tools**: Tools such as Cisco Discovery Protocol (CDP) and Link Layer Discovery Protocol (LLDP) can provide unnecessary information to routers outside your control

    - The services can be desabled with the interface parameter commands:

    ```
    conf t
     interface <name>
      no cdp enable
      no lldp transmit
      no lldp receive
    ```

    - **Enable keepalives for TCP sessions**: Using the following commands:

    ```
    conf t
     service tcp-keepalives-in
     service tcp-keepalives-out
    ```

    - This ensures that the device sends TCP keepalives for inbound/outbound TCP sessions

    - This ensures that the device on the remote end of the connection is still accessible and that half-open or orphaned connections are removed from the local device

    - **Disable IP redirect services**: An ICMP redirect is used to inform a device about a better path to the destination network

    - An IOS XE device sends an ICMP redirect if it detects network traffic hairpinning to it

    - This behaviour is disabled with the interface parameter:

    ```
    conf t
     interface <name>
      no ip redirects
    ```

    **Disable Proxy Address Resolution Protocol (Proxy ARP)**: Proxy ARP is a technique that a router uses to answer ARP requests intended for a different router

    - The router fakes it's identity and sends out an ARP response for the router that is responsible for that network

    - A man-in-the-middle intrusion enables a host on the network with a spoofed MAC address of the router and allows the traffic to be sent to the hacker

    - Disabling proxy ARP on the interface is recommended and accomplised as follows:

    ```
    conf t
     no ip proxy-arp
    ```

    - **Disable service configuration**: Cisco devices support automatic configuration from remote device using TFTP or other methods

    - This service should be disabled as follows:

    ```
    conf t
     no service config
    ```

    - **Disable the Maintenaince Operation Protocol (MOP) service**: The MOP service is not needed and should be disabled globally and per interface:

    ```
    conf t
     no mop enabled ! or no nop device-mode
     interface <name>
      no mop enabled
    ```

    - **Disable the packet assembler/disassembler (PAD) service**: The PAD service is used for X.25 and is not needed

    - It can be disabled as:

    ```
    conf t
     no service pad
    ```

### Embedded Capture Service (EPS)

- Cisco documentation:

[Cisco-doc](https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-embedded-packet-capture/116045-productconfig-epc-00.html)

- Basic EPC configuration:

```
enable
 monitor capture buffer BUF size 2048 max-size 1518 linear
```

- Define an ACL to be used to limit the capture to the desired traffic:

```
conf t
 ip access-list extended BUF-FILTER
  permit ip host 192.168.1.1 host 172.16.1.1
  permit ip host 172.16.1.1 host 192.168.1.1
  exit
 exit

monitor capture buffer BUF filter access-list BUF-FILTER
```

- Define which switching path or address family IPv4/IPv6 should the capture run

```
enable
 monitor capture point ip cef POINT f0/0 both
 monitor capture point associate POINT BUF
```

- Start the capture:

```
enable
 monitor capture point start POINT
```

- Let the capture to run

- Stop the capture

```
enable
 monitor capture point stop POINT
```

- Examine the capture buffer:

```
enable
 show monitor capture buffer BUF dump
```

- Export the capture on another server:

```
enable
 monitor capture buffer BUF export tftp://10.1.1.1/BUF.pcap
```

- Delete the capture and the capture buffer:

```
no monitor capture point ip cef POINT f0/0 both
no monotor capture buffer BUF
```

```
R2-COPP#monitor capture point stop POINT
R2-COPP#
R2-COPP#
R2-COPP#
*Nov 29 13:36:10.617: %BUFCAP-6-DISABLE: Capture Point POINT disabled.
R2-COPP#show monitor capture buffer BUF dump 
13:35:46.019 UTC Nov 29 2025 : IPv4 LES CEF    : Gi0/0 None

0D98B860:                   52540067 BC6B5254          RT.g<kRT
0D98B870: 00E73554 08004500 00640000 0000FE01  .g5T..E..d....~.
0D98B880: B6930101 01010202 02020800 C0B20000  6...........@2..
0D98B890: 00000000 000000BE BCD9ABCD ABCDABCD  .......><Y+M+M+M
0D98B8A0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8B0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8C0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8D0: ABCDABCD ABCDABCD ABCD00             +M+M+M+M+M.     

13:35:46.030 UTC Nov 29 2025 : IPv4 LES CEF    : Gi0/0 None

0D98B860:                   52540067 BC6B5254          RT.g<kRT
0D98B870: 00E73554 08004500 00640001 0000FE01  .g5T..E..d....~.
0D98B880: B6920101 01010202 02020800 C0A60000  6...........@&..
0D98B890: 00010000 000000BE BCE4ABCD ABCDABCD  .......><d+M+M+M
0D98B8A0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8B0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8C0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8D0: ABCDABCD ABCDABCD ABCD00             +M+M+M+M+M.     

13:35:46.035 UTC Nov 29 2025 : IPv4 LES CEF    : Gi0/0 None
          
0D98B860:                   52540067 BC6B5254          RT.g<kRT
0D98B870: 00E73554 08004500 00640002 0000FE01  .g5T..E..d....~.
0D98B880: B6910101 01010202 02020800 C0A10000  6...........@!..
0D98B890: 00020000 000000BE BCE8ABCD ABCDABCD  .......><h+M+M+M
0D98B8A0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8B0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8C0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8D0: ABCDABCD ABCDABCD ABCD00             +M+M+M+M+M.     

13:35:46.040 UTC Nov 29 2025 : IPv4 LES CEF    : Gi0/0 None

0D98B860:                   52540067 BC6B5254          RT.g<kRT
0D98B870: 00E73554 08004500 00640003 0000FE01  .g5T..E..d....~.
0D98B880: B6900101 01010202 02020800 C09B0000  6...........@...
0D98B890: 00030000 000000BE BCEDABCD ABCDABCD  .......><m+M+M+M
0D98B8A0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8B0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8C0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8D0: ABCDABCD ABCDABCD ABCD00             +M+M+M+M+M.     

13:35:46.045 UTC Nov 29 2025 : IPv4 LES CEF    : Gi0/0 None

0D98B860:                   52540067 BC6B5254          RT.g<kRT
0D98B870: 00E73554 08004500 00640004 0000FE01  .g5T..E..d....~.
0D98B880: B68F0101 01010202 02020800 C0970000  6...........@...
0D98B890: 00040000 000000BE BCF0ABCD ABCDABCD  .......><p+M+M+M
0D98B8A0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8B0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8C0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8D0: ABCDABCD ABCDABCD ABCD00             +M+M+M+M+M.     

13:35:47.604 UTC Nov 29 2025 : IPv4 LES CEF    : Gi0/0 None

0D98B860:                   52540067 BC6B5254          RT.g<kRT
0D98B870: 00E73554 08004500 00640005 0000FE01  .g5T..E..d....~.
0D98B880: B68E0101 01010202 02020800 BA820001  6...........:...
0D98B890: 00000000 000000BE C308ABCD ABCDABCD  .......>C.+M+M+M
0D98B8A0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8B0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8C0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8D0: ABCDABCD ABCDABCD ABCD00             +M+M+M+M+M.     

13:35:47.615 UTC Nov 29 2025 : IPv4 LES CEF    : Gi0/0 None

0D98B860:                   52540067 BC6B5254          RT.g<kRT
0D98B870: 00E73554 08004500 00640006 0000FE01  .g5T..E..d....~.
0D98B880: B68D0101 01010202 02020800 BA780001  6...........:x..
0D98B890: 00010000 000000BE C311ABCD ABCDABCD  .......>C.+M+M+M
0D98B8A0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8B0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8C0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8D0: ABCDABCD ABCDABCD ABCD00             +M+M+M+M+M.     

13:35:47.620 UTC Nov 29 2025 : IPv4 LES CEF    : Gi0/0 None

0D98B860:                   52540067 BC6B5254          RT.g<kRT
0D98B870: 00E73554 08004500 00640007 0000FE01  .g5T..E..d....~.
0D98B880: B68C0101 01010202 02020800 BA730001  6...........:s..
0D98B890: 00020000 000000BE C315ABCD ABCDABCD  .......>C.+M+M+M
0D98B8A0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8B0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8C0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8D0: ABCDABCD ABCDABCD ABCD00             +M+M+M+M+M.     

13:35:47.625 UTC Nov 29 2025 : IPv4 LES CEF    : Gi0/0 None

0D98B860:                   52540067 BC6B5254          RT.g<kRT
0D98B870: 00E73554 08004500 00640008 0000FE01  .g5T..E..d....~.
0D98B880: B68B0101 01010202 02020800 BA6D0001  6...........:m..
0D98B890: 00030000 000000BE C31AABCD ABCDABCD  .......>C.+M+M+M
0D98B8A0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8B0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8C0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8D0: ABCDABCD ABCDABCD ABCD00             +M+M+M+M+M.     

13:35:47.630 UTC Nov 29 2025 : IPv4 LES CEF    : Gi0/0 None

0D98B860:                   52540067 BC6B5254          RT.g<kRT
0D98B870: 00E73554 08004500 00640009 0000FE01  .g5T..E..d....~.
0D98B880: B68A0101 01010202 02020800 BA660001  6...........:f..
0D98B890: 00040000 000000BE C320ABCD ABCDABCD  .......>C +M+M+M
0D98B8A0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8B0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8C0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8D0: ABCDABCD ABCDABCD ABCD00             +M+M+M+M+M.     

13:35:48.708 UTC Nov 29 2025 : IPv4 LES CEF    : Gi0/0 None

0D98B860:                   52540067 BC6B5254          RT.g<kRT
0D98B870: 00E73554 08004500 0064000A 0000FE01  .g5T..E..d....~.
0D98B880: B6890101 01010202 02020800 B6350002  6...........65..
0D98B890: 00000000 000000BE C754ABCD ABCDABCD  .......>GT+M+M+M
0D98B8A0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8B0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8C0: ABCDABCD ABCDABCD ABCDABCD ABCDABCD  +M+M+M+M+M+M+M+M
0D98B8D0: ABCDABCD ABCDABCD ABCD00             +M+M+M+M+M.     

R2-COPP#no monitor capture point ip cef POINT g0/0 both 
*Nov 29 13:39:05.382: %BUFCAP-6-DELETE: Capture Point POINT deleted.

R2-COPP#no monitor capture buffer BUF
Capture Buffer deleted
```
