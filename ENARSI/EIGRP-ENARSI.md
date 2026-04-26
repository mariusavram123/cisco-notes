## EIGRP ENARSI

- EIGRP Fundamentals

- EIGRP Configuration Modes

- Path Metric Calculation

- *Enhanced Interior Gateway Routing Protocol (EIGRP)* is an enhanced distance vector routing protocol commonly found in enterprise networks

- EIGRP is a derivative of Interior Gateway Routing Protocol (IGRP) but includes support for variable length subnet masking (VLSM) and metrics capable of supporting higher speed interfaces

- Initially, EIGRP was a Cisco proprietary protocol, but it was released to the Internet Engineering Task Force (IETF) through RFC 7868, which was ratified in May 2016

- Here we will see the underlying mechanics of the EIGRP routing protocol and the path metric calculations, and it demonstrates how to configure EIGRP on a router

- Following chapters:

    - Advanced EIGRP

    - Troubleshooting EIGRP for IPv4

    - EIGRPv6

### EIGRP Fundamentals

- EIGRP overcomes the deficiencies of other distance vector routing protocols, such as Routing Information Protocol (RIP), with features such as unequal-cost load balancing, support for networks 255 hops away, and rapid convergence features

- EIGRP uses a *diffusing update algorithm* (DUAL) to identify network paths and provides for fast convergence using precalculated loop-free backup paths

- Most distance vector routing protocols use hop count as the metric for routing decisions

- However, a route selection algorithm that uses only hop count for path selection does not take into account link speed and total delay

- EIGRP adds logic to the route-selection algorithm to use factors other than hop count alone

#### Autonomous Systems

- A router can run multiple EIGRP processes

- Each process operates under the context of an autonomous system, which represents a common routing domain

- Routers within the same domain use the same metric calculation formula and exchange routes only with members of the same *autonomous system* (AS)

- Do not confuse an EIGRP Autonomous System with a Border Gateway Protocol (BGP) autonomous system

- Below, EIGRP AS 100 consists of R1, R2, R3 and R4 and EIGRP AS 200 consists of R3, R5 and R6

- Each EIGRP process correlates to a specific autonomous system and maintains an independent topology table

- R1 does not have knowledge of routes from AS 200 because it is different from it's own autonomous system, AS 100

```
R1(config)#do sh ip ro eigrp | b Gate
Gateway of last resort is not set

      2.0.0.0/32 is subnetted, 1 subnets
D        2.2.2.2 [90/130816] via 10.1.12.2, 00:09:31, GigabitEthernet0/0
      3.0.0.0/32 is subnetted, 1 subnets
D        3.3.3.3 [90/130816] via 10.1.13.2, 00:07:46, GigabitEthernet0/1
      4.0.0.0/32 is subnetted, 1 subnets
D        4.4.4.4 [90/130816] via 10.1.14.2, 00:04:40, GigabitEthernet0/2
```

- R3 is able to participate in both autonomous systems and, by default, does not transfer routes learned from one autonomous system into a different autonomous system

![EIGRP-Autonomous-Systems](./EIGRP-autonomous-systems.png)

- EIGRP uses *protocol dependent modules (PDMs)* to support multiple network protocols, such as IPv4, IPv6, AppleTalk and IPX

- EIGRP is written so that the PDM is responsible for the functions to handle the route selection criteria for each communication protocol

- In theory, new PDMs can be written as new communication protocols are created

- Current implementations of EIGRP support only IPv4 and IPv6

##### EIGRP Terminology

- Some of the core concepts of EIGRP, along with the path selection process

- Below is a reference topology, showing R1 calculating the best path and alternative loop-free paths to the 10.4.4.0/24 network

- A value in parantheses represents the link's calculated metric 

![eigrp-reference-topology](./eigrp-reference-topology.png)

- Important terms related to EIGRP

```
Term                                        Definition

Successor route                             The route with the lowest path metric to reach a destination.
                                            The successor route for R4 to reach 10.4.4.0/24 network is R1-> R3 -> R4

Successor                                   The first next-hop router for the successor route.
                                            R1's successor for 10.4.4.0/24 is R3

Feasible distance (FD)                      The metric value for the lowest path metric to reach a destination.
                                            The feasible distance is calculated locally using the formula shown later.
                                            The FD calculated by R1 for the 10.4.4.0/24 destination network is 3328
                                            (that is, 256 + 256 + 2816)

Reported distance (RD)                      Distance reported by a router to reach a destination. The reported distance value
                                            is the feasible distance for the advertising router.
                                            R3 advertises the 10.4.4.0/24 destination network to R1 and R2 with an RD of 3072.
                                            R4 advertises the 10.4.4.0/24 destination netwotk to R1, R2 and R3 with an RD of 2816

Feasibility condition                       For a route to be considered a backup route, the RD received for that route must be less 
                                            than the FD calculated locally (for the primary route). This logic guarantees a
                                            loop-free path
                                        
Feasible successor                          A route that satisfies the feasibility condition is maintained as a backup route.
                                            The feasibility condition ensures that the backup route is loop-free.
                                            The route R1 -> R4 is the feasible successor because the RD of 2816 is lower than the FD of 3318 for the
                                            R1 -> R3 -> R4 path 
```

#### Topology Table

- EIGRP contains a *topology table*, which makes it different from a true distance vector routing protocol

- EIGRP's topology table is a vital component of DUAL and contains information to identify loop-free backup routes

- The topology table contains all the network prefixes advertised within an EIGRP autonomous system

- Each entry in the table contains the following:

    - Network prefix

    - EIGRP neighbors that have advertised that prefix

    - Metrics for each neighbor (reported distance and hop count)

    - Values used for calculating the metric (load, reliability, total delay, and minimum bandwidth)

- The following command provides the topology table

```
show ip eigrp topology [all-links]
```

- By default, only the successor and feasible successor routes are displayed, but the optional **all-links** keyword shows the paths that did not pass the feasibility condition

- Below is shown the topology table for R1 from our topology

- We will focus on the 10.4.4.0/24 network when explaining the topology table

```
R1#show ip eigrp topology all-links 
EIGRP-IPv4 Topology Table for AS(100)/ID(192.168.1.1)
Codes: P - Passive, A - Active, U - Update, Q - Query, R - Reply,
       r - reply Status, s - sia Status 

P 10.34.1.0/24, 1 successors, FD is 3072, serno 41
        via 10.13.1.3 (3072/2816), GigabitEthernet0/0
        via 10.14.1.4 (28416/2816), GigabitEthernet0/2
        via 10.12.1.2 (28672/3072), GigabitEthernet0/1
P 192.168.4.4/32, 1 successors, FD is 131072, serno 47
        via 10.13.1.3 (131072/130816), GigabitEthernet0/0
        via 10.14.1.4 (156160/128256), GigabitEthernet0/2
        via 10.12.1.2 (156672/131072), GigabitEthernet0/1
P 10.12.1.0/24, 1 successors, FD is 28160, serno 53
        via Connected, GigabitEthernet0/1
P 10.24.1.0/24, 1 successors, FD is 28672, serno 54
        via 10.13.1.3 (28672/28416), GigabitEthernet0/0, serno 23
        via 10.12.1.2 (53760/28160), GigabitEthernet0/1
        via 10.14.1.4 (53760/28160), GigabitEthernet0/2
P 192.168.1.1/32, 1 successors, FD is 128256, serno 4
        via Connected, Loopback0
P 10.4.4.0/24, 1 successors, FD is 131072, serno 48 (feasible distance)
        via 10.13.1.3 (131072/130816), GigabitEthernet0/0  - Successor route
        via 10.14.1.4 (156160/128256), GigabitEthernet0/2  - Feasible successor - passes feasibility condition
        via 10.12.1.2 (156672/131072), GigabitEthernet0/1
                      -> Path metric
                              -> Reported distance  
P 192.168.3.3/32, 1 successors, FD is 130816, serno 10
        via 10.13.1.3 (130816/128256), GigabitEthernet0/0
        via 10.14.1.4 (156416/130816), GigabitEthernet0/2
        via 10.12.1.2 (156416/130816), GigabitEthernet0/1
P 10.14.1.0/24, 1 successors, FD is 28160, serno 45
        via Connected, GigabitEthernet0/2
P 192.168.2.2/32, 1 successors, FD is 131072, serno 55
        via 10.13.1.3 (131072/130816), GigabitEthernet0/0
        via 10.12.1.2 (156160/128256), GigabitEthernet0/1
        via 10.14.1.4 (156672/131072), GigabitEthernet0/2, serno 21
P 10.13.1.0/24, 1 successors, FD is 2816, serno 1
        via Connected, GigabitEthernet0/0
        via 10.12.1.2 (28672/3072), GigabitEthernet0/1
        via 10.14.1.4 (28672/3072), GigabitEthernet0/2
P 10.23.1.0/24, 1 successors, FD is 3072, serno 52
        via 10.13.1.3 (3072/2816), GigabitEthernet0/0
        via 10.12.1.2 (28416/2816), GigabitEthernet0/1
        via 10.14.1.4 (28672/3072), GigabitEthernet0/2

```

- Below we can see that R1 calculates a FD of 131072 for the successor route

- The successor (upstream router) advertises the successor route with an RD of 130816

- The second path entry has a metric of 156160 and has an RD of 128256

- Because 128256 is less than 130816, the second entry passes the feasibility condition, which means the second entry is classified as a feasible successor for the 10.4.4.0/24 prefix

- The 10.4.4.0 route is passive (P), which means the topology is stable

- During a topology change, routes go into an active (A) state when computing a new path

#### EIGRP Neighbors

- Unlike a number of routing protocols - such as Routing Information Protocol (RIP), Open Shortest Path First (OSPF), and Intermediate-system-to-Intermediate-system (IS-IS) - EIGRP does not rely on periodic advertisement of all the network prefixes in an autonomous system

- EIGRP neighbors exchange the entire routing table when forming an adjacency, and they advertise incremental updates only as topology changes occur within a network

- The neighbor adjacency table is vital for tracking neighbor status and the updates sent to each neighbor

##### Inter-Router Communication

- EIGRP uses 5 different packet types to communicate with other routers, as shown below

- EIGRP uses IP protocol number (88) and uses multicast packets where possible; it uses unicast packets when necessary

- Communication between routers is made with multicast using the group address 224.0.0.10 or the MAC address 01:00:5e:00:00:0a when possible

- EIGRP packet types

```
Opcode value                    Packet type                         Function

1                               Update                              Used to transmit routing and reachability information
                                                                    with other EIGRP neighbors

2                               Request                             Used to get specific information from one or more neighbors

3                               Query                               Sent out to search for another path during convergence

4                               Reply                               Sent in response to a query packet

5                               Hello                               Used for discovery of EIGRP neighbors and for detecting when a 
                                                                    neighbor is no longer available
```

- EIGRP uses multicast packets to reduce bandwidth consumed per link; that is, it uses one packet to reach multiple devices

- While broadcast packets are used in the same general way, all nodes on a network segment process broadcast packets, whereas with multicast, only nodes listening for the particular multicast group process the multicast packets

- EIGRP uses *Reliable Transport Protocol (RTP)* to ensure that packets are delivered in order and to ensure that routers receive specific packets

- A sequence number is included in each EIGRP packet

- The sequence value zero do not require a response from the receiving EIGRP router; all other values require an ACK packet that includes the original sequence number

- Ensuring the packets are received makes the transport method reliable

- All update, query and reply packets are deemed reliable, and hello and ACK packets do not require acknowledgement and could be unreliable

- If the originating router does not receive an ACK packet from the neighbor before the retransmit timeout expires, it notifies the non-acknowledging router to stop processing the multicast packets

- The originating router sends all traffic by unicast until the neighbor is fully synchronized

- Upon complete synchronization, the originating router notifies the destination router to start processing multicast packets again

- All unicast packets require acknowledgement

- EIGRP retries up to 16 times for each packet that requires confirmation, and it resets the neighbor relationship when the neighbor reaches the retry limit of 16

- NOTE: In the context of EIGRP, do not confuse RTP with the Real-Time Transport Protocol (RTP), which is used for carrying audio or video over an IP network

- EIGRP's RTP allows for confirmation of packets while supporting multicast

- Other protocols that require reliable connection-oriented communication, such as TCP, cannot use multicast addressing

##### Forming EIGRP Neighbors

- Unlike other distance vector routing protocols, EIGRP requires a neighbor relationship to form before routes are processed and and added to the Routing Information Base (RIB)

- Upon hearing an EIGRP hello packet, a router attempts to become the neighbor of the other router

- The following parameters must match for the two routers to become neighbors:

    - Metric formula K values

    - Primary subnet matches

    - Autonomous system number (ASN) matches

    - Authentication matches

- Below is shown the process EIGRP uses for forming neighbor adjacencies

![eigrp-adjacency-process-r1-perspective](./eigrp-adjacency-process-r1-perspective.png)

1. R1 and R2 send hello to each other

2. R1 sends Update packet (Unicast), with Init Set

3. R2 replies with ACK

4. R1 sends Update packet (Unicast), Routes sent

5. R2 replies with ACK

6. R1 sends Update packet (Unicast), End of table

7. R2 replies with ACK

### EIGRP Configuration Modes

- There are two methods for EIGRP configuration: classic mode and named mode

#### Classic Configuration Mode

- With Classic EIGRP Configuration mode, most of the configuration takes place in the EIGRP process, but some settings are configured under the interface configuration submode

- This can add complexity for deployment and troubleshooting as users must scroll back and forth between the EIGRP process and individual network interfaces

- Some of the settings that are set individually are hello advertisement interval, split-horizon, authentication, and summary-route advertisements

- Classic configuration requires the initialization of the routing process with the global configuration command:

```
conf t
 router eigrp <as-number>
```

- This is used to identify the ASN and initialize the EIGRP process

- The second step is to identify the network interfaces with the following command:

```
conf t
 router eigrp <as-number>
  network <ip-address> <wildcard-mask>
```

- The network command is explained later

#### EIGRP Named Mode

- EIGRP named mode configuration was released to overcome some of the dificulties network engineers have with classic EIGRP autonomous system configuration, including scattered configurations and unclear scope of commands

- EIGRP named configuration provides the following benefits:

    - All the EIGRP configuration occurs in one location

    - It supports current EIGRP features and future developments

    - It supports multiple address families (including virtual routing and forwarding [VRF] instances)

    - EIGRP named configuration is also known as multi-address family configuration mode

    - Commands are clear in terms of the scope of their configuration

- EIGRP named mode provides a hierarchical configuration and stores settings in three subsections:

    - **Address family**: This submode contains settings that are relevant to the global EIGRP AS operations, such as selection of network interfaces, EIGRP K values, and stub settings

    - **Interface**: This submode contains settings that are relevant to the interface, such as hello advertisement interval, split-horizon, authentication, and summary route advertisements

    - In actuality, there are two methods of EIGRP interface section's configuration

    - Commands can be assigned to a specific interface or to a `default` interface, in which case those settings are placed on all EIGRP-enabled interfaces

    - If there is a conflict between the default interface and a specific interface, the specific interface takes priority over the default interface

    - **Topology**: This submode contains settings regarding the EIGRP topology database and how routes are presented to the router's RIB

    - This section also contains route redistribution and administrative distance settings

- EIGRP named configuration makes it possible to run multiple instances under the same EIGRP process

- The process for enabling EIGRP interfaces on a specific instance is as follows:

1. Initialize the EIGRP process by using the following command:

```
conf t
 router eigrp <process-name>
```

- If a number is used for process-name, the number does not correlate to the autonomous system number

2. Initialize the EIGRP instance for the appropriate address family with the command:

```
conf t
 router eigrp <process-name>
  address-family <IPv4|IPv6> <unicast | vrf name> autonomous-system <as-number>
```

3. Enable EIGRP on interfaces using the `network` command

```
conf t
 router eigrp <process-name>
  address-family <IPv4|IPv6> <unicast | vrf name> autonomous-system <as-number>
   network <network> <wildcard-mask>
```

#### EIGRP Network Statement

- Both configuration modes use a `network` statement to identify the interfaces that EIGRP will use

- The `network` statement use a wildcard mask, which allows the configuration to be as specific or as ambiguous as necessary

- The two styles of EIGRP configuration are independent

- Using the configuration options for classic EIGRP autonomous system configuration does not modify settings on a router running EIGRP named configuration

- The syntax for the `network` statement, which exists under the EIGRP process, is:

```
conf t
 router eigrp <as-number>
  network <ip-address> [wildcard-mask]
```

- The optional wildcard-mask can be omitted to enable interfaces that fail within the classful boundaries for that `network` statement

- A common misconception is that the `network` statements adds prefixes to the EIGRP topology table

- In reality, the `network` statement identifies the interface to enable EIGRP on, and it adds the interface's connected network to the EIGRP topology table

- EIGRP then advertises the topology table to other routers in the EIGRP autonomous system

- EIGRP does not add an interface's secondary connected network to the topology table

- For secondary connected networks to be installed in the EIGRP routing table, they must be redistributed into the EIGRP process

- To help illustrate the concept of wildcard mask, below is provided a set of IP addresses and interfaces for a router

- The examples that follow provide configurations to match specific scenarios

```
Router Interface                                                IP address

Gigabit Ethernet 0/0                                            10.0.0.10/24

Gigabit Ethernet 0/1                                            10.0.10.10/24

Gigabit Ethernet 0/2                                            192.0.0.10/24

Gigabit Ethernet 0/3                                            192.10.0.10/24
```

- The configuration from below example enables EIGRP only on interfaces that explicitly match the IP addresses from our table

```
conf t
 router eigrp 1
  network 10.0.0.10 0.0.0.0
  network 10.0.10.10 0.0.0.0
  network 192.0.0.10 0.0.0.0
  network 192.10.0.10 0.0.0.0
```

- Below is shown the EIGRP configuration using `network` statements that match the subnets used in our table:

```
conf t
 router eigrp 1
  network 10.0.0.0 0.0.0.255
  network 10.0.10.0 0.0.0.255
  network 192.0.0.0 0.0.0.255
  network 192.10.0.0 0.0.0.255
```

- The following example shows the EIGRP configuration using `network` statements for interfaces that are within 10.0.0.0/8 or 192.0.0.0/8

```
conf t
 router eigrp 1
 network 10.0.0.0 0.255.255.255
 network 192.0.0.0 0.255.255.255
```

- The follwing snippet shows the configuration to enable all interfaces with EIGRP:

```
conf t
 router eigrp 1
  network 0.0.0.0 255.255.255.255
```

- A key topic with wildcard `network` statements is that large ranges simplify configuration; however they may possibly enable EIGRP on interfaces where not intended

#### Sample Topology and Configuration

- Below is shown a sample topology for demonstrating EIGRP configuration in classic mode for R1 and named mode for R2

![eigrp-sample-topology](./eigrp-sample-topology.png)

- R1 and R2 enable EIGRP on all their interfaces

- R1 configures EIGRP using multiple specific interface addresses, and R2 enables EIGRP on all network interfaces with one command

- Below is provided the configuration that is applied to R1 and R2

- R1 - classic configuration:

```
conf t
 interface l0
  ip address 192.168.1.1 255.255.255.255

 interface g0/1
  ip address 10.12.1.1 255.255.255.0

 interface g0/2
  ip address 10.11.11.1 255.255.255.0

 router eigrp 100
  network 10.11.11.1 0.0.0.0
  network 10.12.1.1 0.0.0.0
  network 192.168.1.1 0.0.0.0
```

- R2 - named configuration mode:

```
conf t
 interface l0
  ip address 192.168.2.2 255.255.255.255

 interface g0/1
  ip address 10.12.1.2 255.255.255.0

 interface g0/2
  ip address 10.22.22.2 255.255.255.0

 router eigrp EIGRP-NAMED
  address-family ipv4 unicast autonomous-system 100
   network 0.0.0.0 255.255.255.255
```

- As mentioned, EIGRP named mode has three configuration submodes

- The configuration in our example uses only the EIGRP address-family submode section, which uses the `network` statement

- The EIGRP topology base submode is created automatically with the command `topology base`, and exited with the command `exit-af-topology`

```
conf t
 router eigrp EIGRP-NAMED
  address-family ipv4 unicast autonomous-system 100
   topology base
   exit-af-topology
```

- Settings for the topology submode are listed between the two commands

- Below is demonstrated the slight difference in how the configuration is stored on the router between EIGRP classic and named mode configurations

- R1:

```
R1#sh run | s router eigrp
router eigrp 100
 network 10.11.11.1 0.0.0.0
 network 10.12.1.1 0.0.0.0
 network 192.168.1.1 0.0.0.0
```

- R2:

```
R2#sh run | s router eigrp
router eigrp EIGRP-NAMED
 !
 address-family ipv4 unicast autonomous-system 100
  !
  topology base
  exit-af-topology
  network 0.0.0.0
 exit-address-family
```

- The EIGRP interface submode configurations contains the command `af-interface <interface-id>` or `af-interface default`, with any specific commands listed immediately

- The EIGRP interface submode configuration is exited with the command `exit-af-interface`

```
conf t
 router eigrp EIGRP-NAMED
  address-family ipv4 unicast autonomous-system 100
   af-interface g0/1
   exit-af-interface
```

#### Confirming Interfaces

- Upon configuring EIGRP, it is a good practice to verify that only the intended interfaces are running EIGRP

- The command `show ip eigrp interfaces [interface-id]| [detail] [interface-id]` shows active EIGRP interfaces

- Appending the optional `detail` keyword provides additional information such as authentication, EIGRP timers, split horizon, and various packet counts

- Below we can see R1's non-detailed EIGRP interface and R2's detailed information for the G0/1 interface

- CML lab topology

![eigrp-topology](./eigrp-topology.png)

- R1:

```
R1#show ip eigrp interfaces 
EIGRP-IPv4 Interfaces for AS(100)
                              Xmit Queue   PeerQ        Mean   Pacing Time   Multicast    Pending
Interface              Peers  Un/Reliable  Un/Reliable  SRTT   Un/Reliable   Flow Timer   Routes
Gi0/2                    0        0/0       0/0           0       0/0            0           0
Gi0/1                    1        0/0       0/0        1678       0/0         7996           0
Lo0                      0        0/0       0/0           0       0/0            0           0
```

- R2:

```
R2#show ip eigrp interfaces detail g0/1
EIGRP-IPv4 VR(EIGRP-NAMED) Address-Family Interfaces for AS(100)
                              Xmit Queue   PeerQ        Mean   Pacing Time   Multicast    Pending
Interface              Peers  Un/Reliable  Un/Reliable  SRTT   Un/Reliable   Flow Timer   Routes
Gi0/1                    1        0/0       0/0         128       0/0          640           0
  Hello-interval is 5, Hold-time is 15
  Split-horizon is enabled
  Next xmit serial <none>
  Packetized sent/expedited: 4/0
  Hello's sent/expedited: 380/2
  Un/reliable mcasts: 0/4  Un/reliable ucasts: 4/2
  Mcast exceptions: 0  CR packets: 0  ACKs suppressed: 0
  Retransmissions sent: 1  Out-of-sequence rcvd: 0
  Topology-ids on interface - 0 
  Authentication mode is not set
  Topologies advertised on this interface:  base
  Topologies not advertised on this interface:

```

- R3

```
R3#show ip eigrp interfaces detail g1
EIGRP-IPv4 VR(EIGRP-NAMED) Address-Family Interfaces for AS(100)
                              Xmit Queue   PeerQ        Mean   Pacing Time   Multicast    Pending
Interface              Peers  Un/Reliable  Un/Reliable  SRTT   Un/Reliable   Flow Timer   Routes
Gi1                      1        0/0       0/0           1       0/0           50           0
  Hello-interval is 5, Hold-time is 15
  Split-horizon is enabled
  Next xmit serial <none>
  Packetized sent/expedited: 2/0
  Hello's sent/expedited: 9/2
  Un/reliable mcasts: 0/2  Un/reliable ucasts: 2/1
  Mcast exceptions: 0  CR packets: 0  ACKs suppressed: 0
  Retransmissions sent: 0  Out-of-sequence rcvd: 0
  Topology-ids on interface - 0 
  Authentication mode is not set
  Topologies advertised on this interface:  base
  Topologies not advertised on this interface:

```

- Below is shown a brief explanation to the key fields shown with EIGRP interfaces

```
Field                               Description

Interface                           Interfaces running EIGRP

Peers                               Number of peers detected on the interface

XMT Queue                           Number of unreliable/reliable packets remaining in the transmit queue
Un/Reliable                         The value 0 is an indication of a stable network

Mean SRTT                           Average time for a packet to be sent to a neighbor and a reply from that neighbor to be received, in miliseconds

Multicast Flow Timer                Maximum time (seconds) that the router sent multicast packets

Pending Routes                      Number of routes in the transmit queue that need to be sent
```

#### Verifying EIGRP Neighbor Adjacencies

- Each EIGRP process maintains a table of neighbors to ensure they are alive and processing updates properly

- If EIGRP didn't keep track of neighbor states, an autonomous system could contain incorrect data and could potentially route traffic improperly

- EIGRP must form a neighbor relationship before a router advertises update packets containing network prefixes

- The command `show ip eigrp neighbors [interface-id]` displays the EIGRP neighbors for a router

- Below is shown the EIGRP neighbor information obtained using this command

```
R1#show ip eigrp neighbors 
EIGRP-IPv4 Neighbors for AS(100)
H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)         (ms)       Cnt Num
1   10.13.1.3               Gi0/0                    11 00:31:04    1   100  0  3
0   10.12.1.2               Gi0/1                    10 00:59:28 1073  5000  0  5
```

- Below is provided a brief explanation of the key fields shown above

```
Field                               Description

Address                             IP address of the EIGRP neighbor

Interface                           Interface the neighor was detected on

Holdtime                            Time left to receive a packet from this neighbor to ensure that it is still alive

SRTT                                Time for a packet to be sent to a neighbor and a reply to be received from that neighbor, in miliseconds

RTO                                 Timeout for transmission (waiting for ACK)

Q cnt                               Number of packets (Update, Query, Reply) in queue for sending

Seq Num                             Sequence number that was last received from this router
```

#### Displaying Installed EIGRP Routes

- You can see EIGRP routes that are installed into the RIB by using the following command:

```
show ip route eigrp
```

- EIGRP routes that originate within the autonomous system have an administrative distace (AD) of 90 and are indicated in the routing table with a D

- Routes that originate from outside the autonomous system are external EIGRP routes

- External EIGRP routes have an AD of 170 and are indicated in the routing table with D EX

- Placing external EIGRP routes into the RIB with a higher AD acts as a loop-prevention mechanism

- Below are displayed the EIGRP routes from our topology

- The metric for the selected route is the second number in brackets

- R1:

```
R1#show ip route eigrp 
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 9 subnets, 2 masks
D        10.22.22.0/24 [90/3072] via 10.13.1.3, 00:19:38, GigabitEthernet0/0
                       [90/3072] via 10.12.1.2, 00:19:38, GigabitEthernet0/1
      192.168.2.0/32 is subnetted, 1 subnets
D        192.168.2.2 [90/2848] via 10.12.1.2, 00:18:23, GigabitEthernet0/1
      192.168.3.0/32 is subnetted, 1 subnets
D        192.168.3.3 [90/2848] via 10.13.1.3, 00:18:18, GigabitEthernet0/0
```

- R2:

```
R2#show ip route eigrp 
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
D        10.11.11.0/24 [90/15360] via 10.12.1.1, 00:19:10, GigabitEthernet0/1
D        10.13.1.0/24 [90/15360] via 10.22.22.3, 00:19:10, GigabitEthernet0/2
                      [90/15360] via 10.12.1.1, 00:19:10, GigabitEthernet0/1
D EX     10.111.111.0/24 
           [170/15360] via 10.12.1.1, 00:12:32, GigabitEthernet0/1
      192.168.1.0/32 is subnetted, 1 subnets
D        192.168.1.1 [90/2570240] via 10.12.1.1, 00:19:10, GigabitEthernet0/1
      192.168.3.0/32 is subnetted, 1 subnets
D        192.168.3.3 [90/10880] via 10.22.22.3, 00:19:10, GigabitEthernet0/2
```

- R3:

```
R3#show ip route eigrp 
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, m - OMP
       n - NAT, Ni - NAT inside, No - NAT outside, Nd - NAT DIA
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       H - NHRP, G - NHRP registered, g - NHRP registration summary
       o - ODR, P - periodic downloaded static route, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR
       & - replicated local route overrides by connected

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
D        10.11.11.0/24 [90/15360] via 10.13.1.1, 00:19:48, GigabitEthernet1
D        10.12.1.0/24 [90/15360] via 10.22.22.2, 00:19:48, GigabitEthernet2
                      [90/15360] via 10.13.1.1, 00:19:48, GigabitEthernet1
D EX     10.111.111.0/24 [170/15360] via 10.13.1.1, 00:13:05, GigabitEthernet1
      192.168.1.0/32 is subnetted, 1 subnets
D        192.168.1.1 [90/2570240] via 10.13.1.1, 00:19:48, GigabitEthernet1
      192.168.2.0/32 is subnetted, 1 subnets
D        192.168.2.2 [90/10880] via 10.22.22.2, 00:19:48, GigabitEthernet2
```

- The metrics from R2's routes are different from the metrics from R1's routes

- This is because R1's classic EIGRP mode uses classic metrics, and R2's named mode uses wide metrics by default

#### Router ID

- The Router ID (RID) is a 32-bit number that uniquely identifies an EIGRP router and is used as a loop-prevention mechanism

- The RID can be set dynamically, which is the default or manually

- The algorithm for dynamically choosing the EIGRP RID uses the highest IPv4 address of any up loopback interfaces

- If there are not any up loopback interfaces, the highest IPv4 address of any active up physical interfaces becomes the RID when the EIGRP process initializes

- IPv4 addresses are commonly used for the RID because they are 32-bits and are maintained in dotted-decimal format

- Use the following command to set the RID of the EIGRP process

```
eigrp router-id <router-id>
```

- Classic configuration mode (R1):

```
conf t
 router eigrp 100
  eigrp router-id 192.168.1.1
```

- Named mode (R2):

```
conf t
 router eigrp EIGRP-NAMED
  address-family ipv4 unicast autonomous-system 100
   eigrp router-id 192.168.2.2
```

- R1:

```
R1(config-router)#do sh run | s router eigrp
router eigrp 100
 network 10.11.11.1 0.0.0.0
 network 10.12.1.1 0.0.0.0
 network 10.13.1.1 0.0.0.0
 network 10.112.1.0 0.0.0.255
 network 192.168.1.1 0.0.0.0
 redistribute rip metric 1000000 1 255 1 1500
 eigrp router-id 192.168.1.1
```

- R2:

```
R2(config-router-af)#do sh run | s router eigrp
router eigrp EIGRP-NAMED
 !
 address-family ipv4 unicast autonomous-system 100
  !
  topology base
  exit-af-topology
  network 0.0.0.0
  eigrp router-id 192.168.2.2
 exit-address-family
```

#### Passive Interfaces

- Some network segments must advertise a network segment into EIGRP but need to prevent neighbors from forming adjacencies with other routers on that segment

- This might be the case, for example, when advertising access layer networks in a campus topology

- In such a scenario, you need to put the EIGRP interface in a passive state

- Passive EIGRP interfaces do not send out or process EIGRP hellos, which prevents EIGRP from forming adjacencies on these interfaces

- To configure an EIGRP interface as passive, you use the following command, under the EIGRP process for classic configuration:

```
conf t
 router eigrp 100
  passive-interface <interface-id>
```

- Another option is to configure all interfaces as passive by default, and then allow an interface to process EIGRP packets, preempting the global `passive-interface default` configuration

```
conf t
 router eigrp 100
  passive-interface default
  no passive-interface g0/2
```

- R1:

```
R1(config-router)#do sh run | s router eigrp
router eigrp 100
 network 10.11.11.1 0.0.0.0
 network 10.12.1.1 0.0.0.0
 network 10.13.1.1 0.0.0.0
 network 192.168.1.1 0.0.0.0
 redistribute rip metric 100000 1 255 1 1500
 passive-interface default
 no passive-interface Ethernet0/1
 no passive-interface Ethernet0/0
```

- For a named mode configuration, you place the `passive-interface` state on an `af-interface default` for all EIGRP interfaces or on a specific interface with the `af-interface <interface-id>` section

- Below is shown how to make g0/2 interface as passive while allowing the g0/1 interface to be active, using both configuration strategies

- R2:

```
router eigrp EIGRP-NAMED
 address-family ipv4 unicast autonomous-system 100
  af-interface g0/2
   passive-interface
```

```
router eigrp EIGRP-NAMED
 address-family ipv4 unicast autonomous-system 100
  af-interface default
   passive-interface
  af-interface g0/1
   no passive-interface
```

- Below is shown what the named mode configuration looks like with some settings (that is, passive-interface, and no passive-interface) placed under the `af-interface default` and `af-interface <interface-id>` settings

```
R2(config-router-af-interface)#do sh run | s router eigrp
router eigrp EIGRP-NAMED
 !
 address-family ipv4 unicast autonomous-system 100
  !
  af-interface default
   passive-interface
  exit-af-interface
  !
  af-interface Ethernet0/1
   no passive-interface
  exit-af-interface
  !
  topology base
  exit-af-topology
  network 0.0.0.0
 exit-address-family
```

- A passive interface do not appear in the output of `show ip eigrp interfaces` even though it was enabled

- Connected networks for passive interfaces are still added to the EIGRP topology table so that they are advertised to neighbors

- Below is shown that the g0/2 interface on R1 no longer appears, compared with previous output

```
R1#show ip eigrp interfaces 
EIGRP-IPv4 Interfaces for AS(100)
                              Xmit Queue   PeerQ        Mean   Pacing Time   Multicast    Pending
Interface              Peers  Un/Reliable  Un/Reliable  SRTT   Un/Reliable   Flow Timer   Routes
Et0/1                    1        0/0       0/0           2       0/2           50           0
Et0/0                    1        0/0       0/0           1       0/2           50           0
```

- To accelerate troubleshooting of passive interfaces, as well as other settings, use the command `show ip protocols` which provides a lot of valuable information about all the routing protocols

- With EIGRP, it displays the EIGRP process identifier, the ASN, K values, that are used for path calculation, RID, neighbors, AD settings, and all passive interfaces

- Below is the output for both R1 and R2, for classic and named mode

- R1:

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

Routing Protocol is "eigrp 100"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Default networks flagged in outgoing updates
  Default networks accepted from incoming updates
  Redistributing: rip
  EIGRP-IPv4 Protocol for AS(100)
    Metric weight K1=1, K2=0, K3=1, K4=0, K5=0
    Soft SIA disabled
    NSF-aware route hold timer is 240
  Passive Interface(s):
    Router-ID: 192.168.1.1
    Topology : 0 (base) 
      Active Timer: 3 min
      Distance: internal 90 external 170
      Maximum path: 4
      Maximum hopcount 100
      Maximum metric variance 1
      Total Prefix Count: 8
      Total Redist Count: 1

  Automatic Summarization: disabled
  Maximum path: 4
  Routing for Networks:
    10.11.11.1/32
    10.12.1.1/32
    10.13.1.1/32
    192.168.1.1/32
  Passive Interface(s):
    Ethernet0/2
    Loopback0
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.13.1.3             90      00:31:53
  Passive Interface(s):
    10.12.1.2             90      00:31:53
  Distance: internal 90 external 170

Routing Protocol is "rip"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Sending updates every 30 seconds, next due in 25 seconds
  Invalid after 180 seconds, hold down 180, flushed after 240
  Redistributing: eigrp 100, rip
  Default version control: send version 2, receive version 2
    Interface                           Send  Recv  Triggered RIP  Key-chain
    Ethernet0/0                         2     2          No        none            
    Ethernet0/1                         2     2          No        none            
    Ethernet0/2                         2     2          No        none            
    Loopback3                           2     2          No        none            
  Automatic network summarization is not in effect
  Maximum path: 4
  Routing for Networks:
    10.0.0.0
  Passive Interface(s):
  Routing Information Sources:
    Gateway         Distance      Last Update
  Distance: (default is 120)

```

- R2:

```
R2#show ip protocols 
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

Routing Protocol is "eigrp 100"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Default networks flagged in outgoing updates
  Default networks accepted from incoming updates
  EIGRP-IPv4 VR(EIGRP-NAMED) Address-Family Protocol for AS(100)
    Metric weight K1=1, K2=0, K3=1, K4=0, K5=0 K6=0
    Metric rib-scale 128
    Metric version 64bit
    Soft SIA disabled
  Passive Interface(s):
    NSF-aware route hold timer is 240
    Router-ID: 192.168.2.2
    Topology : 0 (base) 
      Active Timer: 3 min
      Distance: internal 90 external 170
      Maximum path: 4
      Maximum hopcount 100
      Maximum metric variance 1
      Total Prefix Count: 8
      Total Redist Count: 0

  Automatic Summarization: disabled
  Maximum path: 4
  Routing for Networks:
    0.0.0.0
  Passive Interface(s):
    Loopback0
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.12.1.1             90      00:32:31
    10.22.22.3            90      00:32:31
  Distance: internal 90 external 170

```

- Set metric version to 32-bit value for R2 - named mode:

```
conf t
 router eigrp EIGRP-named
  address-family ipv4 unicast autonomous-system 100
   metric version 32-bit
```

- R1:

```
R1(config-router)#do sh ip eigrp interf
EIGRP-IPv4 Interfaces for AS(100)
                              Xmit Queue   PeerQ        Mean   Pacing Time   Multicast    Pending
Interface              Peers  Un/Reliable  Un/Reliable  SRTT   Un/Reliable   Flow Timer   Routes
Gi0/1                    1        0/0       0/0           1       0/0           50           0
Gi0/0                    1        0/0       0/0           1       0/0           50           0
```

```
R1(config-router)#do sh ip proto
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

Routing Protocol is "eigrp 100"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Default networks flagged in outgoing updates
  Default networks accepted from incoming updates
  Redistributing: rip
  EIGRP-IPv4 Protocol for AS(100)
    Metric weight K1=1, K2=0, K3=1, K4=0, K5=0
    Soft SIA disabled
    NSF-aware route hold timer is 240
    Router-ID: 192.168.1.1
    Topology : 0 (base) 
      Active Timer: 3 min
      Distance: internal 90 external 170
      Maximum path: 4
      Maximum hopcount 100
      Maximum metric variance 1

  Automatic Summarization: disabled
  Maximum path: 4
  Routing for Networks:
    10.11.11.1/32
    10.12.1.1/32
    10.13.1.1/32
    10.112.1.0/24
    192.168.1.1/32
  Passive Interface(s):
    GigabitEthernet0/2
    Loopback0
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.13.1.3             90      00:01:24
    10.12.1.2             90      00:01:24
  Distance: internal 90 external 170

Routing Protocol is "rip"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Sending updates every 30 seconds, next due in 27 seconds
  Invalid after 180 seconds, hold down 180, flushed after 240
  Redistributing: eigrp 100, rip
  Default version control: send version 2, receive version 2
    Interface                           Send  Recv  Triggered RIP  Key-chain
    GigabitEthernet0/0                  2     2          No        none            
    GigabitEthernet0/1                  2     2          No        none            
    GigabitEthernet0/2                  2     2          No        none            
    Loopback1                           2     2          No        none            
  Automatic network summarization is not in effect
  Maximum path: 4
  Routing for Networks:
    10.0.0.0
  Routing Information Sources:
    Gateway         Distance      Last Update
  Distance: (default is 120)

```

- R3:

```
R3#sh run | s router eigrp
router eigrp EIGRP-NAMED
 !
 address-family ipv4 unicast autonomous-system 100
  !
  af-interface default
   passive-interface
  exit-af-interface
  !
  af-interface GigabitEthernet1
   no passive-interface
  exit-af-interface
  !
  af-interface GigabitEthernet2
   no passive-interface
  exit-af-interface
  !
  topology base
  exit-af-topology
  network 0.0.0.0
  metric version 32bit
 exit-address-family
```

```
R3#sh ip eigrp interfaces 
EIGRP-IPv4 VR(EIGRP-NAMED) Address-Family Interfaces for AS(100)
                              Xmit Queue   PeerQ        Mean   Pacing Time   Multicast    Pending
Interface              Peers  Un/Reliable  Un/Reliable  SRTT   Un/Reliable   Flow Timer   Routes
Gi1                      1        0/0       0/0           1       0/0           50           0
Gi2                      1        0/0       0/0           3       0/0           50           0
```

```
R3#sh ip proto
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

Routing Protocol is "eigrp 100"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Default networks flagged in outgoing updates
  Default networks accepted from incoming updates
  EIGRP-IPv4 VR(EIGRP-NAMED) Address-Family Protocol for AS(100)
    Metric weight K1=1, K2=0, K3=1, K4=0, K5=0 K6=0
    Metric rib-scale 1
    Metric version 32bit
    Soft SIA disabled
    NSF-aware route hold timer is 240
  EIGRP NSF disabled
     NSF signal timer is 20s
     NSF converge timer is 120s
    Router-ID: 192.168.3.3
    Topology : 0 (base) 
      Active Timer: 3 min
      Distance: internal 90 external 170
      Maximum path: 4
      Maximum hopcount 100
      Maximum metric variance 1
      Total Prefix Count: 9
      Total Redist Count: 0

  Automatic Summarization: disabled
  Maximum path: 4
  Routing for Networks:
    0.0.0.0
  Passive Interface(s):
    Loopback0
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.13.1.1             90      00:17:56
    Gateway         Distance      Last Update
    10.22.22.2            90      00:17:57
  Distance: internal 90 external 170
```

#### Authentication

- Authentication is a mechanism for ensuring that only authorized routers are eligible to become EIGRP neighbors

- It is possible for someone to add a router to a network and introduce invalid routes accidentally or maliciously

- Authentication prevents such scenarios from happening

- A precomputed password hash is included with all EIGRP packets, and the receiving router decrypts the hash

- If the password do not match for a packet, the router discards the packet

- EIGRP encrypts the password using Message Digest 5 (MD5) authentication and the hash function

- The hash consists of the key number and the password

- EIGRP authentication encrypts just the password rather than entire EIGRP packet

- Keychain functionality allows a password to be valid for a specific time, so passwords can change at preconfigured times

- To configure EIGRP authentication, you need to create a key chain and then enable EIGRP authentication on the interface

##### Keychain Configuration

- Keychain creation is accomplished in the following steps:

    1. Create the keychain using the command: `key chain <key-chain-name>`

    2. Identify the key sequence by using the command `key <key-number>`, where key number can be anything from 0 to 2147483647

    3. Specify the preshared password by using the command `key-string <password>`

```
conf t
 key chain <key-chain-name>
  key 1
   key-string <password>
```

- Be careful to not use a space after the password because the password, including any trailing space, will be used for computing the hash

##### Enabling Authentication on the Interface

- When using classic configuration, authentication must be enabled on the interface under the interface configuration submode

- The following commands are used in the interface configuration submode

```
conf t
 interface <name>
  ip authentication key-chain eigrp <as-number> <key-chain-name>
  ip authentication mode eigrp <as-number> md5
```

- R1:

```
conf t
 key chain EIGRP-CHAIN
  key 1
   key-string MARIUS12345

 interface range g0/0-1
  ip authentication key-chain eigrp 100 EIGRP-CHAIN
  ip authentication mode eigrp 100 md5
```

- The named mode configuration places the configurations under the EIGRP interface submode, under `af-interface default` or `af-interface <interface-name>`

- Named mode configuration supports MD5 or *Hashed Message Authentication Code-Secure Hash Algorithm-256* (HMAC-SHA-256) authentication

- MD5 authentication involves the following commands:

```
 af-interface <interface|default>
  authentication key-chain <key-chain-name>
  authentication mode md5
```

- HMAC-SHA-256 authentication involves the following command:

```
 af-interface <interface|default>
  authentication mode hmac-sha-256 <password>
```

- R2:

```
conf t
 key-chain EIGRP-CHAIN
  key 1
   key-string MARIUS12345

 router eigrp EIGRP-NAMED
  address-family ipv4 unicast autonomous-system 100
   af-interface g0/1
    authentication key-chain EIGRP-CHAIN
    authentication mode md5
   af-interface g0/2
    authentication key-chain EIGRP-CHAIN
    authentication mode hmac-sha-256 MARIUS12345
```

- R3:

```
conf t
 key chain EIGRP-CHAIN
  key 1
   key-string MARIUS12345

 router eigrp EIGRP-NAMED
  address-family ipv4 unicast autonomous-system 100
   af-interface g1
    authentication mode md5
    authentication key-chain EIGRP-CHAIN

   af-interface GigabitEthernet2
    authentication mode hmac-sha-256 MARIUS12345
    authentication key-chain EIGRP-CHAIN
```

- R1:

```
R1(config)#do sh run | s key chain|router eigrp
key chain EIGRP-CHAIN
 key 1
  key-string MARIUS12345
router eigrp 100
 network 10.11.11.1 0.0.0.0
 network 10.12.1.1 0.0.0.0
 network 10.13.1.1 0.0.0.0
 network 10.112.1.0 0.0.0.255
 network 192.168.1.1 0.0.0.0
 redistribute rip metric 1000000 1 255 1 1500
 passive-interface GigabitEthernet0/2
 passive-interface Loopback0
```

- R2:

```
R2(config)#do sh run | s key chain|router eigrp
key chain EIGRP-CHAIN
 key 1
  key-string MARIUS12345
router eigrp EIGRP-NAMED
 !
 address-family ipv4 unicast autonomous-system 100
  !
  af-interface default
   passive-interface
  exit-af-interface
  !
  af-interface GigabitEthernet0/1
   authentication mode md5
   authentication key-chain EIGRP-CHAIN
   no passive-interface
  exit-af-interface
  !
  af-interface GigabitEthernet0/2
   authentication mode hmac-sha-256 MARIUS12345
   authentication key-chain EIGRP-CHAIN
   no passive-interface
  exit-af-interface
  !
  topology base
  exit-af-topology
  network 0.0.0.0
  metric rib-scale 1
 exit-address-family
```

- R3:

```
R3#sh run | s key chain|router eigrp
key chain EIGRP-CHAIN
 key 1
  key-string MARIUS12345
router eigrp EIGRP-NAMED
 !
 address-family ipv4 unicast autonomous-system 100
  !
  af-interface default
   passive-interface
  exit-af-interface
  !
  af-interface GigabitEthernet1
   authentication mode md5
   authentication key-chain EIGRP-CHAIN
   no passive-interface
  exit-af-interface
  !
  af-interface GigabitEthernet2
   authentication mode hmac-sha-256 MARIUS12345
   authentication key-chain EIGRP-CHAIN
   no passive-interface
  exit-af-interface
  !
  topology base
  exit-af-topology
  network 0.0.0.0
  metric rib-scale 1
 exit-address-family
```

- Remember that the hash is computed using the key sequence number and the key string, which must match on the two nodes

- The command `show key chain` provides verification of the key chain. Each key sequence provides the lifetime and password

```
R1#show key chain 
Key-chain EIGRP-AUTH:
Key-chain EIGRP-CHAIN:
    key 1 -- text "MARIUS12345"
        accept lifetime (always valid) - (always valid) [valid now]
        send lifetime (always valid) - (always valid) [valid now]
```

- The EIGRP interface detail view provides verification of EIGRP authentication on a specific interface

- Below is shown the detailed EIGRP interface output

```
R1#sh ip eigrp interfaces detail 
EIGRP-IPv4 Interfaces for AS(100)
                              Xmit Queue   PeerQ        Mean   Pacing Time   Multicast    Pending
Interface              Peers  Un/Reliable  Un/Reliable  SRTT   Un/Reliable   Flow Timer   Routes
Gi0/1                    1        0/0       0/0           1       0/0           50           0
  Hello-interval is 5, Hold-time is 15
  Split-horizon is enabled
  Next xmit serial <none>
  Packetized sent/expedited: 21/2
  Hello's sent/expedited: 1925/5
  Un/reliable mcasts: 0/19  Un/reliable ucasts: 28/9
  Mcast exceptions: 0  CR packets: 0  ACKs suppressed: 1
  Retransmissions sent: 3  Out-of-sequence rcvd: 0
  Topology-ids on interface - 0 
  Authentication mode is md5,  key-chain is "EIGRP-CHAIN"
  Topologies advertised on this interface:  base
  Topologies not advertised on this interface:

Gi0/0                    1        0/0       0/0           1       0/0           50           0
  Hello-interval is 5, Hold-time is 15
  Split-horizon is enabled
  Next xmit serial <none>
  Packetized sent/expedited: 21/1
  Hello's sent/expedited: 1925/5
  Un/reliable mcasts: 0/16  Un/reliable ucasts: 26/11
  Mcast exceptions: 0  CR packets: 0  ACKs suppressed: 2
  Retransmissions sent: 2  Out-of-sequence rcvd: 0
  Topology-ids on interface - 0 
  Authentication mode is md5,  key-chain is "EIGRP-CHAIN"
  Topologies advertised on this interface:  base
  Topologies not advertised on this interface:

```

### Path Metric Calculation

- Metric calculation is a critical component for any routing protocol

- EIGRP uses multiple factors to calculate the metric for a path

- Metric calculation uses *bandwidth* and *delay* by default but can include interface load and reliability, too

- Below is shown the EIGRP classic metric formula

```
Metric = 256 x [(K1 x Bandwidth + (K2 x Bandwidth) / (256 - Load) + K3 x Delay + K5 / (K4 + Reliability ))]
```

- EIGRP uses K values to define which factors the formula uses and the impact associated with a factor when calculating the metric

- A common misconception is that the K values directly apply to bandwidth, load, delay, or reliability; this is not accurate

- For example, K1 and K2 both reference bandwidth (BW)

- BW represents the slowest link in the path, scaled to a 10 Gbps link (10 ^ 7)

- Link speed correlates with the configured interface bandwidth on an interface and is measured in kilobits per second (Kbps)

- Delay is the total measure of delay in the path, measured in tens of microseconds (us)

- Taking these definitions into consideration, look at the formula for classic EIGRP metrics below

```
Metric = 256 * [(K1 x 10 ^ 7 / Min_bandwidth + (10 ^ 7 / K2 * Min_bandwidth)/ (256 - Load) + (K3 * Total_delay) / 10) * K5 / (K4 + Reliability)]
```

![eigrp-classic-metric-formula-definitions](./eigrp-classic-metric-formula-definitions.png)

- RFC 7868 states that if K5 = 0, then the reliability quotient is defined to be 1

- This is demonstrated in the figure below

- By default, K1 and K3 each has a value of 1, and K2, K4 and K5 are all set to 0

- Below the default K values are placed into the formula and is shown a streamlined version of the formula

- The EIGRP Update packet includes path attributes associated with each prefix

- The EIGRP path attributes can include hop count, cummulative delay, minimum bandwidth link speed, and RD

- These attributes are updated each hop along the way, allowing each router to independently identify the shortest path

```
Metric = 256 * [(1 x 10 ^ 7 / Min_bandwidth + (10 ^ 7) / (0 x Min_bandwidth)/ 256 - Load + 1 x Total_delay / 10) * 0 / 0 + Reliability]


Metric = 256 * (10 ^ 7 / Min_bandwidth + Total_delay / 10)
```

![eigrp-formula-default-k-values](./eigrp-formula-default-k-values.png)

- Below is shown the information in the EIGRP update packets for the 10.1.1.0/24 network propagating through the autonomous system

- Notice that the hop count increments, minimum bandwidth decreases, and the RD changes with each EIGRP update

![eigrp-attribute-propagation](./eigrp-attribute-propagation.png)

- Below are shown some common network types, the link speed, delay and EIGRP metric, based on the streamlined formula

- Default EIGRP interface metrics for classic metrics

```
Interface Type                  Link speed (Kbps)                   Delay                   Metric

Serial                          64                                  20.000 us               40.512.000

T1                              1544                                20.000 us               2.170.031

Ethernet                        10000                               1000 us                 281.600

FastEthernet                    100000                              100 us                  28.160

GigabitEthernet                 1000000                             10 us                   2816

TenGigabitEthernet              10000000                            10 us                   512
```

- Using our original topology, the metrics from R1 and R2 for the 10.4.4.0/24 network are calculated using our formula

- The link speed for both routers is 1 Gbps, and the total delay is 30 us (10 us for the 10.4.4.0/24, 10 us for the 10.34.1.0/24 link, and 10 us for the 10.13.1.1/24 link).

```
Metric = 256 x (10 ^ 7 / 1000000 + 30 / 10) = 3328
```

- If you are unsure of the EIGRP metrics, you can query the parameters from the formula directly from the EIGRP topology table, by using the command `show ip eigrp topology <prefix/length>`

- Below is shown R1's topology table output for the 10.4.4.0/24 network

- Notice that the output includes the successor route, any feasible successor paths, and the EIGRP state for the prefix

- Each path contains the EIGRP attributes minimum bandwidth, total delay, interface reliability, load and hop count

```
R3#show ip eigrp topology 10.12.1.0/24
EIGRP-IPv4 VR(EIGRP-NAMED) Topology Entry for AS(100)/ID(192.168.3.3) for 10.12.1.0/24
  State is Passive, Query origin flag is 1, 2 Successor(s), FD is 196608000, RIB is 1536000
  Descriptor Blocks:
  10.13.1.1 (Ethernet0/0), from 10.13.1.1, Send flag is 0x0
      Composite metric is (196608000/131072000), route is Internal
      Vector metric:
        Minimum bandwidth is 10000 Kbit
        Total delay is 2000000000 picoseconds
        Reliability is 255/255
        Load is 1/255
        Minimum MTU is 1500
        Hop count is 1
        Originating router is 192.168.1.1
  10.22.22.2 (Ethernet0/1), from 10.22.22.2, Send flag is 0x0
      Composite metric is (196608000/131072000), route is Internal
      Vector metric:
        Minimum bandwidth is 10000 Kbit
        Total delay is 2000000000 picoseconds
        Reliability is 255/255
        Load is 1/255
        Minimum MTU is 1500
        Hop count is 1
        Originating router is 192.168.2.2
```

#### Wide Metrics

- The original EIGRP specification measured delay in 10-microsecond delay (us) units and bandwidth in kilobites per second, which did not scale very well with higher speed interfaces

- In the below table, notice that the delay is the same for the GigabitEthernet and TenGigabitEthernet interfaces

- Below is provided some metric calculations for common LAN interface speeds

- Notice that there is not a differenciation between an 11 Gbps interface and a 20 Gbps interface

- The composite metric stays at 256, despite the different bandwidth rates

```
GigabitEthernet:

Scaled Bandwidth =  10 000 000 / 1 000 000

Scaled Delay = 10 / 10

Composite metric = 10 + 1 * 256 = 2816

---

10 GigabitEthernet:

Scaled Bandwidth = 10 000 000 / 10 000 000

Scaled Delay = 10 / 10

Composite Metric = 1 + 1 * 256 = 512

---

11 GigabitEthernet:

Scaled Bandwidth = 10 000 000 / 11 000 000

Scaled Delay = 10 / 10

Composite Metric = 0 + 1 * 256 = 256

---

20 GigabitEthernet:

Scaled Bandwidth = 10 000 000 / 20 000 000

Scaled Delay = 10 / 10

Composite Metric = 0 + 1 * 256 = 256
```

- EIGRP includes support for a second set of metrics, known as wide metrics, that addresses the issue of scalability with higher-capacity interfaces

- Just as EIGRP scaled by 256 to accomodate IGRP, EIGRP wide metrics scale by 65536 to accomodate higher speed links

- This provides support for interface speeds up to 655 Tbps (65536 * 10 ^ 7) without any scalability issues

- Below is shown the explicit EIGRP wide metrics formula

- Notice that an additional K value (K6) is included that adds an extended attribute to measure jitter, energy, or other future attributes

```
Wide metric = 65536 * [ (K1 * BW) + (K2 * BW) / (256 - load) + (K3 * latency) + (K6 * extended)] * K5 / (K4 + Reliability)
```

![eigrp-wide-metrics-formula](./eigrp-wide-metrics-formula.png)

- Latency is the total interface delay measured in picoseconds (10 ^ 12) in place of 10 ^ 6

- Below is shown an updated formula that takes into account the conversions in latency and scalability

```
Wide metric = 65536 * [ (K1 * 10 ^ 7) / min_bandwidth + ((K2 * 10 ^ 7) / min_bandwidth) / 256 - load + (K3 * Latency) / 10 ^ 6 + (K6 * Extended)] * K5 / (K4 + reliability)
```

![wide-metric-calculation1](./wide-metric-calculation1.png)

- The interface delay varies from router to router, depending on the following logic:

    - If the interface's delay was specifically set, the value is converted to picoseconds. Interface delay is always configured in tens of microseconds and is multiplied by 10 ^ 7 for picosecond conversion

    - If the interface's bandwidth was specifically set, the interface delay is configured using the classic default delay, converted to picoseconds. The configured bandwidth is not considered when determining the interface delay. If the delay is configured this step is ignored

    - If the interface supports speeds of 1 Gbps or less and does not contain bandwidth or delay configuration, the delay is the classic default delay, converted to picoseconds

    - If the interface supports speeds over 1 Gbps and does not contain bandwidth and delay configuration, the interface delay is calculated by 10 ^ 13 / interface bandwidth

- The EIGRP classic metric exist only with EIGRP classic configuration, and EIGRP wide metrics exist only in EIGRP named mode

- The metric style used by a router is identified with the command `show ip protocols`. If a K6 metric is present, the router is using wide-style metrics

- R1:

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

Routing Protocol is "eigrp 100"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Default networks flagged in outgoing updates
  Default networks accepted from incoming updates
  Redistributing: rip
  EIGRP-IPv4 Protocol for AS(100)
    Metric weight K1=1, K2=0, K3=1, K4=0, K5=0
    Soft SIA disabled
    NSF-aware route hold timer is 240
    Router-ID: 192.168.1.1
    Topology : 0 (base) 
      Active Timer: 3 min
      Distance: internal 90 external 170
      Maximum path: 4
      Maximum hopcount 100
      Maximum metric variance 1

  Automatic Summarization: disabled
  Maximum path: 4
  Routing for Networks:
    10.11.11.1/32
    10.12.1.1/32
    10.13.1.1/32
    10.112.1.0/24
    192.168.1.1/32
  Passive Interface(s):
    GigabitEthernet0/2
    Loopback0
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.13.1.3             90      01:32:16
    10.12.1.2             90      01:32:16
  Distance: internal 90 external 170

```

- R2:

```
R2(config-router-af)#do sh ip proto
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

Routing Protocol is "eigrp 100"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Default networks flagged in outgoing updates
  Default networks accepted from incoming updates
  EIGRP-IPv4 VR(EIGRP-NAMED) Address-Family Protocol for AS(100)
    Metric weight K1=1, K2=0, K3=1, K4=0, K5=0 K6=0
    Metric rib-scale 128
    Metric version 64bit
    Soft SIA disabled
    NSF-aware route hold timer is 240
    Router-ID: 192.168.2.2
    Topology : 0 (base) 
      Active Timer: 3 min
      Distance: internal 90 external 170
      Maximum path: 4
      Maximum hopcount 100
      Maximum metric variance 1
      Total Prefix Count: 9
      Total Redist Count: 0

  Automatic Summarization: disabled
  Maximum path: 4
  Routing for Networks:
    0.0.0.0
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.12.1.1             90      00:00:21
    10.22.22.3            90      00:00:21
  Distance: internal 90 external 170

```

- Above we can see that R1 does not have a K6 metric and is using EIGRP classic metrics

- R2 has a K6 metric and is using EIGRP wide metrics

#### Metric Backward Compatibility

- EIGRP wide metrics were designed with backward compatibility in mind

- EIGRP wide metrics set K1 and K3 to a value of 1 and set K2, K4, K5, K6 to 0, which allows backward compatibility because the K value metrics match with classic metrics

- As long as K1 through K5 are the same and K6 is not set, the two metric styles allow adjacency between routers

- EIGRP is able to detect when peering with a router is using classic metrics, and it unscales the metric by using the formula below

```
Unscaled bandwidth = (EIGRP bandwidth + EIGRP classic scale) / Scaled bandwidth
```

- This conversion results in loss of clarity if routes pass through a mixture of classic metric and wide metric devices

- An end result of this intended behavior is that paths learned from wide metric peers always look better than paths learned from classic peers

- Using a mixture of classic metric and wide metric devices could lead to suboptimal routing, so it's best to keep all devices operating with the same metric style

#### Interface Delay Settings

- 