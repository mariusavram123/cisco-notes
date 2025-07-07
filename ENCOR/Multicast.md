## Multicast

1. Multicast fundamentals

2. Multicast addressing

3. Internet Group Management Protocol

4. Protocol Independent Multicast

5. Rendezvous Points

- Multicast is deployed in almost any type of network. It allows a source host to send data packets to a group of destination hosts (receivers) in an efficient manner that conserves bandwidth and system resources

- The need for multicast, and the fundamental protocols that are required to understand it's operation, such as IGMP and PIM dense mode/sparse mode and rendezvous points (RPs)

### Multicast Fundamentals

- Tradditional IP communication on a network typically uses one of the following transmission methods:

    - Unicast: One to one

    - Broadcast: One to all

    - Multicast: One to many

- Multicast technology is a technology that optimizes network bandwidth utilization and conserve system resources

- It relies on Internet Group Management Protocol (IGMP) for it's operation on Layer 2 networks and Protocol Indemendent Multicast (PIM) for it's operation in Layer 3 networks

- IGMP operation between the receivers and the local multicast router and how PIM operates between routers

- These two technologies work hand-in-hand to allow multicast traffic to flow from the source to the receivers

![multicast](./multicast-operation.png)

- Below is san example where six stations are watching the same video that is advertised by a server using unicast traffic (one-to-one)

- Each arrow represent a data stream of the same video going to five different hosts

![unicast-video](./unicast-video-5-stations.png)

- If each stream is 10 Mbps, the network link between R1 and R2 needs 50 Mbps of bandwidth

- The network link between R2 and R4 requires 30 Mbps of bandwidth, and the link between R2 and R5 requires 20 Mbps of bandwidth

- The server must maintain session state information for all the sessions between the hosts

- The bandwidth and load on the server increase as more receivers request the same video feed

- An alternative method for all five workstations to receive the video is to send it from the server using broadcast traffic (one-to-all)

- An example of how the same video stream is transmitted using IP directed broadcasts

- The load on the server is reduced because it needs to maintain only one session state rather than many

- The same video stream consumes only 10 Mbps of bandwidth

- However this approach does have it's disadvantages:

    - IP directed broadcast functionality is disabled by default on Cisco routers, and enabling it exposes the router to distributed denial-of-service (DDOS) attacks

    - The network interface cards (NICs) of unintended workstations must still process the broadcast packets and sends them to the workstation's CPU, which wastes processor resources. In our scenario, Workstation F is processing unwanted packets

- For these reasons broadcast traffic is generally not recommended

![broadcast-video](./broadcast-video-feed.png)

- Multicast traffic provides one-to-many communication, where only one data packet is sent on a link as needed and then is replicated between links and the data forks (splits) on a network device along the multicast distribution tree (MDT)

- The data packets are known as a stream that uses a special destination IP address, known as a group address

- A server for a stream still manages only one session, and network devices selectively request to receive the stream

- Recipient devices of a multicast stream are known as receivers

- Common applications that take advantage of multicast traffic:

    - Cisco TelePresence

    - real-time video

    - IPTV

    - Stock tickers

    - distance learning

    - video/audio conferencing

    - music on hold

    - gaming

- An example of the same video feed using multicast

![multicast-video](./multicast-video-feed.png)

- Each of the network links consumes only 10 Mbps of bandwidth, as much as with broadcast traffic, but only receivers interested in the video stream process the multicast traffic

- Workstation F would drop the traffic at the NIC level because it would not be programmed to accept the multicast traffic

- Workstation F would not receive any multicast traffic if the switch for that network segment enabled Internet Group Management Protocol (IGMP) snooping 

### Multicast Addressing

- The Internet Assigned Numbers Authority (IANA) assigned the IP class D address space 224.0.0.0/4 for multicast addressing

- It includes addressed ranging from 224.0.0.0 to 239.255.255.255. The first 4 bits of this whole range start with 1110

- In the multicast address space, multiple blocks of addressing are reserved for specific purposes:

```
Local network control block                 224.0.0.0 - 224.0.0.255

Internetwork control block                  224.0.1.0 - 224.0.1.255

Ad hoc block I                              224.0.2.0 - 224.0.2.255

Reserved                                    224.1.0.0 - 224.1.255.255

SDP/SAP block                               224.2.0.0 - 224.2.255.255

Ad hoc block II                             224.3.0.0 - 224.4.255.255

Reserved                                    224.5.0.0 - 224.255.255.255

Reserved                                    225.0.0.0 - 231.255.255.255

Source Specific Multicast (SSM) block       232.0.0.0 - 232.255.255.255

GLOP block                                  233.0.0.0 - 233.251.255.255

Ad hoc block III                            233.252.0.0 - 233.255.255.255

Reserved                                    234.0.0.0 - 238.255.255.255

Administratively scoped block               239.0.0.0 - 239.255.255.255
```

- Out of the multicast blocks, the most important are the following:

    - **Local network control block (224.0.0.0/24)**: Addresses on the local network control block are used for protocol control traffic that is not forwarded out a broadcast domain. Examples of this type of multicast control traffic are all hosts in this subnet (224.0.0.1), all routers in this subnet (224.0.0.2), and all PIM routers (224.0.0.13)

    - **Internetwork control block (224.0.1.0/24)**: Addresses in the internetwork control block are used for protocol control traffic that may be forwarded through the Internet. Examples include Network Time Protocol (NTP) (224.0.1.1), Cisco-RP-Announce (224.0.1.39), and Cisco-RP-Discovery (224.0.1.40)

- Some of the well-known local network control block and internetwork control block multicast addresses:

```
224.0.0.0           Base address (reserved)

224.0.0.1           All hosts in this subnet (all-hosts group)

224.0.0.2           All routers in this subnet

224.0.0.5           All OSPF routers (AllSPFRouters)

224.0.0.6           All OSPF DRs (AllDRouters)

224.0.0.9           All RIPv2 routers

224.0.0.10          All EIGRP routers

224.0.0.13          All PIM routers

224.0.0.18          VRRP

224.0.0.22          IGMPv3

224.0.0.102         HSRPv2 and GLBP

224.0.1.1           NTP

224.0.1.39          Cisco-RP-Announce (Auto-RP)

224.0.1.40          Cisco-RP-Discovery (Auto-RP)
```

- **Source Specific Multicast (SSM) block (232.0.0.0/8)**: This is the default range used by SSM. SSM is a PIM extension described in RFC 4607. SSM forward traffic to receivers from only those multicast sources which the receivers have explicitly expressed interest; it is primarry targetted to one-to-many applications

- **GLOP block (233.0.0.0/8)**: Addresses in the GLOP block are globally scopped statically assigned addresses. The assignment is made for domains with a 16-bit autonomous system number (ASN) by mapping the domain's ASN, expressed in octets as X.Y, into the middle two octets of the GLOP block, yielding an an assignment of 233.X.Y.0/24. The mapping and assignment are defined in RFC 3180. Domains with 32-bit ASN may apply for space in Ad hoc block III or can consider using IPv6 multicast addresses

- **Administratively scoped block (239.0.0.0/8)**: These addresses described in RFC 2365, are limited to a local group or organization. These addresses are similar to the reserved IP unicast ranges (such as 10.0.0.0/8), described in RFC 1918 and will not be assigned by the IANA to any other group or protocol. In other words network administrators are free to use multicast addresses in this range inside of their domain, without worrying about conflicting with others elsewhere on the Internet. Even though SSM is assigned to the 232.0.0.0/8 range by default, it is typically deployed in private networks using the 239.0.0.0/8 range

#### Layer 2 Multicast Addresses

- Historically, NICs on a LAN segment could retrieve only packets destined for their burned in MAC address or the broadcast MAC address

- Using this logic can cause burden on routing resources during packet replication for LAN segments

- Another method for multicast traffic was created so that replication of multicast traffic did not require packet manipulation, and a method of using a common destination MAC address was created

- A MAC address is a unique value associated with a NIC that is used to uniquely identify the NIC on a LAN segment

- MAC addresses are 12 digits hexadecimal numbers (48 bit in length), and they are typically stored in 8-bit segments separated by hyphens(-) or colons(:)

- Examples:

    - 00-12-34-56-78-90

    - 00:12:34:56:78:90

- Every multicast group address (IP address) is mapped to a special MAC address that allows Ethenet interfaces to identify multicast packets to a specific group

- A LAN segment can have multiple streams, and a receiver knows which traffic to send to the CPU for processing based on the MAC address assigned to the multicast traffic

- The first 24 bits of a multicast MAC address always start with 01:00:5E. The low-order bit of the first byte is the individual/group bit (I/G) bit, also known as the unicast/multicast bit, it indicates that the frame is a multicast frame, and the 25th bit is always 0

- The lower 23 bits of the multicast MAC address are copied from the lower 23 bits of the multicast group IP address

- An example of mapping the multicast IP address 239.255.1.1 into multicast MAC address 01:00:5E:7F:01:01. The first 25 bits are always fixed; the last 23 bits are copied directly from the multicast IP address vary

```
                                                                239         255     1           1
IP address in binary format:                                11101111.1  1111111.00000001.00000001
MAC address in binary format:             00000001.00000000.01011110.0  1111111.00000001.00000001
                                            1 - multicast bit              7F   .  01    .   01 
                                                                    0 - always 0
```

- Out of the 9 bits from the multicast IP address that are not copied into the multicast MAC address, the high-order bits 1110 are fixed. That leaves 5 bits that are variable that are not transferred into the MAC address

- Because of this there are 32 (2^^5) multicast IP addresses that are not universally unique and could correspond to a single MAC address, in other words, they overlap

- An example of two multicast MAC addresses that overlap because they map to the same multicast MAC address:

    - MAC address 01:00:5E:7F:01:01

![address-overlap](./multicast-mac-ip-address-overlap.png)

- When a receiver wants to receive a specific multicast feed, it sends an IGMP join using the multicast IP group assigned for that feed

- The receiver programs it's interface to accept the multicast MAC group address that correlates to the group address

- For example, a PC could send a join to 239.255.1.1 and would reprogram it's NIC to receive 01:00:5E:7F:01:01

- If the PC were to receive an OSPF update sent to 224.0.0.5 and it's corresponding multicast MAC address 01:00:5E:00:00:05, it would ignore it and eliminate wasted CPU cycles by avoiding the processing of undesired multicast traffic

### Internet Group Management Protocol (IGMP)

- Internet Group Management Protocol (IGMP) is the protocol that receivers use to join multicast groups and start receiving traffic from these groups

- IGMP must be supported by receivers and the router interfaces facing the receivers

- When a receiver wants to receive multicast traffic from a source, it sends an IGMP join to it's router

- If the router does not have IGMP enabled on the interface the request is ignored

- Three versions of IGMP exist. RFC 1112 defines IGMPv1 which is old and rarely used

- RFC 2236 defines IGMPv2, which is common on most multicast networks, and RFC 3376 defines IGMPv3 which is used by SSM

#### IGMPv2

- IGMPv2 uses the format show below. The message is encapsulated in an IP packet with a protocol number of 2

- Messages are sent with the IP router alert option set, which indicates that the packet should be examined more closely and a time to live (TTL) of 1

- TTL is an 8-bit field in in an IP packet header that is set by the sender of the IP packet and decremented by every router on the route to it's destination

- If the TTL reaches 0 before reaching the destination, the IP packet is discarded

- IGMP packets are sent with a TTL of one so that the packets are processed by the local router and not forwarded by any router

![igmp-format](./igmpv2-message-format.png)

- The IGMP message format fields are defined as follows:

    - **Type**: This field describes 5 different types of IGMP messages used by routers and receivers

    - **Version 2 Membership Report**: (type value 0x16) is a message type also commonly referred to as an IGMP join; it is used by receivers to join a multicast group or to respond to a local router's membership query message

    - **Version 1 Membership Report**: (type value 0x12) is used by receivers for backward compatibility with IGMPv1

    - **Version 2 Leave Group**: (type value 0x17) is used by receivers to indicate they want to stop receiving multicast traffic for a group they joined

    - **General Membership Query**: (type value 0x11) is sent periodically to the all-hosts group address (224.0.0.1) to see wether there are any receivers in the attached subnet. It sets the group address field to 0.0.0.0

    - **Group Specific Query**: (type value 0x11) is sent in response to a leave group message to the group address the receiver requeste to leave. The group address is the destination IP address of the IP packet and the group address field

    - **Max Response Time**: This field is set only in general and group-specific membership query messages (type value 0x11); it specifies the maximum allowed time before sending a responding report in units of one-tenth of a second. In all other messages it is set to 0x00 by the sender and ignored by the receivers

    