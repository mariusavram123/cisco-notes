## Advanced OSPF

1. Areas

2. Link-state Announcements (Advertisements)

3. Discontiguous Networks

4. OSPF Path Selection

5. Summarization of Routes

6. Route Filtering

- The Open Shortest Path First (OSPF) protocol scales well with proper network planning

- IP addressing schemes, area segmentation, address summarization and hardware capabilities for each area should all be taken into consideration for a network design

- OSPF in large networks and multi-area OSPF domain, path selection and techniques to optimize the OSPF environment

### Areas

- An OSPF area is a logical grouping of routers or, more specifically, a logical grouping of router interfaces

- Area membership is set at the interface level, and the area ID is included in the OSPF hello packet

- An interface can belong to only one area. All routers within the same OSPF area maintain an identical copy of the link-state database (LSDB)

- An OSPF area grows in size as network links and the number of links increase in the area

- While using a single area simplifies the topology, there are trade-offs:

	- Full shortest path first (SPF) tree calculation runs when a link flaps within the area

	- The LSDB increases the size and becomes unmanageable

	- The LSDB for the are grows, consuming more memory, and taking longer during the SPF computation process

	- No summarization of route information occurs

- Proper design addresses each of these issues by segmenting the routers into multiple OSPF areas, thereby keeping the LSDB to a manageable size

- Sizing and design of OSPF networks should account for the hardware constraints of the smallest router in that area

- If a router has interfaces in multiple areas, the router has multiple LSDBs (one for each area)

- The internal topology of one area is invisible from outside that area

- If a topology change occurs (such as a link flap or an additional network being added) within an area, all routers in the same OSPF area calculate the SPF tree again

- Routers outside that area do not calculate the full SPF tree again but perform a partial SPF calculation if the metric have changed or a prefix is removed

- In essence an OSPF area hides the topology from another area but enables the networks to be visible in other areas within the OSPF domain

- Segmenting the OSPF domain into multiple areas reduces the size of the LSDB for each area, making SPF tree calculations faster, and decreasing LSDB flooding between routers when a link flaps

- Just because a router connects to multiple OSPF areas does not mean the routes from one area will be injected into another area

![topology](./ospf-routes-no-backbone.png)

- In the above topology R1 is connected to Area 1 and Area 2. Routes from Area 1 will not advertise into Area 2 and viceversa

- Area 0 is a special area called *the backbone*

- By design, all areas must connect to Area 0 because OSPF expects all areas to inject routing information into the backbone, and Area 0 advertises the routes into other areas

- The backbone design is crucial to preventing routing loops

- *Area Border Routers (ABRs)* are OSPF routers connected to Area 0 and another OSPF area, per Cisco definition and according to RFC 3509

- Every ABR needs to participate in Area 0; otherwise, routes will not advertise into another area

- ABRs compute an SPF tree for every area that they participate in

![topology](./ospf-multiarea-routes2.png)

- In the above topology R1 is connected to Area 0, Area 1 and Area 2

- R1 is a proper ABR because it now participates in Area 0

- The following occurs on R1:

	- Routes from Area 1 advertise into Area 0

	- Routes from Area 2 advertise into Area 0

	- Routes from Area 0 advertise into Area 1 and 2. This includes the local Area 0 routes, in addition to routes that were advertised into Area 0 from Area 1 and Area 2

![topology](./large-scale-multiarea-ospf.png)

- In the above large scale topology:

	- R1, R2, R3 and R4 belong to Area 1234

	- R4 and R5 belong to Area 0

	- R5 and R6 belong to Area 56

	- R4 and R5 are ABRs

	- Area 1234 connects to Area 0, and Area 56 connects to Area 0

	- Routers in Area 1234 can see routes from routers in Area 0, Area 56 and vice versa

- OSPF configuration for ABRs R4 and R5

- Notice that multiple interfaces in the configuration have Area 0 as one of the areas:

- R4:

```
conf t
 router ospf 1
  router-id 192.168.4.4
  network 10.24.1.0 0.0.0.255 area 1234
  network 10.45.1.0 0.0.0.255 area 0
```

- R5:

```
conf t
 router ospf 1
  router-id 192.168.5.5
  network 10.45.1.0 0.0.0.255 area 0
  network 10.56.1.0 0.0.0.255 area 56
```

- Verifying that interfaces on R4 belong to Area 1234 and Area 0, and that interfaces on R5 belong to Area 0 and Area 56

- R4:

```
show ip ospf interface brief

Interface		PID		Area		IP Address/Mask		Cost	State		Nbrs f/c
Gi0/0			1		0			10.45.1.4/24		1		DR			1/1
Se1/0			1		1234		10.24.1.4/29		64		P2P			1/1
```

- R5

```
show ip ospf interface brief

Interface		PID		Area		IP Address/Mask		Cost	State		Nbrs f/c
Gi0/0			1		0			10.45.1.5/24		1		DR			1/1
Gi0/1			1		1234		10.56.1.5/29		1		BDR			1/1
```

#### Area ID

- The Area ID is a 32-bit field and can be formatted in simple decimal (0 through 4,294,976,295) or dotted decimal (0.0.0.0 through 255.255.255.255)

- During router configuration, the area can use decimal format on one router and and dotted-decimal format on a different router, and the routers can still form an adjacency

- OSPF advertises the area ID in dotted-decimal format in the OSPF hello packet

#### OSPF Route Types

- Network routes that are learned from other OSPF routers within the same area are known as *intra-area routes*

- In our topology, the network link between R2 and R4 (10.24.1.0/29) is an intra-area route for R1

- The IP routing table displays OSPF intra-area routes with an O

- Network routes that are learned from other OSPF routers from different area using an ABR are known as *interarea routes*

- On our topology, the network link between R4 and R5 (10.45.1.0/24) is an interarea route to R1

- The IP routing table displays OSPF interarea routes with *O IA*

- Routing table for R1 from our topology. Notice that R1's OSPF routing table shows routes from within Area 1234 as intra-area routes (O routes) and routes from Area 0 and Area 56 as interarea (O IA routes)

- R1:

```
show ip route

(...)
O		10.3.3.0/24 [110/20] via 10.123.1.3, 00:12:07, GigabitEthernet0/0
O		10.24.1.0/29 [110/74] via 10.123.1.2, 00:12:07, GigabitEthernet0/0
(...)
O IA	10.45.1.0/24 [110/84] via 10.123.1.2, 00:12:07, GigabitEthernet0/0
O IA	10.56.1.0/24 [110/94] via 10.123.1.2, 00:12:07, GigabitEthernet0/0
```

- Routing table of R4 from our topology. Notice that R4's routing table shows the routes from within Area 1234 and Area 0 as intra-area routes and routes from Area 56 as interarea because R4 does not connect to Area 56

- Notice that the metric for the 10.123.1.0/24 and 10.3.3.0/24 networks has drastically increased compared to the metric for the 10.56.1.0/24 network. This is because it must cross the slow serial link, which has an interface cost of 64

- R4:

```
show ip route

(...)
O		10.3.3.0/24 [110/66] via 10.24.1.2, 00:03:45, Serial1/0
(...)
O IA	10.56.1.0/24 [110/2] via 10.45.1.5, 00:04:56, GigabitEthernet0/0
O		10.123.1.0/24 [110/65] via 10.24.1.2, 00:13:19, Serial 1/0 	

(...)
```

- Routing tables for R5 and R6. R5 and R6 only contain interarea routes because intra-area routes are directly connected

- R5:

```
show ip route ospf

O IA     10.3.3.0/24 [110/67] via 10.45.1.4, 01:08:01, GigabitEthernet0/0
O IA     10.24.1.0/29 [110/65] via 10.45.1.4, 01:11:55, GigabitEthernet0/0
O IA     10.123.1.0/24 [110/66] via 10.45.1.4, 01:08:06, GigabitEthernet0/0
```

- R6:

```
show ip route ospf

O IA     10.3.3.0/24 [110/68] via 10.56.1.5, 01:09:54, Ethernet0/0
O IA     10.24.1.0/29 [110/66] via 10.56.1.5, 01:13:48, Ethernet0/0
O IA     10.45.1.0/24 [110/2] via 10.56.1.5, 01:13:57, Ethernet0/0
O IA     10.123.1.0/24 [110/67] via 10.56.1.5, 01:09:59, Ethernet0/0
```

- External routes are routes learned from outside of the OSPF domain but injected into an OSPF domain through redistribution

- External OSPF routes can come from a different OSPF domain or from a different routing protocol

### Link-State Announcements

- When OSPF neighbors become adjacent, the LSDBs synchronize between the OSPF routers

- As an OSPF router adds or removes a directly connected network link to or from it's database, the router floods the link state advertisement (LSA) out all active OSPF interfaces

- OSPF LSA contains a complete list of networks advertised from that router

- OSPF uses six LSA types for IPv4 routing:

	- **Type 1, router LSA**: Advertises the LSAs that originate within an area

	- **Type 2, network LSA**: Advertises a multi-access network segment attached to a DR

	- **Type 3, summary LSA**: Advertises network prefixes that originated from a different area

	- **Type 4, ASBR summary LSA**: Advertises a summary LSA for a specific ASBR

	- **Type 5, AS external LSA**: Advertises LSAs for routes that have been redistributed

	- **Type 7, NSSA external LSA**: Advertises redistributed routes in NSSAs

- LSA types 1, 2 and 3 are used for building the SPF tree from interarea and intra-area routes

![ospf-lsa-packet](./ospf-router-lsa-capture.png)

- The above packet capture shows an OSPF update LSA and outlines the important components of the LSA: the LSA type, LSA age, sequence number, and advertising router

- Because this is a type 1 LSA, the link IDs add relevance as they list the attached network and the associated OSPF cost for each interface

#### LSA Sequences

- OSPF uses the sequence number to overcome problems caused by delays in LSA propagation in a network

- The LSA sequence number is a 32-bit number for controlling versioning

- When the originating router sends out LSAs, the LSA sequence number is incremented 

- If a router receives an LSA sequence that is greater than the one in the LSDB, it processes the LSA

- If the LSA sequence number is lower than the one in the LSDB, the router deems the LSA old and discards the LSA

#### LSA Age and Flooding

- Every OSPF LSA includes an age that is entered into the local LSDB and that will increment by 1 every second

- When a router's OSPF LSA age exceeds 1800 seconds (30 minutes) for it's networks, the originating router advertises a new LSA with the LSA age set to 0

- As each router forwards the LSA, the LSA age is incremented with a calculated (minimal) delay that reflects the link

- If the LSA age reaches 3600, the LSA is deemed invalid and is purged from the LSDB

- The repetitive flooding of LSAs is a secondary safety mechanism to ensure all routers maintain a consistent LSDB within an area

#### LSA Types

- All routers within an OSPF area have an identical set of LSAs for that area

- The ABRs maintains a separate set of LSAs for each OSPF area

- Most LSAs in one area will be different from the LSAs in another area

- Displaying the generic router LSA output:

```
show ip ospf database
```

##### LSA Type 1: Router Link

- Every OSPF router advertises a type 1 LSA

- Type 1 LSAs are the essential building blocks within the LSDB

- A type 1 LSA entry exists for each OSPF-enabled link (that is every interface and it's attached networks)

- Refering to our topology we can see that the type 1 LSAs are not advertised outside Area 1234, which means the underlying topology in an area is invisible to other areas

- Displaying the type 1 LSAs for an area:

```
show ip ospf database router
```

![topology](./type-1-lsa-flooding-topology.png)

- The initial fields of each type 1 LSA indicate the RID for the LSA's advertising router, age, sequence, link count and link ID

- Each OSPF-enabled interface is listed under the number of links for each router

- Each network link on a router contains the link type, correlating information for neighbor router identification, and interface metric

- The correlating information for neighbor router identification is often the neighbor RID, with the exception of multi-access network segments that contain designated routers (DRs)

- In those scenarios, the interface address of the DR identifies the neighbor router

- If we correlate just type 1 LSAs from our sample topology, then the topology build by all routers in Area 1234 using the LSA attributes for Area 1234 from all four routers will be the following:

![lsa-type1](./lsa-type1-topology-area1234.png)

##### LSA Type 2: Network Link

- The type 2 LSA represents a multi-access network segment that used a DR

- The DR always advertises the type 2 LSA and identifies all the routers attached to that network segment

- If a DR has not been elected, a type 2 LSA is not present in the LSDB because the corresponding type 1 transit link type 1 LSA is a stub

- Like type 1 LSAs, Type 2 LSAs are not flooded outside the originating OSPF area

- Area 1234 has only one DR segment that connects to R1, R2 and R3 because R3 has not formed an OSPF adjacency on the 10.3.3.0/24 segment

- On the 10.123.1.0/24 network segment, R3 is elected as the DR, and R2 is elected as the BDR because of the order of the RIDs

- Showing detailed type 2 LSA information:

```
show ip ospf datablase network
```

- Now that we have the type 2 LSA for Area 1234, all the network links are connected

- Visualization of the type 1 and type 2 LSAs, which corresponds with Area 1234:

![type-1-type2](./type-1-type-2-lsa.png)

- When the DR changes for a network segment, a new type 2 LSA is created, causing SPF to run again within the OSPF area


##### LSA Type 3: Summary Link

- Type 3 LSAs represent networks from other areas

- The role of the ABRs is to participate in multiple OSPF areas and ensure the networks associated with type 1 LSAs are are reachable in the non-originating OSPF areas

- ABRs do not forward type 1 and type 2 LSAs into other areas

- When an ABR receive a type 1 LSA, it creates a type 3 LSA referencing the network in the original type 1 LSA; the type 2 LSA is used to determine the network mask of the multi-access network

- The ABR then advertises the type 3 LSA into other areas

- If an ABR receives a type 3 LSA from Area 0 (the backbone), it regenerates a new type 3 LSA for the nonbackbone area and lists itself as the advertising router, with the additional cost metric

- Type 3 LSA interaction with type 1 LSAs is shown below

![lsa-type1-type3](./lsa-type1-type3-interaction.png)

- The type 3 LSAs show up under the appropriate areas where they exists in the OSPF domain

- For example, the 10.56.1.0 Type 3 LSA is in Area 0 and Area 1234 on R4; however, on R5 the type 3 LSA exists only on Area 0 because the 10.56.1.0 network is a type 1 LSA in Area 56

- Showing the type 3 LSA information:

```
show ip ospf database summary
```

- The output can be restricted to a specific LSA by appending the network prefix to the end of the command

```
show ip ospf database summary 10.3.3.0
```

- View the IP summary for a prefix and for a specific advertising router

```
show ip ospf database summary 10.3.3.0 adv-router 192.168.4.4
```

- The advertising router for the type 3 LSAs is the last ABR that advertises the prefix. The metric within the type 3 LSA uses the following logic:

	- If the type 3 LSA is created from a type 1 LSA, it is the total path metric to reach the originating router in the type 1 LSA

	- If the type 3 LSA is created from a type 3 LSA from Area 0, it is the total path metric to the ABR plus the metric in the original type 3 LSA

- When R2 advertises the 10.123.1.0/24 network the following happens:

	- R4 receive R2's type 1 LSA and creates a new type 3 LSA by using the metric 65: The cost of 1 of R2's LAN interface and 64 for the serial link between R2 and R4

	- R4 advertises the type 3 LSA with the metric 65 into Area 0

	- R5 receive the type 3 LSA and creates a new type 3 LSA for Area 56, using the metric 66: The cost of 1 for the link between R4 and R5 plus the original LSA type 3 metric 65

	- R6 receives the type 3 LSA. Part of R6's calculation is the metric to reach the ABR (R5), which is 1 plus the metric in the type 3 LSA (66). R6 therefore calculates the metric 67 to reach 10.123.1.0/24

- The type 3 LSA contains the link-state ID (network number), the subnet mask, the IP address of the advertising ABR, and the metric for the network prefix

- R4 does not know if the 10.56.1.0/24 network is directly attached to the ABR (R5) or multiple hops away

- R4 knows that it's metric to the ABR (R5) is 1 and that the type 3 LSA already has a metric of 1, so it's total path metric to reach the 10.56.1.0/24 network is 2

- R4's perspective of the type 3 LSA created by ABR (R5) for the 10.56.1.0/24 network

![topology](./type-3-lsa-r4-perspective.png)

- R3's perspective of the type 3 LSA created by ABR (R4) for the 10.56.1.0/24 network

![topology](./r3-type3-lsa-view.png)

- R3 does not know if the 10.56.1.0/24 network is directly attached to the ABR (R4) or multiple hops away

- R3 knows that it's metric to reach the ABR (R4) is 65 and that the type 3 LSA already has a metric of 2, so it's total path metric to reach the 10.56.1.0/24 network is 67

- An ABR advertises only one type 3 LSA for a prefix, even if it is aware of multiple paths from within it's area (type 1 LSAs) or from outside it's area (type 3 LSAs)

- The metric for the best path will be used when the LSA is advertised into a different area

### Discontiguous Networks

- Network engineers that do not fully understand OSPF design may create a topology such as the following:

![topology](./discontiguous-areas.png)

- While R2 and R3 have OSPF interfaces in Area 0, traffic from Area 12 must cross Area 23 to reach Area 34

- An OSPF network with this design is discontiguous because interarea traffic is trying to cross a nonbackbone area

![discontiguous-net](./ospf-routes-discontiguous-net.png)

- At first glance it looks like routes in the routing table of R2 and R3 are being advertised across area 23

- The 10.34.1.0/24 network was advertised into OSPF by R3 and R4 as type 1 LSA

- R3 is an ABR and converts Area 34's 10.34.1.0/24 type 1 LSA into a type 3 LSA in Area 0

- R3 uses the type 3 LSA from Area 0 to generate the type 3 LSA for area 23

- R2 is able to install the type 3 LSA from Area 23 into it's routing table

- Most people would assume that the 10.34.1.0/24 route learned by area 23 would then be advertised into R2's Area 0 and then propagate to Area 12

- However, they would be wrong. There are three fundamental rules ABRs use for creating type 3 LSAs:

	- Type 1 LSAs received from an area, create type 3 LSAs into the backbone area and nonbackbone areas

	- Type 3 LSAs received from Area 0 are created for the nonbackbone area

	- Type 3 LSAs received from a nonbackbone area only insert into the LSDB for the source area. ABRs do not create a type 3 LSA for the other areas (including a segmented Area 0)

- The simplest fix for a discontiguous network is to ensure that Area 0 is contiguous

- There are other functions, like virtual link or usage of GRE tunnels, but they complicate the setup in these situations

- Real life scenarios of discontiguous networks involves Area 0 becoming partitioned due to hardware failures

- Ensuring that multiple paths exist to keep the backbone contiguous is an important factor in OSPF design

### OSPF Path Selection

- OSPF executes Dijikstra's shortest path first (SPF) algorithm to create a loop free topology of shortest paths

- All routers use the same logic to calculate the shortest path for each network

- Path selection prioritizes paths by using the following logic:

	1. Intra-area

	2. Interarea

	3. External routes

#### Intra-Area Routes

- Routes advertised via a type 1 LSA for an area are always preferred over type 3 LSAs

- If multiple intra-area routes exist, the path with the lowest total path metric is installed in the OSPF Routing Information Base (RIB), which is then presented to the router's global RIB

- If there is a tie in metric, both routes install into the OSPF RIB

![path-calculation](./calculating-ospf-path.png)

- In the above topology R1 is computing the route to 10.4.4.0/24 

- Instead of taking the fastest Ethernet connection (R1-R2-R4), R1 takes the path across the slower serial link (R1-R3-R4) to R4 because that is the intra-area path

- R1's routing table entry for 10.4.4.0/24:

```
show ip route 10.4.4.0
Routing entry for 10.4.4.0/24
	Known via "ospf 1", distance 110, metric 111, type intra area
	Last update from 10.13.1.3 on GigabitEthernet0/1, 00:00:42 ago
	Routing Descriptor Blocks:
	*	10.13.1.3 from 10.34.1.4, 00:00:42 ago, via GigabitEthernet0/1
		Route metric is 111, traffic share count is 1
```

- Notice that the metric is 111, and that the intra-area path was selected over the interarea path with a lower total path metric

#### Interarea Routes

- The next priority for selecting a path to a network is selection of the path with the lowest total path metric to the destination

- If there is a tie in metric both routes will install into the OSPF RIB

- All interarea paths for a route must go through Area 0 to be considered



