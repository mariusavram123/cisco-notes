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


