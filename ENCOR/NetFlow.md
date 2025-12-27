## NetFlow and Flexible NetFlow

- Gathering statistics about a network during it's operations is not only useful but important

- Gathering statistical information on traffic flows is necessary for a number of reasons

- Some businesses, such as service providers, use it for customer billing

- Other businesses use it to determine whether traffic is optimally flowing through the network

- Some use it for troubleshooting if the network is not performing correctly

### NetFlow

- **NetFlow** is versatile and provides a wealth of information without much configuration burden

- That being said, NetFlow has two components that must be configured: *NetFlow data capture* and *NetFlow data export*

- NetFlow Data Capture captures the traffic statistics

- NetFlow Data Export exports the statistical data to a NetFlow collector such as Cisco DNA Center or Cisco Prime Infrastructure

- Examples are provided below

- There are a couple of things to note from a design perspective prior to enabling NetFlow:

    - NetFlow consumes memory resources

    - The traffic statistics are captured in the memory cache

    - The default size of the cache is platform specific and should be investigated prior to enabling NetFlow

    - This is especially the case with older platforms that potentially have lower memory resources available

- NetFlow captures traffic on ingress and egress - that is traffic that is coming into the devices as well as traffic that is leaving them

- Below are listed the different types of ingress and egress traffic collected with NetFlow Version 9 on a Cisco IOS-XE device:

```
Ingress                                                                     Egress

IP to IP packets                                                            NetFlow accounting for all IP traffic packets

IP to Multiprotocol Label Switching (MPLS) packets                          MPLS to IP packets

Frame Relay terminated packets

ATM terminated packets
```

- NetFlow collects traffic based on flows

- A *flow* is a unidirectional traffic stream that contains a combination of the following key fields:

    - Source IP address

    - Destination IP address

    - Source port number

    - Destination port number

    - Layer 3 protocol type

    - Type of service (TOS)

    - Input logical interface

- Below is shown how to enable NetFlow on a device

- (If the desired intention is not to export the NetFlow data to a collector, that step can be skipped)

- Below is shown the configuration of R1's G0/1 interface for NetFlow data capture and exporting the data to the 172.16.29.17 collector

- The process of configuring the NetFlow Data Capture and NetFlow Data Export on R1

```
conf t
 ip flow-export version 9
 ip flow-export destination 172.16.29.17 9999
 interface g0/1
  ip flow ingress
  ip flow egress
```

- To verify that NetFlow and NetFlow Data Export were configured properly, you can run a few commands from the command line interface:

- The first is `show ip flow interface` which shows the interfaces configured for NetFlow:

```
R1#show ip flow interface 
GigabitEthernet0/1
  ip flow ingress
  ip flow egress
```

- The second is `show ip flow export` command, which shows the destination for the NetFlow data to be exported to as well as statistics on the export, including any errors that may arise:

```
R1#sh ip flow export
Flow export v9 is enabled for main cache
  Export source and destination details : 
  VRF ID : Default
    Destination(1)  172.16.29.17 (9999) 
  Version 9 flow records
  46 flows exported in 22 udp datagrams
  0 flows failed due to lack of export packet
  0 export packets were sent up to process level
  0 export packets were dropped due to no fib
  0 export packets were dropped due to adjacency issues
  0 export packets were dropped due to fragmentation failures
  0 export packets were dropped due to encapsulation fixup failures
```

- Finally, the `show ip cache flow` command shows the traffic flows that NetFlow is capturing:

```
R1#show ip cache flow 
IP packet size distribution (47 total packets):
   1-32   64   96  128  160  192  224  256  288  320  352  384  416  448  480
   .000 .000 .000 .127 .000 .191 .553 .000 .127 .000 .000 .000 .000 .000 .000

    512  544  576 1024 1536 2048 2560 3072 3584 4096 4608
   .000 .000 .000 .000 .000 .000 .000 .000 .000 .000 .000

IP Flow Switching Cache, 278544 bytes
  1 active, 4095 inactive, 42 added
  719 ager polls, 0 flow alloc failures
  Active flows timeout in 30 minutes
  Inactive flows timeout in 15 seconds
IP Sub Flow Cache, 34056 bytes
  1 active, 1023 inactive, 42 added, 42 added to flow
  0 alloc failures, 0 force free
  1 chunk, 1 chunk added
  last clearing of statistics never
Protocol         Total    Flows   Packets Bytes  Packets Active(Sec) Idle(Sec)
--------         Flows     /Sec     /Flow  /Pkt     /Sec     /Flow     /Flow
UDP-other           21      0.0         1   194      0.0       0.0      15.6
ICMP                20      0.0         1   195      0.0       3.1      15.7
Total:              41      0.0         1   194      0.0       1.5      15.6
          
SrcIf         SrcIPaddress    DstIf         DstIPaddress    Pr SrcP DstP  Pkts

SrcIf         SrcIPaddress    DstIf         DstIPaddress    Pr SrcP DstP  Pkts
Gi0/1         172.16.29.17    Local         172.16.29.16    01 0000 0303     1 
```

- Another great option for NetFlow is being able to configure the top specified number of talkers on the network

- A useful and quick configuration allows you to gain a great snapshot of what is going on in a device from a flow perspective

- This view can be enabled by issuing the following global config mode command, and then configuring the top number of talkers (between 1 and 200), and sort by bytes or packets:

```
conf t
 ip flow-top-talkers
  top 10
  sort-by bytes # or packets
```

- Viewing the flow top talkers:

```
R1(config)#do sh ip flow top-talkers

SrcIf         SrcIPaddress    DstIf         DstIPaddress    Pr SrcP DstP Bytes
Gi0/1         172.16.29.17    Local         172.16.29.16    11 E414 00A1    74 
Gi0/1         172.16.29.17    Local         172.16.29.16    11 CE0D 00A1    73 
2 of 10 top talkers shown. 2 flows processed.

```

### Flexible NetFlow

- Flexible NetFlow was created to aid in more complex traffic analysis configuration that is not possible with traditional NetFlow

- Flexible NetFlow allows for the use and reuse of configuration components

- Below are listed the components that make Flexible NetFlow powerful

- Flexible NetFlow allows for the use of multiple flow monitors on the same traffic at the same time

- This means that multiple different flow policies can be applied to the same traffic as it flows through a device

- If two different departments have a reason to analyze the traffic, they can both do so by using different parameters in each flow monitor

```
Component Name                                          Description

Flow Records                                            Combination of key and non-key fields. There are predefined and user-defined records

Flow Monitors                                           Applied to the interface to perform network traffic monitoring

Flow Exporters                                          Exports NetFlow version 9 data from the Flow Monitor cache to a remote host or NetFlow collector

Flow Samplers                                           Samples partial NetFlow data rather than analyzing all NetFlow data
```

- There are trade-offs in using sampled NetFlow data

- The biggest one is that there is a reduced load on the device in terms of memory and CPU

- However, by sampling NetFlow data only at specific intervals, something could be missed because the accuracy goes down with sampling compared to when gathering all data

- Depending on the use case and the environment, however, sampling may be perfectly acceptable

- It all depends on the business and it's priorities

- Security has been a huge driver in adoption of Flexible NetFlow due to it's ability to track all parts of the IP header as well as the packet and normalize into flows

- Flexible NetFlow can dynamically create individual caches for each type of flow

- In addition, Flexible NetFlow can filter ingress traffic destined to a single destination

- This factors make Flexible NetFlow a powerful security asset

- You can use the `collect` and `match` commands to create a customized flow record

- To create a custom flow record, certain key and non-key fields must be matched so that the flow record is usable

- The `match` command is used to select key fields, and the `collect` command is used to select non-key fields

- Below is shown a list of the key and non-key fields that can be used to mimic the original NetFlow capabilities when building a custom flow record

- Flow record key and non-key fields

```
Field                               Key or non-key field                                    Definition

IP ToS                              Key                                                     Value in the type of service (ToS) field

IP protocol                         Key                                                     Value in the IP protocol field

IP source address                   Key                                                     IP source address

IP destination address              Key                                                     IP destination address

Transport source port               Key                                                     Value of the transport layer source port field

Transport destination port          Key                                                     Value on the transport layer destination port field

Interface input                     Key                                                     Interface on which the traffic is received

Flow sampler ID                     Key                                                     ID number of the flow sampler (if flow sampling is disabled)

IP source AS                        Non-key                                                 Source autonomous system number

IP destination AS                   Non-key                                                 Destination autonomous system number

IP next-hop address                 Non-key                                                 IP address of the next hop

IP source mask                      Non-key                                                 Mask for the IP source address

IP destination mask                 Non-key                                                 Mask for the IP destination address

TCP flags                           Non-key                                                 Value in the TCP flag field

Interface output                    Non-key                                                 Interface on which the traffic is transmitted

Counter bytes                       Non-key                                                 Number of bytes seen in the flow

Counter packets                     Non-key                                                 Number of packets seen in the flow

Time stamp system uptime first      Non-key                                                 System uptime (time, in miliseconds, since this device
                                                                                            has first booted) when the first packet has switched

Time stamp system uptime last       Non-key                                                 System uptime (time, in miliseconds, since this device has
                                                                                            first booted) when the last packet was switched
```

- Configuring flow records is an important step in enabling Flexible NetFlow because flow record defines what type of traffic will be analized or monitored

- There are predefined flow records, and you can also create custom flow records

- Custom flow records can have hundreds of different combinations to meet the exact needs of business

- Configuring a custom flow record involves the following steps:

    1. Define the flow record name

    2. Set a useful description for the flow record

    3. Set match criteria for key fields

    4. Define non-key fields to be collected

- Many of the predefined flow records that are available may be suitable for many use cases

- Having the ability to build a custom flow record for a specific and unique use case makes it exteremely powerful

- Below is shown a custom record named CUSTOM1 being defined on R4

- This example uses the `match` command to match the IPv4 destination address and the `collect` command to gather the byte and packet counts

```
conf t
 flow-record CUSTOM1
  description Custom Flow Record for IPv4 Traffic
  match ipv4 destination address
  collect counter bytes
  collect counter packets
```

- To verify the flow record configuration, you can use the `show flow record CUSTOM1` command

```
R4(config-flow-record)#do sh flow record CUSTOM1
flow record CUSTOM1:
  Description:        Custom Flow Record For IPv4 Packets
  No. of users:       0
  Total field space:  12 bytes
  Fields:
    match ipv4 destination address
    collect counter bytes
    collect counter packets
```

- To see all flow record configured, including predefined flow records, you can use the `show flow record` command by itself

```
R4#show flow record 
flow record netflow-original:
  Description:        Traditional IPv4 input NetFlow with origin ASs
  No. of users:       0
  Total field space:  53 bytes
  Fields:
    match ipv4 tos
    match ipv4 protocol
    match ipv4 source address
    match ipv4 destination address
    match transport source-port
    match transport destination-port
    match interface input
    match flow sampler
    collect routing source as
    collect routing destination as
    collect routing next-hop address ipv4
    collect ipv4 source mask
    collect ipv4 destination mask
    collect transport tcp flags
    collect interface output
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv4 original-input:
  Description:        Traditional IPv4 input NetFlow with ASs
  No. of users:       0
  Total field space:  53 bytes
  Fields:
    match ipv4 tos
    match ipv4 protocol
    match ipv4 source address
    match ipv4 destination address
    match transport source-port
    match transport destination-port
    match interface input
    match flow sampler
    collect routing source as
    collect routing destination as
    collect routing next-hop address ipv4
    collect ipv4 source mask
    collect ipv4 destination mask
    collect transport tcp flags
    collect interface output
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv4 original-input peer:
  Description:        Traditional IPv4 input NetFlow with peer ASs
  No. of users:       0
  Total field space:  53 bytes
  Fields:
    match ipv4 tos
    match ipv4 protocol
    match ipv4 source address
    match ipv4 destination address
    match transport source-port
    match transport destination-port
    match interface input
    match flow sampler
    collect routing source as peer
    collect routing destination as peer
    collect routing next-hop address ipv4
    collect ipv4 source mask
    collect ipv4 destination mask
    collect transport tcp flags
    collect interface output
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv4 original-output:
  Description:        Traditional IPv4 output NetFlow with ASs
  No. of users:       0
  Total field space:  53 bytes
  Fields:
    match ipv4 tos
    match ipv4 protocol
    match ipv4 source address
    match ipv4 destination address
    match transport source-port
    match transport destination-port
    match interface output
    match flow sampler
    collect routing source as
    collect routing destination as
    collect routing next-hop address ipv4
    collect ipv4 source mask
    collect ipv4 destination mask
    collect transport tcp flags
    collect interface input
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv4 original-output peer:
  Description:        Traditional IPv4 output NetFlow with peer ASs
  No. of users:       0
  Total field space:  53 bytes
  Fields:
    match ipv4 tos
    match ipv4 protocol
    match ipv4 source address
    match ipv4 destination address
    match transport source-port
    match transport destination-port
    match interface output
    match flow sampler
    collect routing source as peer
    collect routing destination as peer
    collect routing next-hop address ipv4
    collect ipv4 source mask
    collect ipv4 destination mask
    collect transport tcp flags
    collect interface input
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv4 as:
  Description:        AS aggregation schemes
  No. of users:       0
  Total field space:  29 bytes
  Fields:
    match routing source as
    match routing destination as
    match interface input
    match interface output
    match flow direction
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv4 as peer:
  Description:        AS aggregation scheme with peer ASs
  No. of users:       0
  Total field space:  29 bytes
  Fields:
    match routing source as peer
    match routing destination as peer
    match interface input
    match interface output
    match flow direction
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv4 as-tos:
  Description:        AS and TOS aggregation schemes
  No. of users:       0
  Total field space:  30 bytes
  Fields:
    match routing source as
    match routing destination as
    match ipv4 tos
    match interface input
    match interface output
    match flow direction
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv4 as-tos peer:
  Description:        AS and TOS aggregation scheme with peer ASs
  No. of users:       0
  Total field space:  30 bytes
  Fields:
    match routing source as peer
    match routing destination as peer
    match ipv4 tos
    match interface input
    match interface output
    match flow direction
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv4 assurance:
  Description:        Assurance metrics
  No. of users:       0
  Total field space:  6 bytes
  Fields:
    match ipv4 version
    match ipv4 protocol
    match application name

flow record netflow ipv6 original-input:
  Description:        Traditional IPv6 input NetFlow with ASs
  No. of users:       0
  Total field space:  97 bytes
  Fields:
    match ipv6 traffic-class
    match ipv6 flow-label
    match ipv6 protocol
    match ipv6 extension map
    match ipv6 source address
    match ipv6 destination address
    match transport source-port
    match transport destination-port
    match interface input
    match flow direction
    match flow sampler
    collect routing source as
    collect routing destination as
    collect routing next-hop address ipv6
    collect ipv6 source mask
    collect ipv6 destination mask
    collect transport tcp flags
    collect interface output
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv6 original-input peer:
  Description:        Traditional IPv6 input NetFlow with peer ASs
  No. of users:       0
  Total field space:  97 bytes
  Fields:
    match ipv6 traffic-class
    match ipv6 flow-label
    match ipv6 protocol
    match ipv6 extension map
    match ipv6 source address
    match ipv6 destination address
    match transport source-port
    match transport destination-port
    match interface input
    match flow direction
    match flow sampler
    collect routing source as peer
    collect routing destination as peer
    collect routing next-hop address ipv6
    collect ipv6 source mask
    collect ipv6 destination mask
    collect transport tcp flags
    collect interface output
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv6 original-output:
  Description:        Traditional IPv6 output NetFlow with ASs
  No. of users:       0
  Total field space:  97 bytes
  Fields:
    match ipv6 traffic-class
    match ipv6 flow-label
    match ipv6 protocol
    match ipv6 extension map
    match ipv6 source address
    match ipv6 destination address
    match transport source-port
    match transport destination-port
    match interface output
    match flow direction
    match flow sampler
    collect routing source as
    collect routing destination as
    collect routing next-hop address ipv6
    collect ipv6 source mask
    collect ipv6 destination mask
    collect transport tcp flags
    collect interface input
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv6 original-output peer:
  Description:        Traditional IPv6 output NetFlow with peer ASs
  No. of users:       0
  Total field space:  97 bytes
  Fields:
    match ipv6 traffic-class
    match ipv6 flow-label
    match ipv6 protocol
    match ipv6 extension map
    match ipv6 source address
    match ipv6 destination address
    match transport source-port
    match transport destination-port
    match interface output
    match flow direction
    match flow sampler
    collect routing source as peer
    collect routing destination as peer
    collect routing next-hop address ipv6
    collect ipv6 source mask
    collect ipv6 destination mask
    collect transport tcp flags
    collect interface input
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv6 as:
  Description:        AS aggregation schemes
  No. of users:       0
  Total field space:  29 bytes
  Fields:
    match routing source as
    match routing destination as
    match interface input
    match interface output
    match flow direction
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last
          
flow record netflow ipv6 as peer:
  Description:        AS aggregation scheme with peer ASs
  No. of users:       0
  Total field space:  29 bytes
  Fields:
    match routing source as peer
    match routing destination as peer
    match interface input
    match interface output
    match flow direction
    collect counter bytes
    collect counter packets
    collect timestamp sys-uptime first
    collect timestamp sys-uptime last

flow record netflow ipv6 assurance:
  Description:        Assurance metrics
  No. of users:       0
  Total field space:  6 bytes
  Fields:
    match ipv6 version
    match ipv6 protocol
    match application name

flow record CUSTOM1:
  Description:        Custom Flow Record For IPv4 Packets
  No. of users:       0
  Total field space:  12 bytes
  Fields:
    match ipv4 destination address
    collect counter bytes
    collect counter packets
```

```
R4#sh run flow record
Current configuration:
!
flow record CUSTOM1
 description Custom Flow Record For IPv4 Packets
 match ipv4 destination address
 collect counter bytes
 collect counter packets
!
```

- Now that a custom flow record has been configured, the flow exporter can be created

- There are a few important steps to complete when building a flow exporter:

    1. Define the flow exporter name

    2. Set a useful description of the flow exporter

    3. Specify the destination of the flow exporter to be used

    4. Specify the NetFlow version to export

    5. Specify the UDP port

- In this instance, the exporter that will be created will point to the 172.16.29.17 host

- This step in the process exports flow data from the device to a netflow collector or management platform such as Cisco DNA Center or Cisco Prime Infrastructure

- Below we can see the configuration of the flow exporter as well as how to verify the configuration

```
conf t
 flow exporter CUSTOM11
  description EXPORT-TO-NETFLOW-COLLECTOR
  destination 172.16.29.17
  export-protocol netflow-v9
  transport UDP 9999
  exit
```

```
R4(config-flow-exporter)#do sh run flow exporter
Current configuration:
!
flow exporter CUSTOM11
 description EXPORT-TO-NETFLOW-COLLECTOR
 destination 172.16.29.17
 transport udp 9999
!
```

```
R4(config-flow-exporter)#do sh flow exporter CUSTOM11
Flow Exporter CUSTOM11:
  Description:              EXPORT-TO-NETFLOW-COLLECTOR
  Export protocol:          NetFlow Version 9
  Transport Configuration:
    Destination IP address: 172.16.29.17
    Source IP address:      10.24.1.4
    Transport Protocol:     UDP
    Destination Port:       9999
    Source Port:            49726
    DSCP:                   0x0
    TTL:                    255
    Output Features:        Not Used
```

- Now that a custom flow exporter called CUSTOM11 has been configured, the flow monitor must be created

- Each flow monitor requires a flow record to be assigned to it

- Each flow monitor has it's own cache, and the flow record provides the layout and how to carve out the cache for the destined traffic defined in the flow record

- The flow monitor can use the predefined flow records or custom flow records

- Below, the CUSTOM1 flow record is used to show the configuration steps

- To configure a flow monitor, the following high-level steps must be taken:

    1. Define the flow monitor name

    2. Set a useful description of the flow monitor

    3. Specify the flow record to be used

    4. Specify a cache timeout of 60 for active connections

    5. Assign the exporter to the monitor

- Configuring the flow monitor is a straight forward task

- The cache timeout tells to the device to export the cache to the collector every 60 seconds

- It is important when creating a flow monitor for the description of the flow monitor to be useful and to map back to the flow record

- Similarly, when you're configuring QoS, it is nice to have the description self-document the intent of what the policy is doing

- This information helps when configuring the flow monitor and when using context-sensitive help, because the description that is configured shows in the output

- Below is shown the configuration of a flow monitor called CUSTOM1

```
conf t
 flow monitor CUSTOM1
  description Uses Custom Flow Record CUSTOM1 for IPv4$
  record ?  CUSTOM1
            netflow
            netflow-original
  record CUSTOM1
  cache timeout active 60
  end
```

```
R4(config)#do sh run flow monitor CUSTOM1
Current configuration:
!
flow monitor CUSTOM1
 description Uses Custom Flow Record CUSTOM1 for IPv4
 cache timeout active 60
 record CUSTOM1
!
```

```
R4#show flow monitor CUSTOM1
Flow Monitor CUSTOM1:
  Description:       Uses Custom Flow Record CUSTOM1 for IPv4
  Flow Record:       CUSTOM1
  Cache:
    Type:                 normal
    Status:               not allocated
    Size:                 4096 entries / 0 bytes
    Inactive Timeout:     15 secs
    Active Timeout:       60 secs
```

- The next step is to map the flow exporter CUSTOM1 to the flow monitor CUSTOM1

- You need to essentially map the two together so that the traffic that is being collected by the flow record can be exported to the NetFlow collector at 172.16.29.17

- Below is shown the process of verification for adding the flow exporter CUSTOM1 to the flow monitor CUSTOM1 on R4

- The output shows the need for detailed and clear descriptions throughout the process

```
conf t
 flow monitor CUSTOM1
  exporter ? CUSTOM1
  exporter CUSTOM1
  end
```

```
R4#show run flow monitor CUSTOM1
Current configuration:
!
flow monitor CUSTOM1
 description Uses Custom Flow Record CUSTOM1 for IPv4
 exporter CUSTOM1
 cache timeout active 60
 record CUSTOM1
!
```

```
R4#show flow monitor CUSTOM1
Flow Monitor CUSTOM1:
  Description:       Uses Custom Flow Record CUSTOM1 for IPv4
  Flow Record:       CUSTOM1
  Flow Exporter:     CUSTOM1 (inactive)
  Cache:
    Type:                 normal
    Status:               not allocated
    Size:                 4096 entries / 0 bytes
    Inactive Timeout:     15 secs
    Active Timeout:       60 secs
```

- The final step necessary in enabling Flexible NetFlow is to apply the flow monitor to the interfaces

- This step turns on the collection of NetFlow statistics, and it can be enabled for ingress, or egress or both

- This scenario highlights the ingress option, using the `ip flow monitor CUSTOM1 input` command on the desired interfaces

- Below is illustrated the process as well as how to verify that Flexible NetFlow is working by issuing the command `show flow monitor CUSTOM1 cache`

```
conf t
 interface range g0/0 - 1
  ip flow monitor CUSTOM1 input
```

```
R4#show flow monitor CUSTOM1 cache
  Cache type:                               Normal
  Cache size:                                 4096
  Current entries:                               1
  High Watermark:                                1

  Flows added:                                   4
  Flows aged:                                    3
    - Active timeout      (    60 secs)          0
    - Inactive timeout    (    15 secs)          3
    - Event aged                                 0
    - Watermark aged                             0
    - Emergency aged                             0

IPV4 DST ADDR         bytes        pkts
===============  ==========  ==========
10.24.1.4                59           1

```

- The modularity of Flexible NetFlow makes the tool much more scalable and powerful than traditional NetFlow

- Having the ability to export to multiple destinations or collectors as well as having the ability of using the tool for security forensics to identify DoS attacks and worm propagation is tremendous

- Although quite a few steps are involved in enabling Flexible NetFlow, the process is easily replicable, so network engineers can easily create traffic analysis to meet the individual needs of the businesses or multiple departments within the same organization

Flow record
    |
    |
Flow exporter
    |
    |
Flow monitor (unite it with the record and exporter)
    |
    |
Apply to inferfaces (input/output/both)
