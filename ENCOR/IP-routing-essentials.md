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

- 

