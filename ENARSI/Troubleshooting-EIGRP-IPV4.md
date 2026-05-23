## Troubleshooting EIGRP for IPv4

1. Troubleshooting EIGRP for IPv4 Neighbor Adjacencies

2. Troubleshooting EIGRP for IPv4 routes

3. Troubleshooting Miscellaneous EIGRP for IPv4 issues

4. EIGRP for IPv4 Trouble Tickets

- Before any routes can be exchanged between EIGRP routers on the same LAN or across a WAN, an EIGRP neighbor relationship must be formed

- Neighbor relationships may not form for many reasons, and as a troubleshooter, you need to be aware of them

- This chapter deeps into these issues and gives you the tools needed to identify them and successfully solve neighbor issues

- Once neighbor relationships are formed, neighboring routers exchange EIGRP routes

- In various cases, routes may end up missing, and you need to be able to determine why the routes are missing

- The various ways that routes could go missing and how you can identify them and solve route-related issues

- How to troubleshoot issues related to load balancing, summarization, discontiguous networks, and feasible successors

### Troubleshooting EIGRP for IPv4 Neighbor Adjacencies

- EIGRP establishes neighbor relationships by sending hello packets to the multicast address 224.0.0.10, out interfaces participating in the EIGRP process

- To enable the EIGRP process on an interface, you use the `network <ip-address> <wildcard-mask>` command in `router eigrp` configuration mode

- For example, the command `network 10.1.1.0 0.0.0.255` enables EIGRP on all interfaces with an IP address from 10.1.1.0 through 10.1.1.255

- The command `network 10.1.1.65 0.0.0.0` enables the EIGRP process on only the interface with the IP address 10.1.1.65

- It seems rather simple, and it is; however, for various reasons, neighbor relationships may not form, and all you need to be aware of all of them if you plan to successfully troubleshoot EIGRP-related problems

- Below will be discussed the reasons EIGRP neighbor relationships may not form and how to identify them during the troubleshooting process

- To verify the EIGRP neighbors, you use the `show ip eigrp neighbors` command

- Below is an example of `show ip eigrp neighbors` command:

```
R2#show ip eigrp neighbors 
EIGRP-IPv4 Neighbors for AS(65001)
H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)         (ms)       Cnt Num
2   172.16.23.3             Gi2                      12 00:04:12  112   672  0  6
1   172.16.24.4             Gi3                      11 00:04:12    7   100  0  3
0   172.16.12.1             Gi1                      13 00:04:12  228  1368  0  9
EIGRP-IPv4 VR(EIGRP-NAMED) Address-Family Neighbors for AS(65002)
R2#
```

- It lists the IPv4 address of the neighboring device's interface that sent the hello packet, the local interface on the router used to reach that neighbor, how long the local router will consider the neighboring router to be a neighbor, how long the routers has been neighbors, the amount of time it takes for the neighbors to communicate (on average), the number of EIGRP packets in a queue waiting to be sent to a neighbor (which should always be zero since you want up-to-date routing information), and a sequence number to keep track of the EIGRP packets received from the neighbor to ensure that only newer packets are accepted and processed

- EIGRP neighbor relationships may not form for a variety of reasons, including the following:

    - **Interface is down**: The interface must be up/up

    - **Mistmatched Autonomous System Numbers**: Both routers need to be using the same *autonomous system* number

    - **Incorrect network statement**: The `network` statement must identify the IP address of the interface you want to include in the EIGRP process 

    - **Mismatched K values**: Both routers must use exactly the same K values

    - **Passive Interface**: The `passive interface` feature suppresses sending and receiving of hello packets while still allowing the interface's network to be advertised

    - **Different subnets**:  