## BGP

1. BGP fundamentals

2. Basic BGP configuration

3. Route Summarization

4. Multiprotocol BGP for IPv6

- RFC 1654 defines BGP(*Border Gateway Protocol*) as an EGP standardized path vector routing protocol that provides scalability, flexibility and network stability

- When BGP was created, the primary design consideration was IPv4 inter-organization connectivity on public networks like the Internet and on private dedicated networks

- BPG is the only protocol used to exchange networks on the Internet, which has more than 780000 IPv4 routes and continues to grow

- Due to the large size of BGP tables, BGP does not advertise incremental updates or refresh network advertisements as OSPF and IS-IS do

- BGP prefers stability within the network, as a link flap could result in route computation for thousands of routes

- Fundamentals of BGP: path attributes, address families, inter-router communication, BGP communication, route summarization and support for IPv6

### BGP Fundamentals

- From the perspective of BGP, an *autonomous system* (AS) is a collection of routers under a single organization's control, using one or more IGPs and common metrics to route packets within the AS

- If multiple IGPs or metrics are used within an AS, the AS must appear consistent to external ASs in routing policy

- An IGP is not required within the AS; an AS could use BGP as the only routing protocol

#### Autonomous System Numbers

- An organization requiring connectivity to the Internet must obtain an autonomous system number (ASN)

- ASNs were originally 2 bytes (16-bit range), which made 65535 ASNs possible

- Due to exhaustion, RFC 4893 expands the ASN field to accomodate 4 bytes (32-bit range)

- This allows for 4.294.967.295 unique ASNs, providing quite an increase from the original 65535 ASNs

- Two blocks of private ASNs are available for any organization to use, as long as they are never exchanged publicly on the Internet

- ASNs 64512 - 65535 are private ASNs in the 16-bit ASN range, and 4.200.000.000 4.294.967.294 are private ASNs within the extended 32-bit range

- The *Internet Assignment Numbers Authority* (IANA) is responsible for assigning all public ASNs to ensure that they are globally unique

- IANA requires the following items when requesting a public ASN:

    - Proof of a publicly allocated network range

    - Proof that Internet connectivity is provided through multiple connections

    - Need for a unique routing policy from providers

- In the event that an organization cannot provide this information, it should use the ASN provided by it's service provider

- It is imperative to use only the ASN assigned by IANA, the ASN assigned by your service provider or a private ASN

- Using another organization's ASN without permission could result in traffic loss and cause havoc on the Internet

#### Path Attributes

- BGP uses path attributes (PAs) associated with each path

- The PAs provide BGP with granularity and control of routing policies with BGP

- The BGP prefix PAs are classified as follows:

    - Well-known mandatory

    - Well-known discretionary

    - Optional transitive

    - Optional non-transitive

- Per RFC 4271, well-known attributes must be recognized by all BGP implementations

- Well-known mandatory attributes must be included with every prefix advertisement; well-known discretionary attributes may or may not be included with a prefix advertisement

- Optional attributes do not have to be recognized by all BGP implementations

- Optional attributes can be set so that they are transitive and stay with route advertisement from AS to AS

- Other PAs are *non-transitive* and cannot be shared from AS to AS

- In BGP, the *Network Layer Reachability Information (NLRI)* is a routing update that consists of the network prefix, prefix length and any BGP PAs for the specific route

#### Loop Prevention

- BGP is a path vector routing protocol and does not contain a complete topology of the network, as link-state routing protocols do

- BGP behaves like distance vector protocols, ensuring that the path is loop free

- The BGP attribute AS_Path is a well-known mandatory attribute and include a complete list of all the ASNs that the prefix advertisement has traversed from it's source AS

- AS_Path is used as a loop prevention mechanism in BGP

- If a BGP router receives a prefix advertisement with it's AS listed in the AS_Path attribute, it discards the prefix because the router thinks the advertisement forms a loop

![loop-prevention](./bgp-loop-prevention.png)

    - AS 100 advertises the prefix 172.16.1.0/24 prefix to AS 200

    - AS 200 advertises the prefix to AS 400, which then advertises the prefix to AS 300

    - AS 300 advertises the prefix back to AS 100 with an AS_Path of 300 400 200 100. AS 100 sees itself in the AS_Path variable and discards the prefix

#### Address Families

- Originally, BGP was intended for routing of IPv4 prefixes between organizations, but RFC 2858 added Multi-Protocol BGP (MP-BGP) capability by adding an extension called the address family identifier (AFI)

- An address family correlates to a specific network protocol, such as IPv4 or IPv6, and additional granularity is provided through a subsequent address-family identifier (SAFI) such as unicast or multicast

- MBGP achieves this separation by using the BGP path attributes (PAs) MP_REACH_NLRI and MP_UNREACH_NLRI

- These attributes are carried inside BGP update messages and are used to query network reachability information for different address families

- Some network engineers refer to Multiprotocol BGP as MP-BGP, and other engineers use the term MBGP. Both terms refer to the same thing

- Every address family maintains a separate database and configuration for each protocol (address-family + sub-address family) in BGP

- This allow for a routing policy in one address family to be different from a routing policy in a different address family, even through the router uses the same BGP session with the other router

- BGP includes an AFI and SAFI with every route advertisement to differentiate between AFI and SAFI databases

#### Inter-Router Communication

- BGP does not use hello packets to discover neighbors as do IGP protocols, and it cannot discover neighbors automatically

- BGP was designed as an inter-autonomous routing protocol, implying that neighbor adjacencies should not change frequently and are coordinated 

- BGP neighbors are defined by IP addresses

- BGP uses TCP port 179 to communicate with the other routers

- TCP allows for handling of fragmentation, sequencing and reliability (acknowledgement and retransmission) of communication packets

- Most recent implementations of BGP set the do-not-fragment (DF) bit to prevent fragmentation and rely on path MTU discovery

- IGPs follow the physical topology because the sessions are formed with hellos that cannot cross boundaries (that is, single hop only)

- BGP uses TCP, which is capable of crossing network boundaries (that is, multi-hop capable)

- While BGP can form neighbor adjacencies that are directly connected, it can also form adjacencies that are multiple hops away

- A BGP session refers to the established adjacency between 2 BGP routers

- Multi-hop sessions require that the router use an underlying route installed in the RIB (static or from any routing protocol) to establish the TCP session to the remote endpoint

![bgp-session](./single-and-multihop-bgp-peering.png)

- In the above figure, R1 is able to establish a direct BGP session with R2

- In addition, R2 is able to establish a BGP session with R4, even though it passes through R3

- R1 and R2 use a directly connected route to locate each other

- R2 uses a static route to reach the 10.34.1.0/24 network, and R4 has a static route to reach the 10.23.1.0/24 network

- R3 is unaware that R2 and R4 have established a BGP session even though the packets flow through R3

- BGP neighbors connected to the same network use the ARP table to locate the IP address of the peer

- Multi-hop BGP sessions require routing table information for finding the IP address of the peer

- It is common to have a static route or an IGP running between iBGP neighbors for providing the topology path information to establish the BGP TCP session

- A default route is not sufficient to establish a multi-hop BGP session

- BGP can be thought of as a control plane routing protocol or as an application because it allows for the exchange of routes with a peer that is multiple hops away

- BGP routers do not have to be in the data plane (path) to exchange prefixes, but all routers in the data path need to know all the routes that will be forwarded through them

#### BGP Session Types

- BGP sessions are categorized into two types:

    - **Internal BGP (iBGP)**: Session established with an iBGP router that are in the same AS or that participate in the same BGP confederation. iBGP prefixes are assigned an administrative distance (AD) of 200 upon installation in the router's RIB

    - **External BGP (eBGP)**: Session established with a BGP router that is in a different AS. eBGP prefixes are assigned an AD of 20 upon installation in the router's RIB

#### iBGP

- The need for BGP within an AS typically occurs when multiple routing policies are required or when transit connectivity is provided between autonomous systems

![transit-connectivity](./bgp-transit-connectivity.png)

- In our figure, AS 65200 provides transit connectivity to AS 65100 and AS 65300. AS 65100 connects at R2 and AS 65300 connects at R4

- R2 could form an iBGP session directly with R4, but R3 would not know where to route traffic from AS 65100 or AS 65300 when traffic from either AS reaches R3, because R3 would not have the appropriate forwarding information for the destination traffic, as seen below:

![route-advertisement-behaviour](./bgp-prefix-advertisement-behaviour.png)

- You might assume that redistributing the BGP table into an IGP overcomes the problem but this is not a viable solution for the following reasons:

    - **Scalability**: The internet has over 780000 + IPv4 network prefixes and continues to increase in size. IGPs cannot scale to that level of routes

    - **Custom Routing**: Link-state protocols and distance vector routing protocols use metric as the primary method for route selection. IGP protocols always use this routing pattern for path selection. BGP uses multiple steps to identify the best path and allows for BGP path attributes to manipulate the path for a specific prefix (NLRI). The path could be longer, and that would normally be deemed suboptimal from an IGPs perspective

    - **Path Attributes**: All the BGP path attributes cannot be maintained within IGP protocols. Only BGP is capable of maintaining the path attribute as the prefix is advertised from one edge of the AS to the other edge

- Establishing iBGP sessions between all the same routers (R2, R3 and R4) in a full mesh allows for proper forwarding between autonomous systems

- Service providers provide transit connectivity. Enterprise organizations are consumers and should not provide transit connectivity between autonomous systems across the Internet

#### eBGP

- eBGP peerings are the core components of BGP on the Internet

- eBGP involves exchaning of network prefixes between autonomous systems

- The following behaviors are different on eBGP sessions than on iBGP sessions:

    - Time to live (TTL) on eBGP packets is set to 1 by default. eBGP packets drop in transit if a multi-hop BGP session is attempted. (TTL on iBGP packets is set to 255, which allows for multihop sessions)

    - The advertising router modifies the BGP next-hop address to the IP address sourcing the BGP connection

    - The advertising router prepends it's ASN to the existing AS_Path variable

    - The receiving router verifies that the AS_Path variable does not contain an ASN that matches the local routers. BGP discards the NLRI if it fails the AS_Path loop prevention check

- The configurations for eBGP and iBGP sessions are fundamentally the same except that the ASN in the **remote-as** statement is different from the ASN defined in the BGP process

![topology](./bgp-sessions-setup.png)

- The above figure shows the eBGP and iBGP sessions that would be needed between the routers to allow connectivity between AS 65100 and 65300

- Notice that AS 65200 R2 establishes an iBGP session with R4 to overcome the loop-prevention behaviour of iBGP learned routes

#### BGP messages

- BGP communication uses four message types:

1. OPEN - Sets up and establishes BGP adjacency

2. UPDATE - Advertises, updates or withdrawns routes

3. NOTIFICATION - Indicates an error condition to a BGP neighbor

4. KEEPALIVE - Ensures that BGP neighbors are still active

- **OPEN**: An OPEN message is used to establish a BGP adjacency. Both sides negotiate session capabilities before BGP peering is established. The OPEN message contains the BGP version number, the ASN of the originating router, the hold time, the BGP identifier, and other optional parameters that establish the session capabilities

    - **Hold Time**: The hold time attribute sets the hold timer, in seconds for each BGP neighbor. Upon receipt of an UPDATE or KEEPALIVE, the hold timer resets to the initial value. If the hold timer reaches 0, the BGP session is torn down, routes from that neighbor are removed, and an appropriate update route withdraw message is sent to other BGP neighbors for the affected prefixes. The hold time is a heartbeat mechanism for BGP neighbors to ensure that a neighbor is healthy and alive

    - When establishing a BGP session, the routers use the smallest hold time value contained in two routers'OPEN messages. The hold time value must be at least 3 seconds, or is set to 0 to disable keepalive messages. For Cisco routers the default hold timer is 180 seconds

    - **BGP identifier**: The *BGP router ID (RID)* is a 32-bit unique number that identifies the BGP router in the advertised prefixes. The RID can be used as a loop-prevention mechanism for routers advertised within an autonomous system. The RID can be set manually or dynamically for BGP. A non-zero value must be set in order for routers to become neighbors

- **KEEPALIVE**: BGP does not rely on TCP connection state to ensure that the neighbors are still alive. KEEPALIVE messages are exchanged every one-third of the hold timer agreed upon between two BGP routers
- Cisco devices have a default hold timer of 180 seconds, so the default keepalive interval is 60 seconds

- If the hold time is set to 0, then no keepalive messages are sent between the BGP neighbors

- **UPDATE**: An UPDATE message advertises any feasible routes, withdraws previously advertised routes, or can do both. An UPDATE message includes the Network Layer Reachability Information (NLRI), such as prefix and associated BGP PAs, when advertising prefixes. Withdrawn NLRIs include only the prefix. An UPDATE message can act as a keepalive to reduce unnecessary traffic

- **NOTIFICATION**: A NOTIFICATION message is sent when an error is detected with the BGP session, such as hold timer expiring, neighbor capabilities changing, or a BGP session reset being requested. This causes the BGP connection to close

#### BGP Neighbor States

- BGP forms a TCP session with neighbor routers called *peers*. BGP uses the finite-state machine (FSM) to maintain a table of all BGP peers and their operational status

- The BGP session may report the following states:

    - Idle

    - Connect

    - Active

    - OpenSent

    - OpenConfirm

    - Established

![session-establishment](./bgp-session-establishment.png)

- The above scheme shows the BGP FSM and the states listed in the order used to establish a BGP session

##### Idle

- Idle is the first state of the BGP FSM. BGP detects a start event and tries to initiate a TCP connection to the BGP peer and also listens for a new connection from a peer router

- If an error causes BGP to go back to the Idle state, for a second time, the ConnectRetryTimer is set to 60 seconds and must decrement to 0 before the connection can be initiated again

- Further failures to leave the Idle state result in the ConnectRetryTimer doubling in length from the previous time

##### Connect

- In the Connect state, BGP initiates the TCP session. If the three-way TCP handshake is completed, the established BGP session process resets the ConnectRetryTimer and sends the Open message to the neighbor; then it changes to the OpenSent state

- If the ConnectRetryTimer depletes before this stage is complete, a new TCP connection is attempted, the ConnectRetryTimer is reset and the state is moved to Active. If any other input is received, the state is changed to Idle

- During this stage, the neighbor with the higher IP address manages the connection

- The router initiating the request uses a dynamic source port, but the destination port is always 179

![tcp-brief](./tcp-session-brief.png)

- The above output shows an established BGP session

- Displaying the TCP sessions active on a router:

```
show tcp brief
```

- Notice that the TCP source port is 179 and the destination port is 59884 on R1; the ports are opposite on R2

