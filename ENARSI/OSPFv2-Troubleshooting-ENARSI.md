## Troubleshooting OSPFv2

1. Troubleshooting OSPFv2 Neighbor Adjacencies

2. Troubleshooting OSPFv2 Routes

3. Troubleshooting Miscellaneous OSPFv2 Issues

4. OSPFv2 Trouble Tickets

- The Open Shortest Path First (OSPF) dynamic routing protocol is a link-state routing protocol that uses *Dijkstra's Shortest Path First* algorithm

- It is an extremely scalable routing protocol because of it's hierarchical design

- OSPF can route both IPv4 and IPv6 protocols

- Before any routes are exchanged between OSPF routers on the same LAN or across a WAN, an OSPF neighbor relationship must be formed

- There are many reasons an OSPF neighbor relationship may not form, and as a troubleshooter, you need to be aware of them

- Delves deeply into the reasons for which this can happen and gives you the tools needed to identify them and successfully solve neighbor issues

- Once neighbor relationships are formed, neighboring routers exchange OSPF LSAs, which contain information about routes

- In various cases routes may end up missing, and you need to be able to determine why the routes are missing

- The various ways that OSPF routes could go missing, how to identify the reasons they are missing, and how to solve route-related issues

- You will also learn how to troubleshoot issues related to load-balancing, summarization, and discontiguous areas

### Troubleshooting OSPFv2 Neighbor Adjacencies

- OSPF establishes neighbor relationships by sending hello packets out interfaces participating in the OSPF process

- To enable the OSPF process on an interface and place it in an OSPF area, you use the `network <ip_address> <wildcard_mask> area <area-id>` command in router OSPF configuration mode or the `ip ospf <process-id> area <area-id>` command in an interface configuration mode

- For example, the following `network <ip_address> <wildcard-mask> area <area-id>` command enables OSPF on all interfaces with an IP address from 10.1.1.0 through 10.1.1.255 and places them in Area 0: `network 10.1.1.0 0.0.0.255 area 0`

- The following interface configuration command enables the OSPF process on the interface and places it in Area 51: `ip ospf 1 area 51`

```
conf t
 router ospf 1
  network 10.1.1.0 0.0.0.255 area 0
```

```
conf t
 interface g0/1
  ip ospf 1 area 51
```

- Because there are two different ways to enable OSPFv2 on an interface, you must be very careful when troubleshooting neighbor adjacencies so that you are not let down the wrong path, thinking that the OSPF process was not enabled on an interface when in fact it was

- You need to check both places

- This section focuses on the reasons an OSPF neighbor relationship may not form and how to identify them during the troubleshooting process

- To verify the OSPFv2 neighbors, you use the `show ip ospf neighbor` command

- Below is shown a sample output of the `show ip ospf neighbor` command

- It lists the neighbor ID, which is the router ID (RID) of the neighbor, the priority of the neighbor for the designated router/ backup designated router (BR/BDR) election process, the state of the neighbor, and whether the neighbor is a DR, BDR or DROTHER

- In addition, it displays the dead time, which is how long the local router waits until it declares the neighbor down if it does not hear another hello packet within that time (The default is 40 seconds on a LAN)

- You can also see the neighbor's interface IP address from which the hello packet was sent and the local router interface used to reach that neighbor

```
R2#show ip ospf neighbor 

Neighbor ID     Pri   State           Dead Time   Address         Interface
192.168.4.4       0   FULL/  -           -        10.1.34.4       OSPF_VL0
192.168.1.1       1   FULL/BDR        00:00:33    10.1.12.1       Ethernet0/0
192.168.3.3       1   FULL/DR         00:00:37    10.1.23.3       Ethernet0/1
```

- When an OSPF neighbor relationship is successfully formed, you receive a syslog message similar to the following:

```
*Oct 11 19:24:32.198: %OSPF-5-ADJCHG: Process 1, Nbr 192.168.1.1 on Ethernet0/0 from LOADING to FULL, Loading Done
```

- The following are some of the reasons an OSPFv2 neighbor relationship might not form:

    - **Interface is down**: The interface must be up/up

    - **Interface not running the OSPF process**: If the interface is not enabled for OSPF, it does not send hello packets or form adjacencies

    - **Mismatched timers**: Hello and dead timers must match between neighbors

    - **Mismatched Area numbers**: The two ends of the link must be in the same OSPF area

    - **Mismatched Area type**: In addition to a normal OSPF area type, an area type could be either a stub area or a not-so-stubby area (NSSA). The routers must agree on the type of area they are in

    - **Different subnets**: Neighbors must be in the same subnet

    - **Passive interface**: The passive interface feature supresses the sending and receiving of hello packets while still allowing the interface's network to be advertised

    - **Mismatched authentication information**: If one OSPF interface is configured for authentication, the OSPF interface at the other end of the link must be configured with matching authentication information

    - **ACLs**: An ACL may be denying packets to the OSPF multicast address 224.0.0.5

    - **MTU mismatch**: Neighboring interfaces must have maximum transmission unit (MTU) values

    - **Duplicate Router IDs**: Router IDs must be unique

    - **Mismatched network types**: Based on the OSPF network type characteristics and default values, two neighbors configured with a different OSPF network type might not form an adjacency

- Adjacencies are not established upon the immediate receipt of hello messages

- Rather, an adjacency transition through the various states described below:

```
State                           Description

Down                            This state indicates that no hellos have been received from a neighbor

Attempt                         This state occurs after a router sends a unicast hello (as opossed to a multicast hello) to a configured neighbor and has not
                                yet received a hello from that neighbor

Init                            This state occurs on a router that has received a hello message from it's neighbor; however, the OSPF RID of the receiving
                                router was not contained in the hello message. If a router remains in this state for a long period, something is probably
                                preventing that router from correctly receiving hello packets from the neighboring router

2-Way                           This state occurs when two OSPF routers have received hello messages from each other, and each router saw it's own RID in 
                                the hello message it received. The 2-Way state is an acceptable state to stay in between DROTHERs on an ethernet LAN

ExStart                         This state occurs when the routers forming a full neighbor adjacency decide who will sent their routing information first.
                                This is accomplished using the RID. The router with the higher RID becomes the primary, and the other one becomes the secondary.
                                The primary sends the routing information first. In a multi-access network, the DR and BDR have to be determined before this
                                state. However, the DR does not have to be the primary because each primary/secondary election is on a per-neighbor basis.
                                If a router remains in this state for a long period, an MTU mismatch could exist between the neighboring routers, or a duplicate RID might exist

Exchange                        This state occurs when the two routers forming an adjacency send one another database destriptor (DBD) packets containing
                                information about a router's link-state database. Each router compares the DBD packets received from the other router to identify
                                missing entries in it's own database. If a router remains in this state for a long period, an MTU mismatch could exist between
                                the neighboring routers

Loading                         Based on the missing link-state database entries identified in the Exchange state, the Loading state occurs when each neighboring
                                router requests the other router to send those missing entries. If a router remains in this state for a long period, a packet
                                might have been corrupted, or a router might have a memory issue. Alternatively, it is possible that such a condition could
                                result from the neighboring routers having an MTU mismatch

Full                            This state indicates that the neighboring OSPF routers have successfully exchanged their link-state information with one
                                another, and an adjacency has been formed
```

- When an OSPF neighbor relationship does not form, the neighbor is not listed in the OSPF neighbor table

- Therefore, you need the assistance of an accurate physical and logical network diagram and the `show cdp neighbors` command to verify who should be the neighbors

- When troubleshooting OSPF adjacencies, you need to be aware of how to verify the parameters associated with each of the reasons listed earlier

- Let's look at them individually

#### Interface is Down

- The interface must be up/up if you plan on forming an OSPF neighbor adjacency

- You can verify the status of an interface with the `show ip interface brief` command

```
R4#show ip int br
Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0         10.24.1.4       YES NVRAM  up                    up      
GigabitEthernet0/1         10.45.1.4       YES NVRAM  up                    up      
GigabitEthernet0/2         unassigned      YES NVRAM  administratively down down    
GigabitEthernet0/3         unassigned      YES NVRAM  administratively down down    
Loopback0                  192.168.4.4     YES NVRAM  up                    up      
```

#### Interface Not Running the OSPF process

- If the router OSPF configuration mode `network <ip_address> <wildcard_mask> area <area-id>` command or the `ip ospf <process-id> area <area-id` interface command is misconfigured, OSPF may not be enabled on the proper interfaces

- As a result, hello packets are not sent, and neighbor relationship are not formed

- You also must specify the OSPF area the interface belongs to

- Therefore, if the command is correct except for the area ID, the interface is participating in the OSPF process but in the wrong area

- This prevents a neighbor relationship from forming as well

- You can verify which interfaces are participating in the OSPF process by using the command `show ip ospf interface brief`, as shown below

- In this example, two interfces are participating in the OSPF process 1

- They are both in Area 1234 and are the designated router interfaces for the multi-access network

- You can also verify the IP addresses and masks of the interfaces, along with the number of full neighbor relationships formed out the interface compared to the total number of neighbors out the interface

- Remember that OSPF passive interfaces appear in the output of `show ip ospf interface brief`

```
R1(config-router)#do sh ip ospf int br
Interface    PID   Area            IP Address/Mask    Cost  State Nbrs F/C
Gi1          1     1               10.1.1.1/24        1     DR    0/0
Gi2          1     1               10.1.12.1/24       1     DR    1/1
```

- The output of `show ip protocols` displays the `network <ip_address> <wildcard_mask> area <area-id>` statements as well as interfaces that were enabled for OSPF with the `ip ospf <process-id> area <area-id>` command

- Take a look at the output below. Notice that it states `Routing for Networks:`

- These are not the networks you are routing for

- You are routing for the networks associated with the interface's OSPF will be enabled on based on the `network ... area ...` statement

- In addition, you can see which interfaces were explicitly configured to participate in the OSPF process by using the `ip ospf <process-id> area <area-id>` interface configuration mode command

- In this example, G2 was enabled for OSPF with the `ip ospf 1 area 1` command and G1 was enabled for OSPF with the `network 10.1.1.1 0.0.0.0 area 1` router ospf configuration mode command

```
R1(config-router)#do sh ip protoc
*** IP Routing is NSF aware ***

Routing Protocol is "application"
  Sending updates every 0 seconds
  Invalid after 0 seconds, hold down 0, flushed after 0
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Maximum path: 32
  Routing for Networks:
  Routing Information Sources:
    Gateway         Distance      Last Update
  Distance: (default is 4)

Routing Protocol is "ospf 1"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Router ID 10.1.12.1
  Number of areas in this router is 1. 1 normal 0 stub 0 nssa
  Maximum path: 4
  Routing for Networks:
    10.1.1.1 0.0.0.0 area 1
  Routing on Interfaces Configured Explicitly (Area 1):
    GigabitEthernet2
  Routing Information Sources:
    Gateway         Distance      Last Update
  Distance: (default is 110)

```

- The `network <ip_address> <wildcard_mask> area <area-id>` command is extremely important, as is the `ip ospf <process-id> area <area-id>` command

- If either of those commands is misconfigured, interfaces that should be participating in the OSPF process might not be, and interfaces that should not be participating in the OSPF process might be

- In addition, it is possible that interfaces might be participating but in the wrong area, preventing neighbor relationships from forming

- Therefore, you should be able to recognize issues related to both of these commands

- If an interface is enabled with both the `network <ip_address> <wildcard_mask> area <area-id>` command and the `ip ospf <process-id> area <area-id>` command, the `ip ospf <process-id> area <area-id>` command takes precedence

#### Mismatched Timers

- Unlike with Enhanced Interior Gateway Routing Protocol (EIGRP), with OSPF timers do have to match between neighbors in order for neighbor adjacencies to form

- The hello timer defaults to 10 seconds for broadcast and point-to-point network types and 30 seconds for non-broadcast and point-to-multipoint network types

- The dead timers default to 40 seconds for broadcast an point-to-point network types and 120 seconds for non-broadcast and point-to-multipoint network types

- To verify the current timers associated with an OSPF interface, issue the `show ip ospf interface <type> <number>` command 

- In this example G2 is using the default hello timer of 10 and dead timer of 40 seconds

- When determining whether timers match, use the spot-the-difference methods with the outputs on the two routers

```
R1#show ip ospf interface g2
GigabitEthernet2 is up, line protocol is up 
  Internet Address 10.1.12.1/24, Interface ID 8, Area 1
  Attached via Interface Enable
  Process ID 1, Router ID 10.1.12.1, Network Type BROADCAST, Cost: 1
  Topology-MTID    Cost    Disabled    Shutdown      Topology Name
        0           1         no          no            Base
  Enabled by interface config, including secondary ip addresses
  Transmit Delay is 1 sec, State DR, Priority 1
  Designated Router (ID) 10.1.12.1, Interface address 10.1.12.1
  Backup Designated router (ID) 10.1.12.2, Interface address 10.1.12.2
  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
    oob-resync timeout 40
    Hello due in 00:00:07
  Supports Link-local Signaling (LLS)
  Cisco NSF helper support enabled
  IETF NSF helper support enabled
  Can be protected by per-prefix Loop-Free FastReroute
  Can be used for per-prefix Loop-Free FastReroute repair paths
  Not Protected by per-prefix TI-LFA
  Index 1/1/2, flood queue length 0
  Next 0x0(0)/0x0(0)/0x0(0)
  Last flood scan length is 2, maximum is 2
  Last flood scan time is 0 msec, maximum is 0 msec
  Neighbor Count is 1, Adjacent neighbor count is 1 
    Adjacent with neighbor 10.1.12.2  (Backup Designated Router)
  Suppress hello for 0 neighbor(s)
```

- You can use the `debug ip ospf hello` command when troubleshooting adjacencies to reveal mismatched timers

```
R1#debug ip ospf hello 
OSPF hello debugging is on
*Oct 12 17:23:18.035: OSPF-1 HELLO Gi1: Rcv hello from 10.1.1.2 area 1 10.1.1.2
*Oct 12 17:23:18.035: OSPF-1 HELLO Gi1: Mismatched hello parameters from 10.1.1.2
*Oct 12 17:23:18.035: OSPF-1 HELLO Gi1: Dead R 44 C 40, Hello R 11 C 10 Mask R 255.255.255.0 C 255.255.255.0
*Oct 12 17:23:18.351: OSPF-1 HELLO Gi2: Send hello to 224.0.0.5 area 1 from 10.1.12.1
*Oct 12 17:23:18.697: OSPF-1 HELLO Gi1: Send hello to 224.0.0.5 area 1 from 10.1.1.1
R1#
*Oct 12 17:23:26.326: OSPF-1 HELLO Gi2: Rcv hello from 10.1.12.2 area 1 10.1.12.2
R1#
*Oct 12 17:23:27.638: OSPF-1 HELLO Gi2: Send hello to 224.0.0.5 area 1 from 10.1.12.1
*Oct 12 17:23:27.968: OSPF-1 HELLO Gi1: Rcv hello from 10.1.1.2 area 1 10.1.1.2
*Oct 12 17:23:27.968: OSPF-1 HELLO Gi1: Mismatched hello parameters from 10.1.1.2
*Oct 12 17:23:27.968: OSPF-1 HELLO Gi1: Dead R 44 C 40, Hello R 11 C 10 Mask R 255.255.255.0 C 255.255.255.0
*Oct 12 17:23:27.999: OSPF-1 HELLO Gi1: Send hello to 224.0.0.5 area 1 from 10.1.1.1
R1#
*Oct 12 17:23:36.146: OSPF-1 HELLO Gi2: Rcv hello from 10.1.12.2 area 1 10.1.12.2
R1#
*Oct 12 17:23:37.424: OSPF-1 HELLO Gi1: Send hello to 224.0.0.5 area 1 from 10.1.1.1
*Oct 12 17:23:37.439: OSPF-1 HELLO Gi2: Send hello to 224.0.0.5 area 1 from 10.1.12.1
R1#
*Oct 12 17:23:38.515: OSPF-1 HELLO Gi1: Rcv hello from 10.1.1.2 area 1 10.1.1.2
*Oct 12 17:23:38.515: OSPF-1 HELLO Gi1: Mismatched hello parameters from 10.1.1.2
*Oct 12 17:23:38.515: OSPF-1 HELLO Gi1: Dead R 44 C 40, Hello R 11 C 10 Mask R 255.255.255.0 C 255.255.255.0
R1#
*Oct 12 17:23:45.278: OSPF-1 HELLO Gi2: Rcv hello from 10.1.12.2 area 1 10.1.12.2
R1#
*Oct 12 17:23:46.580: OSPF-1 HELLO Gi2: Send hello to 224.0.0.5 area 1 from 10.1.12.1
*Oct 12 17:23:47.227: OSPF-1 HELLO Gi1: Send hello to 224.0.0.5 area 1 from 10.1.1.1
R1#
*Oct 12 17:23:49.437: OSPF-1 HELLO Gi1: Rcv hello from 10.1.1.2 area 1 10.1.1.2
*Oct 12 17:23:49.437: OSPF-1 HELLO Gi1: Mismatched hello parameters from 10.1.1.2
*Oct 12 17:23:49.437: OSPF-1 HELLO Gi1: Dead R 44 C 40, Hello R 11 C 10 Mask R 255.255.255.0 C 255.255.255.0
R1#
(...)

R1#
*Oct 12 17:17:46.285: %OSPF-5-ADJCHG: Process 1, Nbr 10.1.1.2 on GigabitEthernet1 from LOADING to FULL, Loading Done
R1#
```

- In this example the packet received (R) has a dead timer of 44 and hello timer of 11

- The local device, C, has a dead timer of 40 and hello timer of 10

#### Mismatched Area Numbers

- Because OSPF uses the concept of areas, it is an extremely scalable dynamic routing protocol

- For OSPF routers to form neighbor adjacencies, their neighboring interfaces must be in the same area

- You can verify the area an OSPF interface is part of by using the `show ip ospf interface <type> <number>` command, or the `show ip ospf interface brief` command

- When determining whether Area IDs match, you can use the spot-the-difference method with the output on the two routers

```
R1#show ip ospf interface g2
GigabitEthernet2 is up, line protocol is up 
  Internet Address 10.1.12.1/24, Interface ID 8, Area 1
  Attached via Interface Enable
  Process ID 1, Router ID 1.1.1.1, Network Type BROADCAST, Cost: 1
  Topology-MTID    Cost    Disabled    Shutdown      Topology Name
        0           1         no          no            Base
  Enabled by interface config, including secondary ip addresses
  Transmit Delay is 1 sec, State BDR, Priority 1
  Designated Router (ID) 3.3.3.3, Interface address 10.1.12.2
  Backup Designated router (ID) 1.1.1.1, Interface address 10.1.12.1
  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
    oob-resync timeout 40
    Hello due in 00:00:03
  Supports Link-local Signaling (LLS)
  Cisco NSF helper support enabled
  IETF NSF helper support enabled
  Can be protected by per-prefix Loop-Free FastReroute
  Can be used for per-prefix Loop-Free FastReroute repair paths
  Not Protected by per-prefix TI-LFA
  Index 1/1/2, flood queue length 0
  Next 0x0(0)/0x0(0)/0x0(0)
  Last flood scan length is 1, maximum is 3
  Last flood scan time is 0 msec, maximum is 0 msec
  Neighbor Count is 1, Adjacent neighbor count is 1 
    Adjacent with neighbor 3.3.3.3  (Designated Router)
  Suppress hello for 0 neighbor(s)
```

```
R1#show ip ospf interface brief 
Interface    PID   Area            IP Address/Mask    Cost  State Nbrs F/C
Gi1          1     1               10.1.1.1/24        1     BDR   1/1
Gi2          1     1               10.1.12.1/24       1     BDR   1/1
```

- You can use the `debug ip ospf adj` command when troubleshooting adjacencies to find mismatched area numbers as shown below

- In this example the packet received an area ID of 1, and the local interface is participating in Area 2

```
R2(config-if)#do debug ip ospf adj
OSPF adjacency debugging is on
R2(config-if)#ip os
R2(config-if)#ip ospf 1 a 2
R2(config-if)#
*Oct 12 17:41:18.646: OSPF-1 ADJ   Gi1: Interface going Up
R2(config-if)#
R2(config-if)#
R2(config-if)#
*Oct 12 17:41:27.071: OSPF-1 ADJ   Gi1: Rcv pkt from 10.1.12.1, area 0.0.0.2, mismatched area 0.0.0.1 in the header
R2(config-if)#
*Oct 12 17:41:36.088: OSPF-1 ADJ   Gi1: Rcv pkt from 10.1.12.1, area 0.0.0.2, mismatched area 0.0.0.1 in the header

*Oct 12 17:41:45.944: OSPF-1 ADJ   Gi1: Rcv pkt from 10.1.12.1, area 0.0.0.2, mismatched area 0.0.0.1 in the header

R2(config-if)#do un all
All possible debugging has been turned off
```

#### Mismatched Area Type

- The default OSPF area type is classified as a normal area

- However, you can convert a normal area into a stub area or a NSSA area to control the types of link-state advertisements (LSAs) that will be sent into the area from an area border router (ABR)

- For routers within an area to form adjacencies, they must agree on the area type

- Within the hello packet, a stub area flag is designed to indicate the type of area the neighbor is in

- You can verify the types of areas connected to a router by using the `show ip protocols` command

- However, it does not tell you which area is which type

- Below is displayed the output of `show ip protocols`, there is only one area (Area 1); therefore, you can deduce that it is the stub area

- However, for a router with multiple areas connected to it, you can verify the areas and their type by running the `show ip ospf` command

```
R1(config-router)#do sh ip protoc
*** IP Routing is NSF aware ***

Routing Protocol is "application"
  Sending updates every 0 seconds
  Invalid after 0 seconds, hold down 0, flushed after 0
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Maximum path: 32
  Routing for Networks:
  Routing Information Sources:
    Gateway         Distance      Last Update
  Distance: (default is 4)

Routing Protocol is "ospf 1"
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Router ID 1.1.1.1
  Number of areas in this router is 1. 0 normal 1 stub 0 nssa
  Maximum path: 4
  Routing for Networks:
    10.1.1.1 0.0.0.0 area 1
  Routing on Interfaces Configured Explicitly (Area 1):
    GigabitEthernet2
  Routing Information Sources:
    Gateway         Distance      Last Update
  Distance: (default is 110)

```

```
R1(config-router)#do sh ip ospf
 Routing Process "ospf 1" with ID 1.1.1.1
 Start time: 00:01:15.166, Time elapsed: 00:27:19.914
 Supports only single TOS(TOS0) routes
 Supports opaque LSA
 Supports Link-local Signaling (LLS)
 Supports area transit capability
 Supports NSSA (compatible with RFC 3101)
 Supports Database Exchange Summary List Optimization (RFC 5243)
 Event-log enabled, Maximum number of events: 1000, Mode: cyclic
 Router is not originating router-LSAs with maximum metric
 Initial SPF schedule delay 50 msecs
 Minimum hold time between two consecutive SPFs 200 msecs
 Maximum wait time between two consecutive SPFs 5000 msecs
 Incremental-SPF disabled
 Initial LSA throttle delay 50 msecs
 Minimum hold time for LSA throttle 200 msecs
 Maximum wait time for LSA throttle 5000 msecs
 Minimum LSA arrival 100 msecs
 LSA group pacing timer 240 secs
 Interface flood pacing timer 33 msecs
 Retransmission pacing timer 66 msecs
 EXCHANGE/LOADING adjacency limit: initial 300, process maximum 300
 Number of external LSA 0. Checksum Sum 0x000000
 Number of opaque AS LSA 0. Checksum Sum 0x000000
 Number of DCbitless external and opaque AS LSA 0
 Number of DoNotAge external and opaque AS LSA 0
 Number of areas in this router is 1. 0 normal 1 stub 0 nssa
 Number of areas transit capable is 0
 External flood list length 0
 IETF NSF helper support enabled
 Cisco NSF helper support enabled
 Reference bandwidth unit is 100000 mbps
    Area 1
        Number of interfaces in this area is 2
        It is a stub area
        Area has no authentication
        SPF algorithm last executed 00:00:52.411 ago
        SPF algorithm executed 15 times
        Area ranges are
        Number of LSA 5. Checksum Sum 0x027DAC
        Number of opaque link LSA 0. Checksum Sum 0x000000
        Number of DCbitless LSA 0
        Number of indication LSA 0
        Number of DoNotAge LSA 0
        Flood list length 0
```

- You can use the `debug ip ospf hello` command when troubleshooting to find mismatched area types

- In this example you can see that the packet received has a mismatched Stub/Transit area option bit

```
R3(config-router)#do sh run | s router ospf
router ospf 1
 router-id 3.3.3.3
 auto-cost reference-bandwidth 100000
 area 1 stub
R3(config-router)#
R3(config-router)#
R3(config-router)#no afre
R3(config-router)#no area 1 stub
R3(config-router)#d 
*Oct 12 19:48:38.220: %OSPF-5-ADJCHG: Process 1, Nbr 1.1.1.1 on GigabitEthernet1 from FULL to DOWN, Neighbor Down: Adjacency forced to reset
R3(config-router)#do debug ip ospf hello
OSPF hello debugging is on
R3(config-router)#
R3(config-router)#
R3(config-router)#
*Oct 12 19:48:45.626: OSPF-1 HELLO Gi1: Send hello to 224.0.0.5 area 1 from 10.1.12.2
R3(config-router)#
*Oct 12 19:48:53.185: OSPF-1 HELLO Gi1: Rcv hello from 1.1.1.1 area 1 10.1.12.1
*Oct 12 19:48:53.185: OSPF-1 HELLO Gi1: Hello from 10.1.12.1 with mismatched Stub/Transit area option bit
R3(config-router)#
*Oct 12 19:48:54.671: OSPF-1 HELLO Gi1: Send hello to 224.0.0.5 area 1 from 10.1.12.2
R3(config-router)#
*Oct 12 19:49:02.425: OSPF-1 HELLO Gi1: Rcv hello from 1.1.1.1 area 1 10.1.12.1
*Oct 12 19:49:02.425: OSPF-1 HELLO Gi1: Hello from 10.1.12.1 with mismatched Stub/Transit area option bit
R3(config-router)#
*Oct 12 19:49:03.778: OSPF-1 HELLO Gi1: Send hello to 224.0.0.5 area 1 from 10.1.12.2
R3(config-router)#do debug ip ospf hello   
*Oct 12 19:49:11.916: OSPF-1 HELLO Gi1: Rcv hello from 1.1.1.1 area 1 10.1.12.1
*Oct 12 19:49:11.916: OSPF-1 HELLO Gi1: Hello from 10.1.12.1 with mismatched Stub/Transit area option bit
*Oct 12 19:49:12.894: OSPF-1 HELLO Gi1: Send hello to 224.0.0.5 area 1 from 10.1.12.2
R3(config-router)#area 1 stub           
R3(config-router)#do yub 
*Oct 12 19:49:16.969: %OSPF-5-ADJCHG: Process 1, Nbr 1.1.1.1 on GigabitEthernet1 from DOWN to DOWN, Neighbor Down: Adjacency forced to reset
R3(config-router)#do un all
All possible debugging has been turned off
R3(config-router)#
*Oct 12 19:49:21.892: OSPF-1 HELLO Gi1: Rcv hello from 1.1.1.1 area 1 10.1.12.1
*Oct 12 19:49:21.893: OSPF-1 HELLO Gi1: Send immediate hello to nbr 1.1.1.1, src address 10.1.12.1
*Oct 12 19:49:21.893: OSPF-1 HELLO Gi1: Send hello to 10.1.12.1 area 1 from 10.1.12.2
*Oct 12 19:49:21.894: OSPF-1 HELLO Gi1: Rcv hello from 1.1.1.1 area 1 10.1.12.1
R3(config-router)#
*Oct 12 19:49:21.895: %OSPF-5-ADJCHG: Process 1, Nbr 1.1.1.1 on GigabitEthernet1 from LOADING to FULL, Loading Done
R3(config-router)#
```

#### Different Subnets

- To form an OSPF neighbor adjacency, the router interfaces must be on the same subnet

- You can verify this in many ways
