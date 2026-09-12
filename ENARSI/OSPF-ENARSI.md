## OSPF

1. OSPF Fundamentals

2. OSPF Configuration

3. The Designated Router and Backup Designated Router

4. OSPF Network Types

5. Failure Detection

6. Authentication

- The Open Shortest Path First (OSPF) protocol is a link-state routing protocol

- OSPF is a nonproprietary Interior Gateway Protocol (IGP) that overcomes the deficiencies of other distance vector routing protocols

- It distributes routing information within a single OSPF routing domain

- OSPF introduced the concept of variable-length subnet masking (VLSM), which supports classless routing, summarization, authentication, and external route tagging

- There are two main versions of OSPF in production networks today:

    - **OSPFv2**: Originally defined in RFC 2328 with IPv4 support

    - **OSPFv3**: Modifies the original structure to support IPv6

- The core concepts of OSPF and the basics of establishing neighborships and exchanging routes with other OSPF routers

- The fundamentals of OSPF and common optimizations in networks of any size

### OSPF Fundamentals

- OSPF sends Link State Advertisements (LSAs) to neighboring routers

- An LSA contains information on the link state and link metric, and OSPF advertises this information to neighboring routers exactly as the original advertising router advertises it

- Received LSAs are stored in a local database called the link-state database (LSDB)

- This process floods the LSA throughout the OSPF routing domain just as the neighboring router advertised it

- All OSPF routers maintain a synchronized identical copy of the LSDB within an area

- The LSDB provides the topology of the network, in essence providing the router the complete map of the network

- All OSPF routers run Dijkstra's shortest path first (SPF) algorithm to construct a loop-free topology of shortest paths

- OSPF dynamically detects topology changes within the network and calculates loop-free paths in a short amount of time with minimal routing protocol traffic

- Each router sees itself as the root or top of the SPF tree (SPT) and SPT contains all network destinations within the OSPF domain

- The SPT differs for each OSPF router, but the LSDB used to calculate the SPT is identical for all OSPF routers

- Below is an example of a simple OSPF topology and the SPT from R1's and R4's perspective

- Notice that the local router's perspective is always that of the root (or top of the tree)

- There is a difference in connectivity to the 10.3.3.0/24 network from R1's and R4's SPT's

- From R1's perspective, the serial link between R3 and R4 is missing; from R4's perspective, the ethernet link between R1 and R3 is missing

- The SPT's give the illusion that no redundancy exists to the networks, but remember that an SPT shows the shortest path to reach a network and is built from the LSDB, which contains all the links from an area

- During a topology change, the SPT is rebuilt and may change

![OSPF-SPT-calculation](./OSPF-SPT-calculation.png)

- A router can run multiple OSPF processes

- Each process maintains it's own unique database, and routes learned in one OSPF process are not available to a different OSPF process without redistribution of routes between processes

- The OSPF process numbers are locally significant and do not have to match among routers

- If OSPF process number 1 is running on one router and OSPF process number 1234 is running on another, the two routers can become neighbors

#### Areas

- OSPF provides scalability for the routing table by splitting segments of the topology into multiple OSPF areas within the routing domain

- An OSPF area is a logical grouping of routers or, more specifically, a logical grouping of router interfaces

- Area membership is set at the interface level, and the area ID is included in the OSPF hello packet

- An interface can belong to only one area

- All routers within the same OSPF area maintain an identical copy of the LSDB

- An OSPF area grows in size as the number of network links and the number of routers increase in the area

- While using a single area simplifies the topology, there are trade-offs:

    - A full SPT calculation run when a link flap within the area

    - With a single area, the LSDB increases in size and becomes unmanageable

    - The LSDB for the single area grows, consumes more memory, and takes longer during the SPF computation process

    - With a single area, no summarization of route information occurs

- Proper design addresses each of these issues by segmenting the OSPF routing domain into multiple OSPF areas, thereby keeping the LSDB a manageable size

- Sizing and design of OSPF networks should account for the hardware constraints of the smallest router in that area

- If a router has interfaces in multiple areas, the router has multiple LSDBs (one for each area)

- The internal topology of one area is invisible from outside that area

- If a topology change occurs (such as a link flap or an additional network added) within an area, all routers in the same OSPF area calculate the SPT again

- Routers outside that area do not calculate the full SPT again but do perform partial SPT calculation if the metrics have changed or a prefix is removed

- In essence, an OSPF area hides the the topology from another area but allows the networks to be visible in other areas within the OSPF domain

- Segmenting the OSPF domain into multiple areas reduce the size of the LSDB for each area, making SPT calculations faster and decreasing LSDB flooding between routers when a link flaps

- Just because a router connects to multiple OSPF areas does not mean that routes from one area will be injected into another area

- Below is shown router R1 connected to Area 1 and Area 2. Routes from Area 1 do not advertise into Area 2 and vice versa

![failed-route-advertisement-areas](./failed-route-advertisement-areas.png)

- Area 0 is a special area called *the backbone* or *backbone area*

- By design, OSPF uses a two-tier hierarchy in which all areas must connect to the upper tier, Area 0, because OSPF expects all areas to inject routing information into Area 0

- Area 0 advertises the routes into other nonbackbone areas

- The backbone is crucial to preventing routing loops

- The area identifier (also known as the area ID) is a 32-bit field that can be formatted in simple decimal (0 through 4294967295) or dotted decimal (0.0.0.0 through 255.255.255.255)

- When configuring routers in an area, even if you use decimal format on one router and dotted-decimal format on a different router, the routers will be able to form an adjacency

- OSPF advertises the area ID in OSPF packets

- *Area Border Routers (ABRs)* are OSPF routers connected to Area 0 and another OSPF area as per Cisco definition and according to RFC 3509

- ABRs are responsible for advertising routes from one area and injecting them into a different OSPF area

- Every ABR needs to participate in Area 0 to allow for the advertisement of routes into another area

- ABRs compute an SPT for every area they participate in

- Below is shown that R1 is connected to Area 0, Area 1 and Area 2

- R1 is a proper ABR router because it participates in Area 0

- The following occurs on R1:

    - Routes from Area 1 advertise into Area 0

    - Routes from Area 2 advertise into Area 0

    - Routes from Area 0 advertise into Areas 1 and 2. This includes the local Area 0 routes, in addition to the routes that were advertised into Area 0 from Area 1 and Area 2

![ospf-success-router-advetisement-multiple-areas](./ospf-success-router-advetisement-multiple-areas.png)

#### Inter-Router Communication

- OSPF runs directly over IPv4, using protocol 89 in the IP header, which the Internet Assigned Numbers Authority (IANA) reserves for OSPF

- OSPF uses multicast where possible to reduce unnecessary traffic

- There are 2 OSPF multicast addresses:
