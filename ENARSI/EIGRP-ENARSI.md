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

