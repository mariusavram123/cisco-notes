## OSPF

1. OSPF Fundamentals

2. OSPF Configuration

3. Default Route Advertisement

4. Common OSPF Optimizations

- OSPF is a nonproprietary Interior Gateway Protocol (IGP) that overcomes the deficiencies of other distance vector routing protocols and distributing routing information within a single OSPF routing domain

- OSPF introduces the concept of variable-length subnet masking (VLSM), which supports classless routing, summarization, authentication, and external route tagging

- There are two main versions of OSPF in production networks today:

    - **OSPF Version 2 (OSPF V2)**: Defined in RFC 2328 and supports IPv4

    - **OSPF Version 3 (OSPF V3)**: Defined in RFC 5340 and modifies the original structure to support IPv6

- **Advanced OSPF**: Explain the function of segmenting the OSPF domain into smaller areas to support larger topologies

- **OSPF V3**: Explains how OSPF can be used for routing IPv6 packets

### OSPF Fundamentals

- OSPF sends to neighboring routers link-state advertisements (LSAs) that contains the link state and link metric

- The received LSAs are stored in a local database called the link-state database (LSDB), and they are flooded throughout the OSPF routing domain just as the advertising router advertised them

- All OSPF routers maintain a synchronized identical copy of the LSDB for the same area

- The LSDB provides the topology of the network, in essence providing for the router a complete map of the network

- All OSPF routers run the Dijikstra shortest path first (SPF) algorithm to construct a loop free topology of shortest paths

- OSPF dynamically detects topology changes within the network and calculates loop-free paths in a short amount of time with minimal routing protocol traffic

- Each router sees itself as the root or top of the SPF tree (SPT), and the SPT contains all network destinations within the OSPF domain

- The SPT differs for each OSPF router, but the LSDB used to calculate the SPT is identical for all OSPF routers

![SPT-calculation](./ospf-spt-calculation.png)

- The above scheme shows a simple OSPF topology and the SPT from R1 and R4's perspective

- Notice that the local router's perspective will always be the root (top of the tree)

- There is a difference in connectivity to the 10.3.3.0/24 network from R1's SPT and R4's SPT

- From R1's perspective, the serial link between R3 and R4 is missing; from R4's perspective, the Ethernet link between R1 and R3 is missing

- The SPTs give the illusion that no redundancy exists in the networks, but remember that the SPT shows the shortest path to reach a network and is built from the LSDB, which contains all the links for an area

- During a topology change, the SPT is rebuilt and may change

- OSPF provides scalability for the routing table by using multiple OSPF areas within the routing domain

- Each OSPF area provides a collection of connected networks and hosts that are grouped together

- OSPF uses a two-tier hierarchical architecturem where Area 0 is a special area known as the backbone, to which all other areas must connect

- In other words, Area 0 provides transit connectivity between nonbackbone areas

- Nonbackbone areas advertise routes into the backbone and the backbone then advertises routes into other non-backbone areas

![multiarea-advertisement](./ospf-multiarea-routes.png)

- The above scheme shows the route advertisement into other areas. Area 12 routes are advertised into Area 0 and then into Area 34

- Area 34 routes are advertised to Area 0 and then into Area 12

- Area 0 routes are advertised to all other OSPF areas

- The exact topology of the area is invisible from outside the area while still providing connectivity of routers outside the area

- This means that routers outside the area do not have a complete topological map of the area, which reduces OSPF traffic in that area

- When you segment an OSPF routing domain into multiple areas, it is no longer true that all OSPF routers will have identical LSDBs; however all routers within the same area will have will have identical area LSDBs

- The reduction in routing traffic uses less router memory and resources and therefore provides scalability

- This will be explained in detail later on. For now we will focus on core OSPF concepts. Area 0 is used as a reference area

- A router can run multiple OSPF processes. Each process maintains it's own unique database, and routes learned in one OSPF process are not available to a different OSPF process without redistribution of routes between processes

- The OSPF process numbers are locally significant and do not have to match among routers

- Running OSPF process number 1 in one router and running OSPF process number 1234 on the second router will still allow the two routers to become neighbors

#### Inter-Router Communication

- OSPF runs directly over IPv4, using it's own protocol 89, which is reserved for OSPF by the Internet Assigned Numbers Authority (IANA)

- OSPF uses multicast where possible to reduce unnecessary traffic 

- The two OSPF multicast addresses are as follows:

    - **AllSPFRouters**: IPv4 address 224.0.0.5 or MAC address 01:00:5e:00:00:05. All routers running OSPF should be able to receive these packets

    - **AllDRouters**: IPv4 address 224:0.0.6 or MAC address 01:00:5e:00:00:06. Communication with Designated Routers (DRs) uses this address

- Within the OSPF protocol, five types of packets are communicated:

    1. **Hello**: These packets are for discovering and maintaining neighbors. Packets are sent out periodically on all OSPF interfaces to discover new neighbors while ensuring that other adjacent neighbors are still online

    2. **Database Description (DBD or DDP)**: These packets are for summarizing database contents. Packets are exchanged when an OSPF adjacency is first being formed. These packets are used to discribe the contents of the LSDB

    3. **Link-state request (LSR)**: These packets are for database downloads. When a router thinks that part of LSDB is stale, it may request a portion of neighbor's database by using this packet type

    4. **Link-state update (LSU)**: These packets are for database updates. This is an explicit LSA for a specific network link and normally is sent in direct response to LSR

    5. **Link-state ack (LSAck)**: These packets are for flooding acknowledgements. These packets are sent in response to the flooding of LSAs, thus making flooding a reliable transport feature

#### OSPF Hello Packets

- OSPF hello packets are responsible for discovering and maintaining neighbors. In most instances, a router sends Hello packets to AllSPFRouters address (224.0.0.5) 

- Below is the list with the data present in an OSPF Hello packet:

    - **Router ID**: A unique 32-bit ID within an OSPF domain

    - **Authentication options**: A field that allows secure communication between OSPF routers to prevent malicious activity. Options are none, plain text, or Message Digest 5 (MD5) authentication

    - **Area ID**: The OSPF area that the OSPF interface belongs to. It is a 32-bit number that can be written in dotted-decimal format (0.0.1.0) or decimal(256)

    - **Interface address mask**: The network mask for the primary IP address for the interface out which the hello is sent

    - **Interface Priority**: The router interface priority for DR elections

    - **Hello Interval**: The time span, in seconds, that a router sends out hello packets on the interface

    - **Dead Interval**: The time span, in seconds, that a router waits to hear a hello from the neighbor router before it declares that router down

    - **Designated Router and Backup Designated Router**: The IP address of the DR and backup DR (BDR) for the network link

    - **Active neighbor**: A list of OSPF neighbors seen on the network segment. A router must have received a hello from the neighbor within the dead interval

##### Router ID

- The OSPF Router ID (RID) is a 32-bit number that uniquely identifies an OSPF router

- In some OSPF output commands, *neighbor ID* refers to the RID; the terms are synonymous

- The RID must be unique for each OSPF process in an OSPF domain and must be unique between OSPF processes on a router

##### Neighbors

- An OSPF neighbor is a router that shares a common OSPF-enabled network link

- OSPF routers discover other neighbors via the OSPF hello packets

- An adjacent OSPF neighbor is an OSPF neighbor that shares a synchronized OSPF database between the two neighbors

- Each OSPF process maintains a table for adjacent OSPF neighbors and the state of each router

- OSPF neighbor states:

    - **Down**: This is the initial state of the neighbor relationship. It indicates that the router has not received any OSPF hello packets

    - **Attempt**: This state is relevant to NBMA (non broadcast multi access) networks that do not support broadcast and require explicit neighbor configuration. This state indicates that no information has been received recently, but the router is still attempting communication

    - **Init**: This state indicates that a hello packet has been received from another router, but bidirectional communication has not been established

    - **2-Way**: Bidirectional communication has been established. If a DR and BDR is needed, the election occurs during this state

    - **ExStart**: This is the first state in forming an adjacency. Routers identify which router will be the master or slave for LSDB synchronization

    - **Exchange**: During this state, routers are exchanging link states by using DBD packets

    - **Loading**: LSR packets are sent to the neighbor, asking for the more recent LSAs that have been discovered (but not received) in the Exchange state

    - **Full**: Neighboring routers are fully adjacent

##### Designated Router and Backup Designated Router

- Multi-access networks such as Ethernet (LANs) and Frame Relay allow more than 2 routers to exist on a network segment

