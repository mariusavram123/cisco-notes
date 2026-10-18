## OSPFv3

1. OSPFv3 Fundamentals

2. OSPFv3 Configuration

3. OSPFv3 LSA Flooding scope

- The Open Shortest Path First version 3 (OSPFv3) is the latest version of the OSPF protocol and includes support for both the IPv4 and IPv6 address families

- The OSPFv3 protocol is not backward compatible with OSPFv2, but the protocol mechanisms are essentially the same

### OSPFv3 Fundamentals

- OSPFv3 differs from OSPFv2 in several ways:

    - **Support for multiple address families**: OSPFv3 supports IPv4 and IPv6 address families

    - **New LSA types**: New LSA types have been created to carry IPv6 prefixes

    - **Removal of addressing semantics**: IP prefix information is no longer present in the OSPF packet headers. Instead it is carried as LSA payload information, making the protocol essentially address family independent, similar to Intermediate-System to Intermediate-System (IS-IS). OSPFv3 uses the term *link* instead of *network* because the shortest path first tree (SPF) calculations are per link instead of per subnet

    - **LSA Flooding**: OSPFv3 includes a new link-state type field that is used to determine the flooding scope of an LSA, as well as the handling of unknown LSA types

    - **Packet format**: OSPFv3 runs directly over IPv6, and the number of fields in the packet header has been reduced

    - **Router ID**: The router ID is used to identify the neighbors, regardless of the network type in OSPFv3

    - **Authentication**: Neighbor authentication has been removed from the OSPF protocol and is now performed through IPsec extension headers in the IPv6 packet

    - **Neighbor Adjacencies**: OSPFv3 inter-router communication is handled by IPv6 link-local addressing. Neighbors are not automatically detected over nonbroadcast multi-access (NBMA) interfaces. The neighbor must be manually specified using the link-local address. IPv6 allows multiple subnets to be assigned to a single interface, and OSPFv3 allows for neighbor adjacency to form even if the two routers do not share a common subnet

    - **Multiple instances**: An OSPFv3 packet includes an instance ID field that may be used to manipulate which routers on a network segment are allowed to form adjacencies

- RFC 5340 provides in-depth coverage of all the differences between OSPFv2 and OSPFv3

#### OSPFv3 Link-State Advertisement

- The OSPF Link State Database (LSDB) information is organized and advertised differently in version 3 than in version 2

- OSPFv3 modifies the structure of the router LSA (Type 1), uses the term inter-area prefix LSA instead of network summary LSA, and uses the term inter-area router LSA instead of Autonomous System Boundary Router (ASBR) summary LSA

- The principal difference is that the router LSA is only responsible for announcing interface parameters such as the interface type (point-to-point, broadcast, NBMA, point-to-multipoint and virtual links) and metric (cost)

- IP address information is advertised independently by two new LSA types:

    - Intra-area prefix LSA

    - Link-local LSA

- The OSPF Dijkstra's shortest path first (SPF) algorithm, used to to determine the SPT, only examines the router and network LSAs

- Advertising the IP prefix information using new LSA types eliminates the need for OSPF to perform full shortest path first (SPF) tree calculations every time a new IP address (prefix) is added or changed on an interface

- The OSPFv3 LSDB creates a shortest path topology tree based on links instead of networks

- Brief description of each OSPFv3 LSA type

```
LSA Type            Name                        Description

0x2001              Device                      Every router generates router LSAs that describe the the state and cost of the router's interfaces to the area

0x2002              Network                     A designated router generates network LSAs to announce all the routers attached to the link, including itself

0x2003              Inter-area prefix           Area border routers generate inter-area prefix LSAs to describe routes to IPv6 address prefixes that belong to
                                                other areas

0x2004              Inter-area router           Area border routers generate inter-area router LSAs to announce the addresses of autonomous system boundary
                                                routers in other areas


```