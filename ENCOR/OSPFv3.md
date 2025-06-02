## OSPFv3

1. OSPFv3 Fundamentals

2. OPSFv3 Configurations

3. IPv4 Support in OSPFv3

- OSPF version 3 (OSPFv3), the latest version of the OSPF protocol includes support for both IPv4 and IPv6 address families

- OSPFv3 is not backward compatible with OSPFv2 but the base mechanisms are the same

### OSPFv3 Fundamentals

- OSPFv3 vs OSPFv2:

	- **Support for multiple address families**: OSPFv3 supports IPv4 and IPv6 address families

	- **New LSA types**: New LSA types created to carry IPv6 prefixes

	- **Removal of addressing semantics**: The IP prefix information is no longer present in the OSPF packet header. Instead it is carried as LSA payload information, making the protocol essentially address-family independent, much like IS-IS. OSPFv3 uses the therm "link" instead of "network" because the SPT calculations are per link instead of per subnet

	- **LSA flooding**: OSPFv3 includes new link state type field that is used to determine the flooding scope of the LSA, as well as handling the unknown LSA types

	- **Packet format**: OSPFv3 runs directly over IPv6, and the number of fields in the packet header has been reduced

	- **Router ID**: The router ID is used to identify neighbors, regardless of the network type in OSPFv3. You must always manually assign the router ID for the OSPFv3 process

	- **Authentication**: Neighbor authentication has been removed from the OSPF protocol and is now performed through IPsec extension headers in the IPv6 packet

	- **Neighbor Adjacencies**: OSPFv3 inter-router communication is handled by IPv6 link-local addressing. Neighbors are not automatically detected over non-broadcast multi access (NBMA) interfaces. A neighbor must be manually specified using the link-local address. IPv6 allow for multiple subnets to be assigned to a single interface, and OSPFv3 allows for neighbor adjacency to form even if the two routers do not share a common subnet

	- **Multiple instances**: OSPFv3 packets include an instance ID field that may be used to manipulate which routers on a network segment are allowed to form adjacencies

- RFC 5340 shows the differences between OSPFv2 and OSPFv3 in depth

#### OSPFv3 Link-State Advertisement

- OSPFv3 packets use IP protocol number 89 and routers communicate with each-other using the local interface's IPv6 link-local address

- The link state database is organized differently in Version 3 than in Version 2

- LSAs modification in OSPFv3:

	- Modified structure of the router LSA (type 1)

	- Network summary LSA (type 3) renamed to interarea prefix LSA

	- ASBR summary LSA (type 4) renamed to interarea router LSA

	- The router LSA is only responsible for announcing interface parameters such as interface type (point-to-point, broadcast, NBMA, point-to-multipoint and virtual links) and metric (cost)

	- IP addressing information is advertised into two new LSA types:

		- Intra-area prefix LSA (contains global prefix information)

		- Link-local LSA (contains link-local information)

- The OSPF Dijikstra calculation is used to determine the shortest path tree (SPT) only advertises the router and network LSAs

- Advertising the IP address information using the new LSA types eliminates the need for OSPF to perform the full shortest path first (SPF) thee calculations every time a new address prefix is added or changed on an interface

- The OSPFv3 link state database (LSDB) creates a shortest path topology tree based on links instead of networks

- OSPFv3 LSA types description:

	- LS type: 0x2001, Name: Router, Description: Every router generates router LSAs that describes the state and cost of the router's interfaces to the area

	- LS type: 0x2002, Name: Network, Description: A designated router generates network LSAs to announce all of the routers attached to the link, including itself

	- LS type: 0x2003, Name: Interarea Prefix, Description: Area border routers generate interarea prefix LSAs to describe routes to IPv6 address prefixes that belong to other areas

	- LS typw: 0x2004, Name: Intra-area router, Description: Area border routers generate interarea router LSAs to announce the addresses of autonomous system boundary routers in other areas 

	- LS type: 0x4005, Name: AS external, Description: Autonomous system boundary routers advertise AS external LSAs to announce default routes or routes learned through redistribution from other protocols

	- LS type: 0x2007, Name: NSSA, Description: Autonomous system boundary routers that are located in a no-so-stubby area advertise NSSA LSAs for routers redistributed into the area

	- LS type: 0x0008, Name: Link, Description: The link LSA maps all the global unicast address prefixes associated with an interface to the link local interface IP address of the router

	- LS type: 0x2009, Name: Intra-area Prefix, Description: The intra-area prefix LSA is used to advertise one ore more IPv6 prefixes that are associated with a router, stub or transit network segment

#### OSPFv3 Communication

- OSPFv3 packets use protocol ID 89, and routers communicate with each-other using the local interface's IPv6 link-local address as the source

- Depending on the packet type, the destination address is a unicast link-local address or a multicast link-local scoped address:

	- FF02::5: OSPFv3 AllSPFRouters

	- FF02::6: OSPFv3 AllDRouters designated router (DR)

- All routers use the AllSPFRouters multicast address FF02::5 to send OSPF hello messages to routers on the same link

- The hello messages are used for neighbor discovery and detecting either a neighbor relationship is down

- The DR and BDR also uses this address to send link-state update and flooding acknowledgement messages to all routers

