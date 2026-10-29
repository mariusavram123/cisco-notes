## Troubleshooting OSPFv3

1. Troubleshooting OSPFv3 for IPv6

2. OSPFv3 trouble tickets

3. Troubleshooting OSPFv3 Address Families

4. OSPFv3 AF trouble tickets

- The Open Shortest Path First version 3 (OSPFv3) dynamic routing protocol is a link-state routing protocol that uses *Dijkstra's shortest path first (SPF) algorithm*. It is an extremely scalable routing protocol because of it's hierarchical design. OSPFv3 is designed for routing IPv6 neighbors

- Troubleshooting OSPFv3 using classic configurations and also using the OSPF address family configurations

- Before any routes can be exchanged between OSPFv3 routers on the same LAN or across a WAN, an OSPFv3 neighbor relationship must be formed

- Neighbor relationships may fail to form for many reasons, and as a troubleshooter you need to be aware of them

- Focus on the OSPFv3 show commands that can be used for troubleshooting, and examples of them in various trouble tickets

- After neighbor relationships are formed, neighboring routers exchange OSPF link-state advertisements (LSAs), which contain information about routes

- In some cases, routes may end up missing, and you need to be able to determine why the routes are missing

- Focus on the OSPFv3 commands that that can be used to troubleshoot missing OSPFv3 routes in certain scenarios

### Troubleshooting OSPFv3 for IPv6

