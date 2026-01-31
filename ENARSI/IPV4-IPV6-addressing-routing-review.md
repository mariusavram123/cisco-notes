## IPv4/IPv6 Addressing and Routing review

1. IPv4 Addressing

2. DHCP for IPv4

3. IPv6 Addressing

4. IPv6 SLAAC, Stateful DHCPv6, Stateless DHCPv6

5. Packet Forwarding Process

6. Routing Information Sources

7. Static Routes

8. Trouble Tickets

- IPv6 is currently being deployed, but that deployment is occurring at a slow peace

- Most networks still rely on IPv4, and many new networks and network additions are being deployed only with IPv4

- Therefore you still need to the skills to successfully configure, verify and troubleshoot IPv4 addressing

- Typically when deploying IPv4 addresses, Dynamic Host Configuration Protocol (DHCP) is used so that addresses can be automatically assigned

- However, with this dynamic process, issues may arise that prevent a device from successfully obtaining an IPv4 address from a DHCP server

- How DHCP server operates and how to identify the issues that may prevent a client from obtaining an IP address from a DHCP server

- How IPv6-enabled devices determines whether a destination is local or remote and explores the various options for address assignment and what to look out for when troubleshooting

- Review the packet delivery process (also known as the routing process)

- This is the process that a router goes through when a packet arrives at an egress interface and needs to be packet switched to an egress interface

- It does not matter whether the packet is an IPv4 or IPv6 packet

- Either way, the router goes through the same steps to successfully take a packet from an ingress interface and packet switch it to the egress interface

- Review how a router populates the routing table with "the best" routes

- What classifies those routes as the best?

- Is an EIGRP-learned route better than a static route?

- What about an OSPF-learned route or a BGP-learned route?

- How do they compare with the other sources of routing information?

- Be able to identify why the router made the decision it made

- Static routes are part of every network

- However, because they are manually configured, they are prone to human error, which may lead to suboptimal routing or routing loops

- Review IPv4 and IPv6 static routing configuration and verification

### IPv4 Addressing

- Just as your personal street address uniquely defines where you live, an IPv4 address uniquely defines where a device resides in a network

- Your street address is made of two parts - the number of your residence and the street name - and the combination of those is unique to your city/town


