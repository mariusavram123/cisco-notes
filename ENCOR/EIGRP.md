## EIGRP - Enhanced Interior Gateway Routing Protocol

1. EIGRP fundamentals

2. Path Metric Calculation

3. Failure Detection and Timers

4. Route Summarization

- *Enhanced Interior Gateway Routing Protocol (EIGRP)* is an enhanced distance vector routing protocol commonly used in enterprise networks

- Initially, it was a Cisco proprietary protocol, but is was released to the Internet Engineering Task Force (IETF) through RFC 7868, which was ratified in May 2016

### EIGRP Fundamentals

- EIGRP overcomes the deficiencies of other distance vector routing protocols like RIP with features such as unequal-cost load balancing, support for networks 255 hops away, and rapid convergence features

- EIGRP uses a *diffusing update algorithm (DUAL)* to identify network paths and enable fast convergence using precalculated loop-free backup paths

- Most distance vector routing protocols use hop count as metric for routing decisions 

- However, using hop count for path selection does not take into account link speed and total delay

- EIGRP adds to the route selection algorithm logic that uses factors outside of hop count

#### Autonomous Systems

- A router can run multiple EIGRP processes. Each process operates under the context of an *autonomous system*, which represents a common routing domain

- Routers with the same domain use the same metric calculation formula and exchange routes with members of the same autonomous system

- An EIGRP autonomous system should not be confused with a Border Gateway Protocol (BGP) autonomous system

![multi-as](./eigrp-multi-as.png)

- In the above figure, EIGRP autonomous system (AS) 100 consists of R1, R2, R3 and R4, and EIGRP AS 200 consists of R3, R5 and R6

- Each EIGRP process correlates to a specific autonomous system and maintains an independent EIGRP topology table

- R1 does not have knowledge of routes from AS 200 because it is different from it's own autonomous system, AS 100

- R3 is able to participate in both autonomous systems and by default does not transfer routes learned from one autonomous system into a different autonomous system

#### EIGRP Terminology

- Core concepts of EIGRP and the path selection process in EIGRP

![EIGRP-topology](./EIGRP-network-topology.png)

- The above topology shows R1 calculating the best path and alternative loop-free paths to the 10.4.4.0/24 network

- Each value written on the links represents a particular link's calculated metric for a segment, based on the bandwidth and delay

- EIGRP terminology

- **Successor route**: The route with the lowest path metric to reach a destination. The successor route for R1 to reach 10.4.4.0/24 on R4 is R1-> R3 -> R4

- **Successor**: The first next-hop router for the successor route. The successor for 10.4.4.0/24 network is R3

- **Feasible Distance (FD)**: The metric value for the lowest-metric path to reach the destination. The feasible distance is calculated locally using the formula shown in the "Path Metric Calculation" section - later

- The FD calculated by R1 for 10.4.4.0/24 network is 3328 (that is, 256 + 256 + 2816)

- **Reported Distance (RD)**: The distance reported by a router to reach a prefix. The reported distance value is the feasible distance for the advertising router (the cost of the path as it is reported by my neighbor and can be seen in the captured packets). R3 advertises the 10.4.4.0/24 prefix with an RD of 3072. R4 advertises the 10.4.4.0/24 prefix to R1 and R2 with an RD of 2816

- **Feasibility condition**: A condition under which, for a route to be considered a backup route, the reported distance received for that route must be less than the feasible distance calculated locally. This logic guarantees a loop-free path

- **Feasible successor**: A route that satisfies the feasibility condition and is maintained as a backup route. The feasibility condition ensures that the backup path is loop-free

- The route R1->R4 is the feasible successor because RD 2816 is lower than the FD 3328 for the R1 -> R3 -> R4 path

#### Topology Table

- EIGRP contains a topology table that makes it different from a "true" distance vector routing protocol

- EIGRP's topology table is a vital component to DUAL and contains information to identify loop-free backup routes

- The topology table contains all the network prefixes advertised within an EIGRP autonomous system. Each entry in the table contains the following:

    - Network prefix

    - EIGRP neighbors that have advertised that prefix

    - Metrics from each neighbor (for example, reported distance, hop count)

    - Values used to calculate the metric (for example load, reliability, total delay, maximum bandwidth)

- Topology table for the 10.4.4.0/24 network and explaining the topology table

```
show ip eigrp topology
EIGRP-IPv4 Topology Table for AS(100)/ID(192.168.1.1)
Codes: P - Passive, A - Active, U - Update, Q - Query, R - Reply
    r - reply Status, s - sia Status

P 10.12.1.0/24, 1 successors, FD is 2816
    via Connected, GigabitEthernet0/3
P 10.13.1.0/24, 1 successors, FD is 2816
    via Connected, GigabitEthernet0/1
P 10.14.1.0/24, 1 successors, FD is 5120
    via Connected, GigabitEthernet0/2
P 10.23.1.0/24, 2 successors, FD is 3072
    via 10.12.1.2 (3072/2816), GigabitEthernet0/3
    via 10.13.1.3 (3072/2816), GigabitEthernet0/1
P 10.34.1.0/24, 1 successors, FD is 3072
    via 10.13.1.3 (3072/2816), GigabitEthernet0/1
    via 10.14.1.4 (5376/2816), GigabitEthernet0/2
P 10.24.1.0/24, 1 successors, FD is 5376
    via 10.12.1.2 (5376/5120), GigabitEthernet0/3
    via 10.14.1.4 (7680/5120), GigabitEthernet0/2
P 10.4.4.0/24, 1 successors, FD is 3328 ---> Feasible distance
    via 10.13.1.3 (3328/3072), GigabitEthernet0/1 ---> Successor Route
    via 10.14.1.4 (5376/2816), GigabitEthernet0/2 ---> Feasible Successor - Passes feasibility condition: 2816 < 3328
                5376 = Feasible distance
                2816 = Reported distance  
```

- Upon examining the network 10.4.4.0/24, notice that R1 calculates FD of 3328 for the successor route

- The successor (upstream router) advertises the successor route with an RD of 3072

- The second path entry has a metric of 5376 and has an RD of 2816

- Because 2816 is less than 3328 the second entry passes the feasibility condition, which means the second entry is classified as the feasible successor for the prefix

- The 10.4.4.0/24 route is passive (P), which means the topology is stable. During a topology change, routes go into an active (A) state when computing a new path

### EIGRP Neighbors

- EIGRP neighbors exchange the entire routing table when forming an adjacency, and they advertise only incremental updates as topology changes occur within a network

- The neighbor adjacency table is vital for tracking neighbor status and the updates send to each neighbor

- EIGRP uses five different packet types to communicate with other routers

- EIGRP uses it's own IP number (88); it uses multicast packets where possible and unicast packets when necessary

- Communication between routers is done with multicast, using group address 224.0.0.10 when possible 

- EIGRP packet types:

- Type: 1, Packet name: **Hello** - Used for discovery of EIGRP neighbors and for detecting when a neighbor is no longer available

- Type: 2, Packet name: **Request** - Used to get specific information from one or more neighbors

- Type: 3, Packet name: **Update** - Used to transmit routing and reachability information with other EIGRP neighbors

- Type: 4, Packet name: **Query** - Sent out to search for another path during convergence

- Type: 5, Packet name: **Reply** - Send in response to a Query packet

