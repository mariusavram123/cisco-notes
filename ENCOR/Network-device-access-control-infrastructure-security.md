## Network Device Access Control and Infrastructure Security

1. Access Control Lists (ACLs)

2. Terminal Lines and Password Protection

3. Authentication, Authorization, and Accounting (AAA)

4. Zone-Based Firewall (ZBFW)

5. Control Plane Policing (CoPP)

6. Device Hardening

### Access Control Lists (ACLs)

- **Access control lists** (also known as ACLs or access-lists) are sequential lists of access control entries (ACEs) that perform permit or deny packet classification, based on predefined conditional matching statemets

- Packet classification starts at top (lowest sequence) and proceeds down (higher sequence) until a matching pattern is identified

- When a match is found, the appropriate action (permit or deny) is taken, and processing stops

- At the end of every ACL is an implicit deny ACE, which denies all packets that did not match earlier in the ACL

- Access lists applied on Layer 3 interfaces are sometimes referred to as router ACLs (RACLs)

- ACLs can be used to provide packet classification for a variety of features, such as quality of service (QoS), Network Address Translation (NAT), or network identification within routing protocols

- ACLs that can be used for packet filtering:

    - **Numbered standard ACLs**: These ACLs define packets based solely on the source network, and they use numbered entries 1-99 and 1300-1999

    - **Numbered extended ACLs**: These ACLs define packets baded on source, destination, protocol, port, or a combination of other packet attributes, and they use numbered entries 100 - 199 and 2000 - 2699

    - **Named ACLs**: These ACLs allow standard and extended ACLs to be given names instead of numbers and are generally preferred because the name can be correlated to the functionality of the ACL

    - **Port ACLs (PACLs)**: These ACLs can use standard, extended, named, and named extended MAC ACLs to filter traffic on Layer 2 switch ports

    - **VLAN ACLs (VACLs)**: These ACLs can use standard, extended, named, and named extended MAC ACLs to filter traffic on VLANs

- ACLs use wildcard masks instead of subnet masks to classify packets that are being evaluated

- For example, to match all packets with the IP address 192.168.1.0 and the subnet mask 255.255.255.0, an ACL would use an inverted subnet mask, better known as an wildcard mask, of 0.0.0.255 to match the three octets exactly, while all the bits of the last octet could be any value between 0 and 255

- All that is required to convert a subnet mask into a wildcard mask is to substract the subnet mask from 255.255.255.255

- The following shows a subnet mask 255.255.128.0 being converted into a wildcard mask by substracting it from 255.255.255.255

- The end result is a 0.0.127.255 wildcard mask:

```
    255.    255.    255.    255
-   255.    255.    128.    0           Subnet mask
    ----------------------------
    0.      0.      127.    255         Wildcard mask
```

- ACLs have no effect until they are applied to an interface

- Therefore, the next step after creating an ACL is to apply it to an interface

- In addition to the interface, you have to specify the direction (in or out) in which the ACL needs to be applied

- Cisco routers allow only one inbound ACL to and one outbound ACL per interface

- ACLs can be used for various other services in addition to applying to interfaces, such as route maps, class maps, NAT, SNMP, virtual terminal (vty lines), or traffic classification techniques

#### Numbered Standard ACLs

- The process of defining a numbered standard ACL for IOS-XE devices is as follows:

    1. Define the ACL:

    ```
    conf t
     access-list <acl-number> [ deny | permit ] <source> <source-wildcard>
    ```

    - The ACL number can be 1-99 or 1300-1999

    2. Apply the ACL to an interface:

    ```
    conf t
     interface <name>
      ip access-group <acl-nr> <in|out>
    ```

- The keyword `any` and `host` can be used as abbreviation for <source> <source-wildcard>

- Using the keyword `any` is the equivalent of specifying 0.0.0.0 255.255.255.255, which matches all packets

- For example, `access-list 1 permit 0.0.0.0 255.255.255.255` is equivalent to `access-list 1 permit any`

- The keyword `host` is used to match a specific host

- It is equivalent of having specified a host IP address followed by a wildcard mask of 0.0.0.0

- For example: `access-list 1 permit 192.168.1.1 0.0.0.0` is equivalent to `access-list 1 permit host 192.168.1.1`

- The source and source-wildcard reflect a matching pattern for the network prefix that is being matched

- Below are provided standard ACE entries from within the ACL configuration mode and specifies the networks that would match with a standard ACL

```
ACE entry                                                           Networks

permit any                                                          Permits all networks

permit 172.16.0.0 0.0.255.255                                       Permits all networks in the 172.16.0.0/16 range

permit host 192.168.1.1                                             Permits only the 192.168.1.1/32 network
```

- Below we can see how a numbered standard ACL is created and applied to an interface to deny traffic from the 172.16.0.0/24 subnet and from host 192.168.1.1/32 while allowing all other traffic coming into interface G0/1

- Notice that the last ACE in the ACL permits all traffic (permit any)

- If this ACE is not included, all traffic will be dropped because of the implicit deny (deny any) at the end of every ACL

- R1:

```
conf t
 access-list 1 deny 172.16.0.0 0.0.0.255
 access-list 1 deny host 192.168.1.1
 access-list 1 permit any

 interface g0/1
  ip access-group 1 in
```

#### Numbered Extended ACLs

- The process of defining numbered extended ACL is as follows:

    1. Define the ACL as follows:

    ```
    conf t
     access-list <number> [deny|permit] <protocol> <source> <source-wildcard> <destination> <destination-wildcard> [protocol-options] <log | log-input> 
    ```

    - The ACL number can be 100-199 or 2000-2699

    2. Apply the ACL to an interface:

    ```
    conf t
     interface <name>
      ip access-group <acl-nr> <in|out>
    ```

- As with standard ACLs, `source` `source-wildcard` and `destination` `destination-wildcard` can be defined to match a single host with the `host` keyword or match any subnet with the `any` keyword

- The `protocol-options` keyword differs based on the protocol specified by the ACE

- For example, when TCP or UDP protocols are defined, eq, lt, and gt (equal to, less than, and greater than) keywords become available to specift ports to be matched as well as more granular options such as SYN and ACK

- Below we can see how a numbered extended ACL is created and applied to an interface to block all telnet and ICMP traffic as well as deny all IP traffic from host 10.1.2.2 to host 10.1.2.1

- Notice how telnet's TCP port is being matched with the eq keyword

```
conf t
 access-list 100 deny tcp any any eq 23
 access-list 100 deny icmp any any
 access-list 100 deny ip host 10.1.2.2 host 10.1.2.1
 access-list 100 permit ip any any

 interface g0/1
  ip access-group 100 in
```

#### Named ACLs

- Named ACLs allow for ACLs to be named, which makes administering ACLs much easier, as long as proper ACL naming conventions are followed

- They function the same way as standard and extended ACLs; the only difference is in the CLI syntax used to create them

- To create and apply a named ACL, follow these steps:

    1. Define the ACL using the following commands:

    ```
    conf t
     ip access-list <standard|extended> <acl-nr|acl-name>
    ```

    - Entering this command places the CLI in ACL configuration mode

    2. Configure the specific ACE in ACL configuration mode:

    ```
      [sequence] <permit|deny> <source> <source-wildcard> ...
    ```

    3. Apply the ACL to an interface:

    ```
    conf t
     interface <name>
      ip access-group <acl-nr|acl-name> <in|out>
    ```

- Notice in step 1 that the CLI for named ACLs starts with `ip` instead of just `access-list` and that the standard and extended ACL keywords need to be explicitly defined

- Below is shown how named standard and extended ACLs are created and applied to an interface

- The numbered ACLs in the examples below are included as a reference for easy comparison to named ACLs

- Named standard ACLs:

```
conf t
 ip access-list standard STANDARD_ACL
  deny 172.16.0.0 0.0.255.255
  deny host 192.168.1.1
  permit any
  exit
 interface g0/1
  ip access-group STANDARD_ACL in 
```

- Numbered standard ACL:

```
conf t
 access-list 1 deny 172.16.0.0 0.0.255.255
 access-list 1 deny host 192.168.1.1
 access-list 1 permit any
 interface g0/1
  ip access-group 1 in
```

- Named Extended ACL:

```
conf t
 ip access-list extended EXTENDED_ACL
  deny tcp any any eq 23
  deny icmp any any
  deny ip host 10.1.2.2 host 10.1.2.1
  permit ip any any
  exit
 interface g0/1
  ip access-group EXTENDED_ACL in
```

- Numbered extended ACL:

```
conf t
 access-list 100 deny tcp any any eq 23
 access-list 100 deny icmp any any
 access-list 100 deny ip host 10.1.2.2 host 10.1.2.1
 access-list 100 permit ip any any
 interface g0/1
  ip access-group 100 in
```

#### Port ACLs (PACLs) and VLAN ACLs (VACLs)

- Layer 2 Cisco switches support access-lists that can be applied on Layer 2 ports as well as VLANs

- Access lists applied to Layer 2 ports are called *port access control lists* (PACLs), and access-lists applied to VLANs are called *VLAN access control lists* (VACLs)

##### PACLs

- The CLI syntax for configuring PACLs that are used to filter Layer 3 traffic is the same as the syntax for RACLs on an IOS XE router; the only difference is that PACLs also support Layer 2 MAC-address based filtering, which uses different CLI syntax

- PACLs can be standard, extended, or named IPv4 ACLs for Layer 3, and they can be named MAC address ACLs for Layer 2

- PACLs have a few restrictions that vary from platform to platform

- The following are some of the most common restrictions:

    - PACLs only support filtering incoming traffic on an interface (no outbound filtering support)

    - PACLs cannot filter Layer 2 control packets, such as CDP, VTP, DTP, PAgP, UDLD and STP

    - PACLs are supported only in hardware

    - PACLs do not support ACLs to filter IPv6, ARP, or Multiprotocol Label Switching (MPLS) traffic

- An IPv4 PACL is applied to an interface with the following procedure:

```
conf t
 ip access-group <acl-name/nr> in
```

- Below we can see a PACL applied to a Layer 2 interface G0/1 to block ICMP, telnet traffic, and host 10.1.2.2 access to host 10.1.2.1

```
conf t
 ip access-list extended PACL
  deny tcp any any eq 23
  deny icmp any any
  deny ip host 10.1.2.2 host 10.1.2.1
  permit ip any any
 interface g0/1
  switchport
  ip access-group PACL in
```

- MAC access list applied to an interface:

```
conf t
 mac access-list extended MACL
  permit 11:22:13:11:11:12 11:22:13:11:11:14 any
  deny any any

 interface g0/1
  mac access-list MACL in
```

##### VACLs

- VACLs can filter traffic that is bridged within a VLAN or that is routed into or out of a VLAN

- These are the steps to create and apply VACLs:

    1. Define a vlan access map:

    ```
    conf t
     vlan access-map <name> <sequence>
    ```

    - A VLAN access map consists on one or more VLAN access map sequences where each VLAN access map sequence is composed on one match and one action statement

    2. Configure the match statement by using the following command:

    ```
      match ip address <acl-nr|acl-name> mac address <acl-name>
    ```

    - The match statement supports standard, extended, or named IPv4 ACLs as well as named MAC address ACLs as the matching criteria

    - Configure the action statement, by using the command:

    ```
      action <forward|drop|log>
    ```

    - The action statement specifies the action to be taken when a match occurs, which could be to forward or drop traffic

    - Only dropped traffic can be logged using the `log` keyword

    4. Apply the VACL:

    ```
    conf t
     vlan filter <vlan-access-map-name> vlan-list <vlan-list>
    ```

    - VLAN-list can be a single VLAN, a range of VLANs (such as 5-30), or a comma-separated list of multiple VLANs (such as 1,2-4,6)

- Below is shown a VLAN access map applied to vlan 20 to drop ICMP and telnet traffic and allow other traffic

- Notice that the named ACLs ICMP and TELNET, only include ACEs with a permit statement

- The reason is that ACLs are used as matching criteria only by the VLAN access maps, while the VLAN access maps are configured with the action to drop the matched traffic

```
conf t
 ip access-list extended ICMP
  permit icmp any any

 ip access-list extended TELNET
  permit tcp any any eq 23

 ip access-list extended OTHER
  permit ip any any

 vlan access-map VACL_20 10
  match ip address ICMP
  action drop

 vlan access-map VACL_20 20
  match ip address TELNET
  action drop log

 vlan access-map VACL_20 30
  march ip address OTHER
  action forward
 
 vlan filter VACL_20 vlan-list 20
```

- Verification:

```
SW1(config)#do sh vlan access-map
Vlan access-map "VMAP1"  10
  Match clauses:
    ip   address: PACL
  Action:
    forward
Vlan access-map "VACL_20"  10
  Match clauses:
    ip   address: ICMP
  Action:
    drop
Vlan access-map "VACL_20"  20
  Match clauses:
    ip   address: TELNET
  Action:
    drop log
Vlan access-map "VACL_20"  30
  Match clauses:
    ip   address: OTHER
  Action:
    forward

SW1(config)#do sh vlan filter
VLAN Map VACL_20 is filtering VLANs:
  20
```

#### PACL, VACL and RACL interaction

- When a PACL, a VACL, and an RACL are all configured in the same VLAN, the ACLs are applied in a specific order, depending on whether the incoming traffic needs to be bridged or routed:

- Bridged traffic processed in order (within the same VLAN)

    1. Inbound PACL on the switch port (for example, VLAN 10)

    2. Inbound VACL on the VLAN (for example, VLAN 10)

    3. Outbound VACL on the VLAN (for example, VLAN 10)

- Routed traffic processing in order (across VLANs):

    1. Inbound PACL on the port (for example, VLAN 10)

    2. Inbound VACL on the port (for example, VLAN 10)

    3. Inbound ACL on the SVI (for example, SVI 10)

    4. Outbound ACL on the SVI (for example, SVI 20)

    5. Outbound VACL on the VLAN (for example, VLAN 20)

- Outbound PACLs are not supported

- Downloadable ACLs (dACLs) are another form of PACL that can be assigned dynamically by a RADIUS authentication server, such as Cisco ISE

- After successful network access authentication, if a PACL is configured on a switch port and a dACL is assigned by Cisco ISE on the same switch port, the dACL overwrites the PACL

### Terminal Lines and Password Protection

- Password protection to control or restrict access to the CLI to protect the router from unauthorized local access is the most common type of security that needs to be implemented

- There are three basic methods to gain access to the CLI of an IOS XE device:

    - **Console port (cty line)**: On any IOS XE device, this line appears in configuration as `line con 0` and in the output of the command `show line` as *cty*. The console port is mainly used for local system access using a console terminal

    - **Auxiliary port (aux) line**: This line appears in the configuration as `line aux 0`. The aux port is mainly used for remote access into the device through a modem

    - **Virtual terminal (vty) lines**: These lines are displayed by default in the configuration as `line vty 0 4`

    - They are used solely for Telnet and SSH connections

    - They are virtual because they are logical lines with no physical interface associated with them

- Below is shown the default configuration for the cty, aux, and vty lines on a Cisco IOS XE device:

```
SW1#show run | s line
line con 0
 logging synchronous
line aux 0
line vty 0 4
 logging synchronous
 login
line vty 5 1023
 logging synchronous
 login
```

- Each of these types of terminal lines should be password protected

- There are three ways to add password protection to the lines:

    - **Using a password configured directly on the line**: Not recommended

    - **Using username-based authentication**: Recommended as a fallback

    - **Using an AAA server**: Highly recommended

#### Password Types

- The following five password types are available in Cisco IOS XE; they are mentioned in the order of evolution:

    - **Type 0 passwords**: These passwords are the most insecure because they are not encrypted or hashed, and they are visible in the device configuration in plaintext

    - The command `enable password` is an example of a command that uses a type 0 password

    - Type 0 passwords are not recommended to be used

    - **Type 7 passwords**: These passwords use a Cisco proprietary Vigenere cypher encryption algorithm which is a very weak encryption algorithm

    - There are multiple online password utilities online that can decrypt type 7 encrypted passwords in less than a second

    - Type 7 encryption is enabled by the command `service password-encryption` for commands that use type 0 passwords such as `enable password`, `username password`, and `line password` commands

    - Type 7 passwords are not recommended to be used

    - **Type 5 passwords**: These password uses the MD5 hashing algorithm with password salting

    - This makes them much stronger than type 0 or type 7 passwords, but they are also very easy to crack

    - The command `enable secret` is an example of a command that use a type 5 password

    - Type 5 passwords are not recommended to be used

    - **Type 8 passwords**: These passwords use the Password-Based Key Derivation Function 2 (PBKDF2) with a SHA-256 hashed secret and password salting

    - They are considered to be uncrackable and recommended to be used

    - **Type 9 passwords**: These passwords use the scrypt hashing algorithm and password salting

    - Just like type 8 passwords, they are considered to be uncrackable, and Cisco recommends that they be used

- Type 4 passwords are available in a limited number of Cisco IOS XE releases based on the Cisco IOS XE 15 code base

- They were not mentioned in the preceeding list because they should never be used due to a security flaw in the implementation (security advisory cisco-sa-20130318-type4)

- Type 4 passwords were deprecated, and type 8 and 9 password hashing was introduced

- Types 8 and 9 are the recommended password types to use, where type 9 is recommended by Cisco

#### Password Encryption

- The `service password-encryption` command in global configuration mode is used to encrypt type 0 passwords in the configuration (for example, BGP passwords) over a plain-text session such as telnet in an effort to prevent unauthorized users from viewing the password

- For example, if someone executed the command `show running-config` during a telnet session, a protocol analyzer would be able to display the password

- However, if the command `service password-encryption` were used, the password would be encrypted even during the same plaintext telnet session

- Password configured prior to configure the command `service password-encryption` are not encrypted and must be reentered into the configuration

