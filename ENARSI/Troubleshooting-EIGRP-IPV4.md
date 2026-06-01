## Troubleshooting EIGRP for IPv4

1. Troubleshooting EIGRP for IPv4 Neighbor Adjacencies

2. Troubleshooting EIGRP for IPv4 routes

3. Troubleshooting Miscellaneous EIGRP for IPv4 issues

4. EIGRP for IPv4 Trouble Tickets

- Before any routes can be exchanged between EIGRP routers on the same LAN or across a WAN, an EIGRP neighbor relationship must be formed

- Neighbor relationships may not form for many reasons, and as a troubleshooter, you need to be aware of them

- This chapter deeps into these issues and gives you the tools needed to identify them and successfully solve neighbor issues

- Once neighbor relationships are formed, neighboring routers exchange EIGRP routes

- In various cases, routes may end up missing, and you need to be able to determine why the routes are missing

- The various ways that routes could go missing and how you can identify them and solve route-related issues

- How to troubleshoot issues related to load balancing, summarization, discontiguous networks, and feasible successors

### Troubleshooting EIGRP for IPv4 Neighbor Adjacencies

- EIGRP establishes neighbor relationships by sending hello packets to the multicast address 224.0.0.10, out interfaces participating in the EIGRP process

- To enable the EIGRP process on an interface, you use the `network <ip-address> <wildcard-mask>` command in `router eigrp` configuration mode

- For example, the command `network 10.1.1.0 0.0.0.255` enables EIGRP on all interfaces with an IP address from 10.1.1.0 through 10.1.1.255

- The command `network 10.1.1.65 0.0.0.0` enables the EIGRP process on only the interface with the IP address 10.1.1.65

- It seems rather simple, and it is; however, for various reasons, neighbor relationships may not form, and all you need to be aware of all of them if you plan to successfully troubleshoot EIGRP-related problems

- Below will be discussed the reasons EIGRP neighbor relationships may not form and how to identify them during the troubleshooting process

- To verify the EIGRP neighbors, you use the `show ip eigrp neighbors` command

- Below is an example of `show ip eigrp neighbors` command:

```
R2#show ip eigrp neighbors 
EIGRP-IPv4 Neighbors for AS(65001)
H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)         (ms)       Cnt Num
2   172.16.23.3             Gi2                      12 00:04:12  112   672  0  6
1   172.16.24.4             Gi3                      11 00:04:12    7   100  0  3
0   172.16.12.1             Gi1                      13 00:04:12  228  1368  0  9
EIGRP-IPv4 VR(EIGRP-NAMED) Address-Family Neighbors for AS(65002)
R2#
```

- It lists the IPv4 address of the neighboring device's interface that sent the hello packet, the local interface on the router used to reach that neighbor, how long the local router will consider the neighboring router to be a neighbor, how long the routers has been neighbors, the amount of time it takes for the neighbors to communicate (on average), the number of EIGRP packets in a queue waiting to be sent to a neighbor (which should always be zero since you want up-to-date routing information), and a sequence number to keep track of the EIGRP packets received from the neighbor to ensure that only newer packets are accepted and processed

- EIGRP neighbor relationships may not form for a variety of reasons, including the following:

    - **Interface is down**: The interface must be up/up

    - **Mistmatched Autonomous System Numbers**: Both routers need to be using the same *autonomous system* number

    - **Incorrect network statement**: The `network` statement must identify the IP address of the interface you want to include in the EIGRP process 

    - **Mismatched K values**: Both routers must use exactly the same K values

    - **Passive Interface**: The `passive interface` feature suppresses sending and receiving of hello packets while still allowing the interface's network to be advertised

    - **Different subnets**: The exchange of hello packets should be made on the same subnet; if it isn't, the hello packets are ignored

    - **Authentication**: If authentication is being used, the key ID and the key string must match, and the key must be valid (if valid times has been configured)

    - **ACLs**: An access control list (ACL) may be denying packets to the EIGRP multicast address 224.0.0.10

    - **Timers**: Timers do not have to match; however, if they are not configured correctly, neighbor adjacencies could flap

- When an EIGRP neighbor relationship does not form, the neighbor is not listed in the neighbor table

- In such a case, you need the assistance of an accurate physical and logical network diagram and the `show cdp neighbors` command to verify who should be the neighbors

- When troubleshooting EIGRP, you need to be aware on how to verify the parameters associated with each of the reasons listed here

- A look at them individually

#### Interface is Down

- The interface must be up if you plan on forming an EIGRP neighbor adjacency

- You can verify the status of an interface with the `show ip interface brief` command

- The status should be listed as `up`, and the protocol should be listed as `up`

#### Mismatched Autonomous System Numbers

- For an EIGRP neighbor relationship to be formed, both routers need to be in the same autonomous system

- You specify the autonomous system number when you issue the command `router eigrp <autonomous-system-number>` command in global configuration mode

- If the two routers are not in the same autonomous systems, they will not form EIGRP neighbor relationship

- Most EIGRP `show` commands display the autonomous system number in the output

- However, the best one is `show ip protocols`, which displays an incredible amount of information for troubleshooting as shown below

- In this example, you can see that R1 is participating in EIGRP autonomous system 65001

- Using the `spot-the-difference` troubleshooting method, you can compare the autonomous system value listed to the value of a neighboring router to determine whether they differ

```
R1#show ip protocols 
*** IP Routing is NSF aware ***

Routing Protocol is "application"
  Sending updates every 0 seconds
  Invalid after 0 seconds, hold down 0, flushed after 0
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Maximum path: 32
  Routing for Networks:
  Routing Information Sources:
    Gateway         Distance      Last Update
  Distance: (default is 4)

Routing Protocol is "eigrp 65001"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Default networks flagged in outgoing updates
  Default networks accepted from incoming updates
  EIGRP-IPv4 Protocol for AS(65001)
    Metric weight K1=1, K2=0, K3=1, K4=0, K5=0
    Soft SIA disabled
    NSF-aware route hold timer is 240
  EIGRP NSF disabled
     NSF signal timer is 20s
     NSF converge timer is 120s
    Router-ID: 10.1.200.1
    Topology : 0 (base) 
      Active Timer: 3 min
      Distance: internal 90 external 170
      Maximum path: 4
      Maximum hopcount 100
      Maximum metric variance 1

  Automatic Summarization: disabled
  Maximum path: 4
  Routing for Networks:
    10.1.100.0/24
    10.1.200.0/24
    172.16.12.0/24
    172.16.13.0/24
  Routing Information Sources:
    Gateway         Distance      Last Update
    172.16.12.2           90      00:02:15
    172.16.13.3           90      00:02:15
  Distance: internal 90 external 170
```

- R4

```
R4(config-router)#do debug eigrp packets
    (UPDATE, REQUEST, QUERY, REPLY, HELLO, UNKNOWN, PROBE, ACK, STUB, SIAQUERY, SIAREPLY)
EIGRP Packet debugging is on
R4(config-router)#
*May 24 09:32:28.368: EIGRP: Sending HELLO on Gi1 - paklen 20
*May 24 09:32:28.368:   AS 65002, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R4(config-router)#
*May 24 09:32:33.161: EIGRP: Sending HELLO on Gi1 - paklen 20
*May 24 09:32:33.162:   AS 65002, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R4(config-router)#
*May 24 09:32:37.774: EIGRP: Sending HELLO on Gi1 - paklen 20
*May 24 09:32:37.774:   AS 65002, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R4(config-router)#
*May 24 09:32:42.050: EIGRP: Sending HELLO on Gi1 - paklen 20
*May 24 09:32:42.050:   AS 65002, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R4(config-router)#
*May 24 09:32:46.856: EIGRP: Sending HELLO on Gi1 - paklen 20
*May 24 09:32:46.857:   AS 65002, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R4(config-router)#do un all
```

- The output of `debug eigrp packets` command shown that the router is not receiving any hello packets from the neighbors with the mismatched autonomous system number

- In this example R1 is sending hello packets out G1

- However is not receiving any hello packets on this interface

- This could be because of an autonomous system mismatch

- The local router could have the wrong autonomous system number, or the remote router could have the wrong autonomous system number

#### Incorrect Network Statement

- If the network command is misconfigured, EIGRP may not be enabled on proper interfaces, and as a result, hello packets will not be sent and neighbor relationships will not be formed

- You can determine which interfaces are participating in the EIGRP process with the command `show ip eigrp interfaces`

- In our example for instance, you can see that two interfaces are participating in the EIGRP process for autonomous system 65001

- Gi0/1 does not have an EIGRP peer and Gi0/0 does have an EIGRP peer

```
R1(config-router)#do sh ip eigrp interf
EIGRP-IPv4 Interfaces for AS(65001)
                              Xmit Queue   PeerQ        Mean   Pacing Time   Multicast    Pending
Interface              Peers  Un/Reliable  Un/Reliable  SRTT   Un/Reliable   Flow Timer   Routes
Gi0/0                    1        0/0       0/0           1       0/0           50           0
Lo1                      0        0/0       0/0           0       0/0            0           0
Gi0/1                    0        0/0       0/0           0       0/0            0           0
```

- This is expected because no other routers can be reached out G0/1 for this scenario

- However, if you expect an EIGRP peer out the interface based on your documentation, you need to troubleshoot why the peering/neighbor relationship is not forming

- Shift your attention to the `Pending Routes` column

- Notice that all interfaces are listed as 0

- This is expected

- Any other value in this column means that some issue on the network (such as congestion) is preventing the interface from sending the necessary updates to the neighbor

- Remember that EIGRP passive interfaces do not show up in this output

- Therefore, you shouldn't jump to the conclusion that the network command is incorrect or missing if the interface does not show up in this output

- It is possible that the interface is passive

- The output of `show ip protocols` displays the interfaces that are running EIGRP as a result of the network command

- It is not obvious at first unless someone tells you

- The reason is not obvious is that it' not displayed properly

- Notice in output `Routing for Networks`

- Those are not the networks you are routing for

```
R1(config-router)#do sh ip protocols
*** IP Routing is NSF aware ***

Routing Protocol is "application"
  Sending updates every 0 seconds
  Invalid after 0 seconds, hold down 0, flushed after 0
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Maximum path: 32
  Routing for Networks:
  Routing Information Sources:
    Gateway         Distance      Last Update
  Distance: (default is 4)

Routing Protocol is "eigrp 65001"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Default networks flagged in outgoing updates
  Default networks accepted from incoming updates
  EIGRP-IPv4 Protocol for AS(65001)
    Metric weight K1=1, K2=0, K3=1, K4=0, K5=0
    Soft SIA disabled
    NSF-aware route hold timer is 240
    Router-ID: 1.1.1.1
    Topology : 0 (base) 
      Active Timer: 3 min
      Distance: internal 90 external 170
      Maximum path: 4
      Maximum hopcount 100
      Maximum metric variance 1

  Automatic Summarization: disabled
  Maximum path: 4
  Routing for Networks:
    1.1.1.1/32
    10.1.1.1/32
    10.1.12.1/32
  Passive Interface(s):
    Loopback1
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.1.1.2              90      00:01:09
  Distance: internal 90 external 170

```

- Rather, you are routing for the networks associated with the interface on which the EIGRP will be enabled, based on network commands

- In this case, network 10.1.1.1/32 really means network 10.1.1.1 0.0.0.0, and network 10.1.12.1/32 really means network 10.1.12.1 0.0.0.0

- Therefore, a better option is to use `show run | s router eigrp` command, as shown below

```
R1(config-router)#do sh run | s router eigrp
router eigrp 65001
 network 1.1.1.1 0.0.0.0
 network 10.1.1.1 0.0.0.0
 network 10.1.12.1 0.0.0.0
 passive-interface Loopback1
```

- Notice that the `network` statement is extremely important

- If it is misconfigured, interfaces that should be participating in the EIGRP process might not be, and interfaces that should not be participating in the EIGRP process, might be

- So, you should be able to recognize issues related to the `network` statement

- When using the `debug eigrp packets` command on the router with the misconfigured or missing network statement, you will notice that hello packets not being sent out the interface properly

- For example, if you expect hello packets to be sent out G0/1, but the `debug eigrp packets` command is not indicating that this is happening, it is possible that the interface is not participating in the EIGRP process because of a bad network statement or the interface is passive and suppressing hello packets

#### Mismatched K Values

- The K values used for metric calculation must match between neighbors in order for an adjacency to form

- You can verify either K values match by using `show ip protocols` as shown below

- The default K values are highlighted in our example

- Usually there is no need to change the K values

- However, if they are changed, you need to make them match on every router in the autonomous system

- You can use the `spot-the-difference` method when determining K values do not match between routers

- In addition, if you are logging syslog messages with a severity level of 5, you receive a message similar with the following:

```
logging console notification
logging buffered notification

R2(config-router)#metric weights 0 1 1 3 3 1 
R2(config-router)#
R2(config-router)#
*May 24 18:15:59.131: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet2) is down: K-value mismatch
*May 24 18:15:59.682: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.1.1 (GigabitEthernet1) is down: K-value mismatch
R2(config-router)#
*May 24 18:16:04.233: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.1.1 (GigabitEthernet1) is down: K-value mismatch
R2(config-router)#
*May 24 18:16:08.674: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet2) is down: K-value mismatch
R2(config-router)#
*May 24 18:16:13.304: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet2) is down: K-value mismatch
*May 24 18:16:13.829: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.1.1 (GigabitEthernet1) is down: K-value mismatch
R2(config-router)#
*May 24 18:16:17.755: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet2) is down: K-value mismatch
*May 24 18:16:18.553: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.1.1 (GigabitEthernet1) is down: K-value mismatch
```

- Viewing K values on `show ip protocols` output

```
R2(config-router)#do sh ip protoc
*** IP Routing is NSF aware ***

Routing Protocol is "application"
  Sending updates every 0 seconds
  Invalid after 0 seconds, hold down 0, flushed after 0
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Maximum path: 32
  Routing for Networks:
  Routing Information Sources:
    Gateway         Distance      Last Update
  Distance: (default is 4)

Routing Protocol is "eigrp 65001"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Default networks flagged in outgoing updates
  Default networks accepted from incoming updates
  EIGRP-IPv4 Protocol for AS(65001)
    Metric weight K1=1, K2=1, K3=3, K4=3, K5=1
    Soft SIA disabled
    NSF-aware route hold timer is 240
  EIGRP NSF disabled
     NSF signal timer is 20s
     NSF converge timer is 120s
    Router-ID: 2.2.2.2
    Topology : 0 (base) 
      Active Timer: 3 min
      Distance: internal 90 external 170
      Maximum path: 4
      Maximum hopcount 100
      Maximum metric variance 1

  Automatic Summarization: disabled
  Maximum path: 4
  Routing for Networks:
    2.2.2.2/32
    10.1.1.2/32
    10.1.12.2/32
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.1.12.1             90      00:00:05
    10.1.1.1              90      00:00:05
  Distance: internal 90 external 170

```

#### Passive Interface

- The passive interface feature is a must-have for all organizations

- It does two things:

    1. Reduces the EIGRP-related traffic on a network

    2. Improves EIGRP security

- The passive interface feature turns off the sending and receiving of EIGRP packets on an interface while still allowing the interface's network ID to be injected into the EIGRP process and advertised to other EIGRP neighbors

- This ensures that rogue routers attached to the LAN will not be able to form an adjacency with your legitimate router on that interface because it is not sending or receiving EIGRP packets on the interface

- However, if you configure the wrong interface as passive, a legitimate neighbor relationship will not be formed

- As shown in the output of `show ip protocols` below, Gigabit Ethernet 0/1 and Loopback1 are passive interfaces

- If there are no passive interfaces, the passive inteface section does not appear in the `show ip protocols` output

```
R1(config-router)#do sh ip protocols
*** IP Routing is NSF aware ***

Routing Protocol is "application"
  Sending updates every 0 seconds
  Invalid after 0 seconds, hold down 0, flushed after 0
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Maximum path: 32
  Routing for Networks:
  Routing Information Sources:
    Gateway         Distance      Last Update
  Distance: (default is 4)

Routing Protocol is "eigrp 65001"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Default networks flagged in outgoing updates
  Default networks accepted from incoming updates
  EIGRP-IPv4 Protocol for AS(65001)
    Metric weight K1=1, K2=0, K3=1, K4=0, K5=0
    Soft SIA disabled
    NSF-aware route hold timer is 240
    Router-ID: 1.1.1.1
    Topology : 0 (base) 
      Active Timer: 3 min
      Distance: internal 90 external 170
      Maximum path: 4
      Maximum hopcount 100
      Maximum metric variance 1

  Automatic Summarization: disabled
  Maximum path: 4
  Routing for Networks:
    1.1.1.1/32
    10.1.1.1/32
    10.1.12.1/32
  Passive Interface(s):
    GigabitEthernet0/1
    Loopback1
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.1.12.2             90      00:11:54
    10.1.1.2              90      00:00:14
  Distance: internal 90 external 170

```

- Remember for EIGRP, passive interfaces do not appear in the EIGRP interface table

- Therefore, before you jump to the conclusion that the wrong network command was used and the interface was not enabled for EIGRP, you need to check to see if whether the interface is passive

- When using the `debug eigrp packets` command on the router with the passive interface, notice that hello packets are not being sent out that interface

- For example if you expect hello packets to be sent out G0/1 but the `debug eigrp packets` command is not indicating that this is happening, it is possible that the interface is participating in the EIGRP process but is configured as a passive interface

#### Different subnets

- To form an EIGRP neighbor adjacency, the router interfaces must be on the same subnet

- You can confirm this in many ways

- The simplest way is to look at the interface configuration with the `show run interface <type><number>` command

- You can also use the `show ip interface <type> <number>` command or the `show interface <type><number>` command

- Below are shown the running-config for R1 and R2's G0/0 interfaces

- R1:

```
R1#sh run int g0/0
Building configuration...

Current configuration : 114 bytes
!
interface GigabitEthernet0/0
 ip address 10.1.12.1 255.255.255.0
 duplex auto
 speed auto
 media-type rj45
end
```

- R2:

```
R2(config-if)#do sh run int g0/0
Building configuration...

Current configuration : 114 bytes
!
interface GigabitEthernet0/0
 ip address 10.1.12.2 255.255.255.0
 duplex auto
 speed auto
 media-type rj45
end

```

- Are they in the same subnet? Yes!

- Based on the IP address and subnet mask, they are both in the 10.1.12.0/24 subnet

- However if they are not in the same subnet and you have a syslog set up for a severity level of 6, you will get a message similar to the following:

```
R1(config)#logging console informational 
R1(config)#log
*May 31 16:55:10.570: %SYS-5-LOG_CONFIG_CHANGE: Console logging: level informational, xml disabled, filtering disabled

R1(config)#logging buffered informational 

*May 31 16:55:15.649: %SYS-5-LOG_CONFIG_CHANGE: Buffer logging: level informational, xml disabled, filtering disabled, size (8192)
R1(config)#
*May 31 16:55:34.174: %DUAL-6-NBRINFO: EIGRP-IPv4 65001: Neighbor 10.1.21.1 (GigabitEthernet0/0) is blocked: not on common subnet (10.1.12.1/24)
R1(config)#
*May 31 16:55:44.292: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.2 (GigabitEthernet0/0) is down: holding time expired
R1(config)#
```

#### Authentication

- Authentication is used to ensure that EIGRP routers form neighbor relationships only with legitimate routers and that they only accept EIGRP packets from legitimate routers

- Therefore, if authentication is implemented, both routers must agree on the settings for a neighbor relationship to form

- With the authentication, you can use the `spot-the-difference` method

- Below is shown the output of `show run interface <type> <number>` and `show ip eigrp interfaces detail <type> <number>`

- According to the output it is using authentication

```
R1(config-if)#do sh run int g0/0
Building configuration...

Current configuration : 206 bytes
!
interface GigabitEthernet0/0
 ip address 10.1.12.1 255.255.255.0
 ip authentication mode eigrp 65001 md5
 ip authentication key-chain eigrp 65001 EIGRP_AUTH
 duplex auto
 speed auto
 media-type rj45
end

```

```
R1(config-if)#do sh ip eigrp int detail g0/0
EIGRP-IPv4 Interfaces for AS(65001)
                              Xmit Queue   PeerQ        Mean   Pacing Time   Multicast    Pending
Interface              Peers  Un/Reliable  Un/Reliable  SRTT   Un/Reliable   Flow Timer   Routes
Gi0/0                    0        0/0       0/0           0       0/0          932           0
  Hello-interval is 5, Hold-time is 15
  Split-horizon is enabled
  Next xmit serial <none>
  Packetized sent/expedited: 2/0
  Hello's sent/expedited: 92/2
  Un/reliable mcasts: 0/2  Un/reliable ucasts: 3/4
  Mcast exceptions: 0  CR packets: 0  ACKs suppressed: 0
  Retransmissions sent: 3  Out-of-sequence rcvd: 1
  Topology-ids on interface - 0 
  Authentication mode is md5,  key-chain is "EIGRP_AUTH"
  Topologies advertised on this interface:  base
  Topologies not advertised on this interface:

```

- Verifying the key used

```
R1(config-if)#do sh key chain
Key-chain EIGRP_AUTH:
    key 1 -- text "ENARSI"
        accept lifetime (always valid) - (always valid) [valid now]
        send lifetime (always valid) - (always valid) [valid now]
```

- Notice that the authentication must be configured on the correct interface and that it must be tied to the correct autonomous system number

- If you put in the wrong autonomous system number, authentication will not be enabled for the correct autonomous system

- In addition, make sure that you specify the correct keychain to be used for the Message Digest Key 5 (MD5) hash

- You can verify the key chain with the command `show key chain`, as shown above

- The keys in these example do not expire

- However, if you have implemented rotating keys, the key must be valid for authentication to be successful

- Inside the key chain you will find the key ID (1 in this case) and the key string (ENARSI in this case)

- It is mandatory that the key ID and the key string match between neighbors

- Therefore, if you have multiple keys and key strings in a key chain, the same key and the same string must be used at the same time by both routers (meaning they must be valid and in use); otherwise the authentication will fail

- When using the `debug eigrp packets` command for troubleshooting authentication, you receive output based on the authentication issue

- Below is the message that is shown when a neighbor is not configured for authentication:

```
R2(config-if)#do debug eigrp pack
    (UPDATE, REQUEST, QUERY, REPLY, HELLO, UNKNOWN, PROBE, ACK, STUB, SIAQUERY, SIAREPLY)
EIGRP Packet debugging is on
R2(config-if)#
*May 31 18:50:42.318: EIGRP: Gi0/0: ignored packet from 10.1.12.1, opcode = 5 (authentication off)
*May 31 18:50:42.771: EIGRP: Sending HELLO on Gi0/0 - paklen 20
*May 31 18:50:42.771:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R2(config-if)#
R2(config-if)#
R2(config-if)#
*May 31 18:50:46.783: EIGRP: Gi0/0: ignored packet from 10.1.12.1, opcode = 5 (authentication off)
*May 31 18:50:47.408: EIGRP: Sending HELLO on Gi0/0 - paklen 20
*May 31 18:50:47.408:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R2(config-if)#
R2(config-if)#do un all
All possible debugging has been turned off
```

- It ignores the packet and states (authentication off)

- When an incorrect key ID is used for authentication:

```
*May 31 18:44:28.122: EIGRP: pkt authentication key id = 1, key not defined
*May 31 18:44:28.123: EIGRP: Gi0/0: ignored packet from 10.1.12.1, opcode = 5 (invalid authentication)
*May 31 18:44:28.420: EIGRP: Sending HELLO on Gi0/0 - paklen 60
*May 31 18:44:28.420:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R2(config-if)#end
R2#
*May 31 18:44:30.509: %SYS-5-CONFIG_I: Configured from console by console
R2#
*May 31 18:44:33.009: EIGRP: pkt authentication key id = 1, key not defined
*May 31 18:44:33.010: EIGRP: Gi0/0: ignored packet from 10.1.12.1, opcode = 5 (invalid authentication)
*May 31 18:44:33.243: EIGRP: Sending HELLO on Gi0/0 - paklen 60
*May 31 18:44:33.243:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R2#
```

- When the key IDs or key strings do not match between the neighbors, the debug output states 'invalid authentication'

#### ACLs

- Access control lists (ACLs) are extremely powerful

- How they are implemented determines what they control in the network

- If there is an ACL applied to an interface, and the ACL is denying EIGRP packets, or if an EIGRP packet falls victim to the implicit deny all at the end of the ACL, a neighbor relationship does not form

- To determine whether an ACL is applied to an interface, use the `show ip interface <type> <number>` command

- Notice that ACL 100 is applied inbound on interface g0/0

- To verify ACL 100 entries, issue the command `show access-lists 100`

```
R1(config-if)#do sh ip int g0/0
GigabitEthernet0/0 is up, line protocol is up
  Internet address is 10.1.12.1/24
  Broadcast address is 255.255.255.255
  Address determined by non-volatile memory
  MTU is 1500 bytes
  Helper address is not set
  Directed broadcast forwarding is disabled
  Multicast reserved groups joined: 224.0.0.10
  Outgoing access list is not set
  Inbound  access list is 100 ! ACL 100 applied inbound
  Proxy ARP is enabled
  Local Proxy ARP is disabled
  Security level is default
  Split horizon is enabled
  ICMP redirects are always sent
  ICMP unreachables are always sent
  ICMP mask replies are never sent
  IP fast switching is enabled
  IP fast switching on the same interface is disabled
  IP Flow switching is disabled
  IP CEF switching is enabled
  IP CEF switching turbo vector
  IP multicast fast switching is enabled
  IP multicast distributed fast switching is disabled
  IP route-cache flags are Fast, CEF
  Router Discovery is disabled
  IP output packet accounting is disabled
  IP access violation accounting is disabled
  TCP/IP header compression is disabled
  RTP/IP header compression is disabled
  Policy routing is disabled
  Network address translation is disabled
  BGP Policy Mapping is disabled
  Input features: Access List, MCI Check
  IPv4 WCCP Redirect outbound is disabled
  IPv4 WCCP Redirect inbound is disabled
  IPv4 WCCP Redirect exclude is disabled
```

```
R1(config-if)# do sh access-lists 100
Extended IP access list 100
    10 deny eigrp any any (13 matches)
    20 permit ip any any
```

- In this case you can see that ACL 100 is denying EIGRP traffic; this prevents a neighbor relationship from forming

- Notice that outbound ACLs do not affect EIGRP packets; only inbound ACLs do

```
R1(config-if)#ip access-group 100 in
R1(config-if)#
*May 31 19:18:39.348: EIGRP: Sending HELLO on Gi0/0 - paklen 60
*May 31 19:18:39.348:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
*May 31 19:18:39.406: EIGRP: received packet with MD5 authentication, key id = 1
*May 31 19:18:39.406: EIGRP: Received HELLO on Gi0/0 - paklen 60 nbr 10.1.12.2
*May 31 19:18:39.407:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0 peerQ un/rely 0/0
R1(config-if)#
*May 31 19:18:43.693: EIGRP: Sending HELLO on Gi0/0 - paklen 60
*May 31 19:18:43.693:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R1(config-if)#
*May 31 19:18:48.538: EIGRP: Sending HELLO on Gi0/0 - paklen 60
*May 31 19:18:48.539:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R1(config-if)#
*May 31 19:18:52.901: EIGRP: Sending HELLO on Gi0/0 - paklen 60
*May 31 19:18:52.902:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R1(config-if)#
*May 31 19:18:54.409: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.2 (GigabitEthernet0/0) is down: holding time expired
R1(config-if)#
*May 31 19:18:54.412: EIGRP: Sending HELLO on Gi0/0 - paklen 60
*May 31 19:18:54.412:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
*May 31 19:18:54.414: EIGRP: Lost Peer: Total 1 (5/0/0/0/0)
R1(config-if)#
*May 31 19:18:58.695: EIGRP: Sending HELLO on Gi0/0 - paklen 60
*May 31 19:18:58.695:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R1(config-if)#
*May 31 19:19:03.216: EIGRP: Sending HELLO on Gi0/0 - paklen 60
*May 31 19:19:03.217:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R1(config-if)#un  
*May 31 19:19:07.564: EIGRP: Sending HELLO on Gi0/0 - paklen 60
*May 31 19:19:07.564:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/ 
R1(config-if)#ip access-group 100 in
*May 31 19:19:12.506: EIGRP: Sending HELLO on Gi0/0 - paklen 60
*May 31 19:19:12.506:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0 iidbQ un/rely 0/0
R1(config-if)#no ip access-group 100 in
R1(config-if)#u
*May 31 19:19:16.846: EIGRP: received packet with MD5 authentication, key id = 1
*May 31 19:19:16.847: EIGRP: Received HELLO on Gi0/0 - paklen 70 nbr 10.1.12.2
*May 31 19:19:16.848:   AS 65001, Flags 0x0:(NULL), Seq 0/0 interfaceQ 0/0
*May 31 19:19:16.848: EIGRP: Add Peer: Total 1 (6/0/0/0/0)
*May 31 19:19:16.849: EIGRP: Add Peer: Total 1 (6/0/1/0/0)
*May 31 19:19:16.849: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.2 (GigabitEthernet0/0) is up: new adjacency
R1(config-if)#ub 
```

- Therefore, any outbound ACLs that deny EIGRP packets have no effect on your EIGRP troubleshooing efforts

#### Timers

- Although EIGRP timers do not have to match, if the timers are skewed enough, an adjacency will flap

- For example, suppose that R1 is using the default timers 5 and 15, while R2 is sending hello packets every 20 seconds

- R1's hold time will expire before it receives another hello packet from R2; this terminates the neighbor relationship

- Five seconds later, the neighbor relationship is formed, but it is then terminated again 15 seconds later

- Although timers do not have to match, it is important that routers send hello packets at a rate that is faster than the hold time

```
R2#sh ip eigrp int det g0/0 
EIGRP-IPv4 Interfaces for AS(65001)
                              Xmit Queue   PeerQ        Mean   Pacing Time   Multicast    Pending
Interface              Peers  Un/Reliable  Un/Reliable  SRTT   Un/Reliable   Flow Timer   Routes
Gi0/0                    1        0/0       0/0          12       0/0           52           0
  Hello-interval is 20, Hold-time is 15
  Split-horizon is enabled
  Next xmit serial <none>
  Packetized sent/expedited: 19/0
  Hello's sent/expedited: 934/11
  Un/reliable mcasts: 0/18  Un/reliable ucasts: 21/47
  Mcast exceptions: 0  CR packets: 0  ACKs suppressed: 0
  Retransmissions sent: 37  Out-of-sequence rcvd: 5
  Topology-ids on interface - 0 
  Authentication mode is md5,  key-chain is "EIGRP_AUTH"
  Topologies advertised on this interface:  base
  Topologies not advertised on this interface:

```

```
*May 31 19:34:43.865: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is down: Interface PEER-TERMINATION received
R2#debug eigrp ti
R2#debug eigrp timers 
EIGRP Timers debugging is on
R2#debuy
R2#debuy
*May 31 19:34:48.144: EIGRP-Timer: Hello (Gi0/0) Getting Context
*May 31 19:34:48.145: EIGRP-Timer: NSF RS Send Timer IS NOT running
*May 31 19:34:48.148: EIGRP-Timer: NSF RS Send Timer IS NOT running
*May 31 19:34:48.149: EIGRP-Timer: Hello (Gi0/0) Start Jittered in (20000:15)
*May 31 19:34:48.161: EIGRP-Timer: Peer holding Timer IS NOT running
*May 31 19:34:48.162: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:34:48.163: EIGRP-Timer: Hello (Gi0/0) Start in 0
*May 31 19:34:48.164: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is up: new adjacency
*May 31 19:34:48.165: EIGRP-Timer: Pacing (Gi0/0) Timer IS NOT running
*May 31 19:34:48.166: EIGRP-Timer: Pacing (Gi0/0) Start in 0
*May 31 19:34:48.167: EIGRP-Timer: (parent) is Not Expired
*May 31 19:34:48.168: EIGRP-Timer: (parent) is Expired
*May 31 19:34:48.169: EIGRP-Timer: Pacing (Gi0/0) Getting Context
*May 31 19:34:48.170: EIGRP-Timer: Pacing (Gi0/0) Stop Timer
*May 31 19:34:48.171: EIGRP-Timer: Pacing (Gi0/0) Timer IS NOT running
*May 31 19:34:48.172: EIGRP-Timer: Peer transmission Start in 0
*May 31 19:34:48.173: EIGRP-Timer: Peer transmission Getting Context
*May 31 19:34:48.174: EIGRP-Timer: Pacing (Gi0/0) Timer IS NOT running
*May 31 19:34:48.175: EIGRP-Timer: Peer transmission Timer IS running
*May 31 19:34:48.176: EIGRP-Timer: Peer transmission Stop Timer
*May 31 19:34:48.178: EIGRP-Timer: Pacing (Gi0/0) Timer IS NOT running
*May 31 19:34:48.178: EIGRP-Timer: Peer transmission Set Exptime 584942417y18w
*May 31 19:34:48.187: EIGRP-Timer: Hello (Gi0/0) Getting Context
*May 31 19:34:48.188: EIGRP-Timer: NSF RS Send Timer IS NOT running
*May 31 19:34:48.190: EIGRP-Timer: NSF RS Send Timer IS NOT running
*May 31 19:34:48.191: EIGRP-Timer: Hello (Gi0/0) Start Jittered in (20000:15)
*May 31 19:34:48.193: EIGRP-Timer: Peer holding Start in 15000
(...)
R2#debug eigrp neighbors 
EIGRP Static Neighbor debugging is on
R2#
*May 31 19:35:09.162: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:35:09.165: EIGRP-Timer: Peer holding Timer IS running
*May 31 19:35:09.166: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:35:09.168: EIGRP-Timer: (parent) is Not Expired
*May 31 19:35:09.168: EIGRP-Timer: (parent) is Not Expired
*May 31 19:35:10.257: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:35:10.260: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is down: Interface PEER-TERMINATION received
R2#
*May 31 19:35:10.262: EIGRP-Timer: Active Check Timer IS NOT running
*May 31 19:35:10.263: EIGRP-Timer: Peer transmission Stop Timer
*May 31 19:35:10.264: EIGRP-Timer: Peer holding Stop Timer
*May 31 19:35:10.265: EIGRP-Timer: NSF route hold Stop Timer
*May 31 19:35:10.266: EIGRP-Timer: (parent) is Not Expired
*May 31 19:35:10.267: EIGRP-Timer: (parent) is Not Expired
R2#
*May 31 19:35:15.048: EIGRP-Timer: Peer holding Timer IS NOT running
*May 31 19:35:15.048: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:35:15.049: EIGRP-Timer: Hello (Gi0/0) Start in 0
*May 31 19:35:15.050: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is up: new adjacency
*May 31 19:35:15.051: EIGRP-Timer: Pacing (Gi0/0) Timer IS NOT running
*May 31 19:35:15.052: EIGRP-Timer: Pacing (Gi0/0) Start in 0
*May 31 19:35:15.053: EIGRP-Timer: (parent) is Not Expired
*May 31 19:35:15.054: EIGRP-Timer: (parent) is Expired
*May 31 19:35:15.055: EIGRP-Timer: Pacing (Gi0/0) Getting Context
*May 31 19:35:15.056: EIGRP-Timer: Pacing (Gi0/0) Stop Timer
*May 31 19:35:15.057: EIGRP-Timer: Pacing (Gi0/0) Timer IS NOT running
*May 31 19:35:15.058: EIGRP-Timer: Peer transmission Start in 0
*May 31 19:35:15.059: EIGRP-Timer: Peer transmission Getting Context
*May 31 19:35:15.060: EIGRP-Timer: Pacing (Gi0/0) Timer IS NOT running
*May 31 19:35:15.060: EIGRP-Timer: Peer transmission Timer IS running
*May 31 19:35:15.061: EIGRP-Timer: Peer transmission Stop Timer
*May 31 19:35:15.064: EIGRP-Timer: Pacing (Gi0/0) Timer IS NOT running
*May 31 19:35:15.065: EIGRP-Timer: Peer transmission Set Exptime 584942417y18w
*May 31 19:35:15.069: EIGRP-Timer: Hello (Gi0/0) Getting Context
*May 31 19:35:15.071: EIGRP-Timer: NSF RS Send Timer IS NOT running
*May 31 19:35:15.073: EIGRP-Timer: NSF RS Send Timer IS NOT running
*May 31 19:35:15.074: EIGRP-Timer: Hello (Gi0/0) Start Jittered in (20000:15)
*May 31 19:35:15.086: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:35:15.087: EIGRP-Timer: Peer holding
R2# Start in 15000
*May 31 19:35:15.090: EIGRP-Timer: Peer holding Timer IS running
*May 31 19:35:15.091: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:35:15.093: EIGRP-Timer: (parent) is Not Expired
*May 31 19:35:15.093: EIGRP-Timer: (parent) is Not Expired
R2#
*May 31 19:35:17.106: EIGRP-Timer: (parent) is Not Expired
*May 31 19:35:17.107: EIGRP-Timer: (parent) is Expired
*May 31 19:35:17.107: EIGRP-Timer: Peer transmission Getting Context
*May 31 19:35:17.108: EIGRP-Timer: Pacing (Gi0/0) Timer IS NOT running
*May 31 19:35:17.109: EIGRP-Timer: Peer transmission Timer IS running
*May 31 19:35:17.110: EIGRP-Timer: Peer transmission Stop Timer
*May 31 19:35:17.114: EIGRP-Timer: Pacing (Gi0/0) Timer IS NOT running
*May 31 19:35:17.114: EIGRP-Timer: Peer transmission Set Exptime 584942417y18w
*May 31 19:35:17.125: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:35:17.131: EIGRP-Timer: (parent) is Not Expired
*May 31 19:35:17.132: EIGRP-Timer: (parent) is Not Expired
*May 31 19:35:17.133: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:35:17.134: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:35:17.137: EIGRP-Timer: Packetization (Gi0/0) Timer IS NOT running
*May 31 19:35:17.138: EIGRP-Timer: Packetization (Gi0/0) Start in 10
*May 31 19:35:17.139: EIGRP-Timer: Pacing (Gi0/0) Timer IS NOT running
*May 31 19:35:17.140: EIGRP-Timer: Pacing (Gi0/0) Start in 0
*May 31 19:35:17.141: EIGRP-Timer: Peer transmission Timer IS running
*May 31 19:35:17.142: EIGRP-Timer: Peer transmission Stop Timer
*May 31 19:35:17.143: EIGRP-Timer: Pacing (Gi0/0) Timer IS running
*May 31 19:35:17.144: EIGRP-Timer: (parent) is Not Expired
*May 31 19:35:17.145: EIGRP-Timer: (parent) is Expired
(...)
R2#
R2#
R2#
R2#unb 
*May 31 19:35:29.758: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:35:29.763: EIGRP-Timer: Peer holding Timer IS running
*May 31 19:35:29.764: EIGRP-Timer: Peer holding Start in 15000
*May 31 19:35:29.765: EIGRP-Timer: (parent) is Not Expired
*May 31 19:35:29.766: EIGRP-Timer: (parent) is Not Expire 
R2#un all
All possible debugging has been turned off
R2#
R2#
R2#
R2#
*May 31 19:35:35.176: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is down: Interface PEER-TERMINATION received
R2#s          
*May 31 19:35:40.165: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is up: new adjacency
R2#sh ip eigrp int det g0/0 
EIGRP-IPv4 Interfaces for AS(65001)
                              Xmit Queue   PeerQ        Mean   Pacing Time   Multicast    Pending
Interface              Peers  Un/Reliable  Un/Reliable  SRTT   Un/Reliable   Flow Timer   Routes
Gi0/0                    1        0/0       0/0          12       0/0           52           0
  Hello-interval is 20, Hold-time is 15
  Split-horizon is enabled
  Next xmit serial <none>
  Packetized sent/expedited: 19/0
  Hello's sent/expedited: 934/11
  Un/reliable mcasts: 0/18  Un/reliable ucasts: 21/47
  Mcast exceptions: 0  CR packets: 0  ACKs suppressed: 0
  Retransmissions sent: 37  Out-of-sequence rcvd: 5
  Topology-ids on interface - 0 
  Authentication mode is md5,  key-chain is "EIGRP_AUTH"
  Topologies advertised on this interface:  base
  Topologies not advertised on this interface:

R2# 
*May 31 19:35:55.324: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is down: Interface PEER-TERMINATION received
R2#
*May 31 19:36:00.322: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is up: new adjacency
R2#
*May 31 19:36:15.465: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is down: Interface PEER-TERMINATION received
R2#
*May 31 19:36:20.196: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is up: new adjacency
R2#
*May 31 19:36:35.353: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is down: Interface PEER-TERMINATION received
R2#
*May 31 19:36:39.859: %DUAL-5-NBRCHANGE: EIGRP-IPv4 65001: Neighbor 10.1.12.1 (GigabitEthernet0/0) is up: new adjacency
R2#
```

- You can verify the configured timers with the command `show ip eigrp interfaces detail <name> <number>`

### Troubleshooting EIGRP for IPv4 Routes

- After establishing a neighbor relationship, an EIGRP router performs a full exchange of routing information with the newly established neighbor

- After the full exchange, only updates to route information are exchanged with that neighbor

- Routing information learned from EIGRP neighbors is inserted into the EIGRP topology table

- If the EIGRP information happens to be the best source of information, it is installed in the routing table

- There are various reasons EIGRP routes might be missing from either the topology table or the routing table, and you need to be aware of them if you plan on successfully troubleshooting EIGRP route-related problems

- The reasons EIGRP routes might be missing and how to determine why they are missing

- 