## IP Routing Essentials

1. Routing Protocol Overview

2. Path Selection

3. Static Routing

4. Virtual Routing and Forwarding (VRF)

- A router is necessary to transmit packets between network segments

- This chapter explains the process a router uses to insert routes into the routing table from routing protocol databases and the methodologies for selecting a path

- A brief overview of static routing is provided as well

- By the end of this chapter you should have a solid understanding of the routing process on a router

## Routing Protocol Overview

- A router's primary function is to move an IP packet from one network to a different network

- A router learns about nonattached networks through configuration of static routes or through dynamic IP routing protocols

- Dynamic IP routing protocols distribute network topology information between routers and provide updates without intervention when a topology change in the network occurs

- Design requirements or hardware limitations may restrict IP routing to static routes, which do not accomodate topology changes very well and can burden network engineers, depending on the size of the network

- With dynamic routing protocols, routers try to select the best loop-free path on which to forward a packet to it's destination IP address

- A network of interconnected routers and related systems managed under a common network administration is known as an *autonomous system (AS)* or a routing domain

- The Internet is composed of thousands of autonomous systems spanning the globe

- The common dynamic routing protocols found on most routing platforms today are as follows:

    - **Routing Information Protocol Version 2**(RIP v2)

    - **Enhanced Interior Gateway Routing Protocol** (EIGRP)

    - **Open Shortest Path First** (OSPF)

    - **Intermediate System-to-Intermediate System** (IS-IS)

    - **Border Gateway Protocol** (BGP)

- With the exception of BGP, the protocols listed above are designed and optimized for routing within an Autonomous System and are known as Interior Gateway Protocols (IGPs)

- Exterior Gateway Protocols (EGPs) route between Autonomous Systems

- BGP is an EGP protocol but can also be used within an autonomous system

- If BGP exchanges routes within an autonomous system, it is known as *interior BGP (iBGP) session*

- If it exchanges routes between different autonomous systems, it is known as *exterior BGP (eBGP) session*

![BGP-iBGP-eBGP](./BGP-eBGP-iBGP.png)

- The above network scheme shows how one or many IGPs as well as iBGP can be running within an autonomous system and how eBGP sessions interconnect the various autonomous systems together

- EGPs and IGPs use different algorithms for path selection as follows in the next sections

### Distance Vector Algorithms

- Distance vector routing protocols, such as RIP, advertise routes as vectors, where distance is a metric (or cost) such as hop count, and vector is the next hop router's IP used to reach the destination:

    - **Distance**: The distance is the route metric to reach the network

    - **Vector**: The vector is the interface or direction to reach the network

- When a router receives routing information from a neighbor, it stores it in a local routing database as it is received, and the distance vector algorithm (such as Bellman-Ford and Ford-Fulkerson algorithms) is used to determine which paths are the best loop-free paths to each reachable destination

- When the best paths are determined, they are installed into the routing table and are advertised to each neighbor router

- Routers running distance vector protocols advertise the routing information to their neighbors from their own perspective, modified from the original route received

- Therefore, a distance vector protocol does not have a complete map of the whole network; instead it's database reflects that a neighbor router knows how to reach the destination network and how far the neighbor router is from the destination network

- The advantage of distance vector protocols is that they require less CPU and memory and can run on low-end routers

- An analogy commonly used to describe distance vector protocols is a road sign at an intersection indicating that the intersection is 2 miles to the west; drivers trust and blindly follow this indication that the destination is 2 miles to the west; drivers trust and blindly follow this information, without really knowing whether there is a shorter or better way to the destination or whether the sign is even correct

![Distance-vector](./Distance-vector-routing.png)

- The above scheme illustrates how a router using a distance vector routing protocol views the network and the direction that R3 needs to go to reach the 192.168.1.0/24 subnet

- A distance vector protocol selects paths purely based on distance

- It does not account for link speeds or other factors

- In the above figure the link between R1-R7 is a serial link with only 64 Kbps of bandwidth, and all other links are 1Gbps Ethernet links

- RIP does not take this into consideration and forwards traffic across this link which will result in packet loss when that link is oversubscribed

### Enhanced Distance Vector Algorithms

- The diffusing update algorithm (DUAL) is an enhanced distance vector algorithm that EIGRP uses to calculate the shortest path to a destination within a network

- EIGRP advertises network information to it's neighbors as other distance vector protocols do, but it haves some enhancements, as it's name suggests

- Enhancements introduced into this algorithm compared to other distance vector algorithms:

    - It offers rapid convergence time for changes in the network topology

    - It sends updates only when there is a change in the network. It does not send full routing table updates in a periodic fashion, as distance vector protocols do

    - It uses hellos and forms neighbor relationships just as link-state protocols do

    - It uses bandwidth, delay, reliability, load, and maximum transmission unit (MTU) size instead of hop count for path calculations

    - It has the option to load balance traffic across equal- or unequal-cost paths

- EIGRP is sometimes referred to as a *hybrid routing protocol* because it has characteristics of both distance vector and link-state protocols, as shown in the preceding list

- EIGRP relies on some more advanced metrics other than hop count (for example bandwidth) for it's best path calculations

- By default, EIGRP advertises the total path delay and minimum bandwidth for a route

- This information is advertised out every direction, as happens with a distance vector routing protocol; however, each router can calculate the best path based on the information provided by it's direct neighbors

![EIGRP-metrics](./distance-vector-eigrp-metric.png)

- This topology now includes EIGRP metric calculations for each link

- R3 is trying to forward packets to 192.168.1.0/24 network

- If the routing domain used a distance vector routing protocol, it would take the R3->R1->R7 path, which is only two hops away, rather than the path R3->R1->R2->R7, which is three hops away

- But the R3->R1->R7 path does not support traffic over 64 kbps

- While the R3->R1->R2->R7 path is longer, it provides more bandwidth and does not have as much delay (because of the serialization process on lower-speed interfaces) and is the path selected by EIGRP

### Link-State Algorithms

- A link-state IP routing protocol advertises the link state and link metric for each of it's connected links and directly connected routers to every router in the network

- OSPF and IS-IS are two link-state IP routing protocols commonly used in enterprise and service provider networks

- OSPF advertisements are called *link-state advertisements (LSAs)*, and IS-IS uses *link-state packets (LSPs)* for it's advertisements

- As a router receives an advertisement from a neighbor, it stores the information on the local database called *link-state database (LSDB)* and advertises link-state information on to each of it's neighbor routers exactly as it was received

- The link-state database is essentially flooded throughout the network, unchanged, from router to router, just as the originating router advertises it

- This allows all the routers in the network to have a synchronized and identical map of the network

- Using the complete map of the network, every router runs the Dijkstra shortest path first (SPF) algorithm to calculate the best shortest loop-free paths

- The link-state algorithm then populates the routing table with this information

- Due to having the complete map of the network, link-state protocols usually require more CPU and memory than the distance vector protocols, but they are less prone to routing loops and make better path decisions

- In addition, link-state protocols are equipped with extended capabilities such as opaque LSAs for OSPF and and TLVs (type/length/value) for IS-IS that allow them to support features commonly used by service providers, such as MPLS traffic engineering

- An analogy for link-state protocols is a GPS navigation system

- The GPS navigation system has a complete map and can make the best decision about which way is the shortest and best path to reach a destination

![LS-protocols-view](./link-state-protocols-view.png)

- The above picture illustrates how R3 would view the network to reach 192.168.1.0/24 subnet

- R1 will use the same algorithm as R3 and take the direct link to R4

### Path Vector Algorithm

- A path vector protocol such as BGP is similar to a distance vector protocol; the difference is that instead of looking at the distance to determine the next loop free path, it looks at various BGP path atributes

- BGP path attributes include autonomous system path (AS path), multi-exit discriminator (MED), origin, next hop, local preference, atomic aggregate and aggregator

- More about BGP path atributes are covered later

- A path vector protocol guarantees loop-free paths by keeping a record of each autonomous system that the routing advertisement traverses

- Any time a router receives an advertisement in which it is already part of the AS_Path, the advertisement is rejected because accepting the AS_Path would effectively result in a routing loop

- Loop prevention concept:

    1. R1 (AS1) advertises the 10.1.1.0/24 network to R2 (AS2). R1 adds the AS 1 to the AS_Path during the network advertisement to R2
    
    2. R2 advertises the 10.1.1.0/24 network to R4 and adds AS 2 to the AS_Path during the network advertisement to R4
    
    3. R4 advertises the 10.1.1.0/24 network to R3 and adds AS 4 to the AS_Path during the network advertisement to R3
    
    4. R3 advertises the 10.1.1.0/24 network back to R1 and R2 after adding AS 3 to the AS_Path during the network advertisement
    
    5. As R1 receives the 10.1.1.0/24 network advertisement from R3, it discards the route advertisement because R1 detects it's AS (AS 1) in the AS_Path "3 4 2 1" and considers the advertisement a loop. R2 discards the 10.1.1.0/24 network advertisement from R3 as it detects it's AS (AS 2) in the AS_Path "3 4 2 1" and considers it a loop too.
    
![BGP-route-advertisement](./bgp-route-advertisement.png)

- In the above scheme the advertisement of the 10.1.1.0/24 network towards R3 is not added to be easier to visualize, but the process happens in the other direction as well

- R3 attempts to advertise the 10.1.1.0/24 network to R2 as well

- R2 discards the route because R1 detects it's AS (AS 2) in the AS_Path "3 4 2 1" and considers it a loop as well - even though it did not source the original route

### Path Selection


