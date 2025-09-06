### Modular QoS CLI

- Modular QoS CLI (MQC) is Cisco's approach to implementing QoS on Cisco routers

- MQC provides a modular CLI framework to create QoS policies that are used to perform traffic classification and QoS actions such as marking, policing, shaping, congestion management, and congestion avoidance

- MQC policies are implemented using the following MQC components:

    - **Class maps**: These maps define traffic classification criteria by identifying the type of traffic that need QoS treatment (for example, matching voice traffic)

    - Multiple class maps are usually required to identify all the different types of traffic that need to be classified

    - Class maps are defined as follows:

    ```
    conf t
     class-map [match-any | match-all] <class-map-name>
    ```

    - Each class-map can include one or more `match` command statements within it for traffic classification

    - **Policy maps**: These maps provide QoS actions for each traffic class defined by the class maps

    - Each policy mode can include one or more traffic classes, and each traffic class can have one or more QoS actions

    - Policy maps are configured as follows:

    ```
    conf t
     policy-map <name>
    ```

    - **Service policies**: These policies are used to apply policy maps to interfaces in an inbound and/or outbound direction

    - Service polices can be applied as follows:

    ```
    conf t
     interface <name>
      service-policy {input | output} <policy-map-name>
    ```

    - The same policies can be reused on multiple interfaces

- A policy map consists of two main elements:

    - A traffic class to classify traffic, identified with the `class <class-map-name>` command

    - The QoS actions to apply to the traffic that matches the traffic class

- Because policy maps use traffic classes to apply QoS actions, QoS actions applied using MQC, are referred to as *class-based QoS actions*

- The following class-based QoS actions supported by MQC can be applied to traffic matching a traffic class:

    - Class-based weighted fair quewing (CBWFQ)

    - Class-based policing

    - Class-based shaping

    - Class-based marking

- All traffic that is not matched by any of the user-defined traffic classes within the policy map is referred to as unclassified traffic

- Unclassified traffic is matched by an implicitly configured default class called class-default

- Unclassified traffic is typically best-effort traffic that requires no QoS guarantees; however class-based QoS actions can also be applied to the default class if necessary

- Policy maps have no effect until they are applied to an interface in an outbound or inbound direction as follows:

```
conf t
 interface <name>
  service-policy [inbound | outbound] <policy-map-name>
```

- Service policies can be used to apply the same policy map to multiple interfaces

- They can also be used to apply a single inbound and/or a single outbound policy map to a single interface

- An example of the MQC framework:

1. Identify interesting traffic:

```
conf t
 ip access-list extended VOICE-TRAFFIC
  10 permit udp any any range 16384 32767
  20 permit udp any range 16385 32767 any
```

2. Define traffic classification criteria:

```
conf t
 class-map match-all VOIP-TELEPHONY
  match access-group name VOICE-TRAFFIC

 class-map match-any P2P
  match protocol bittorrent
  match protocol soulseek
```

3. Perform QoS actions for each traffic class:

```
conf t
 policy-map QUEUING
  class VOIP-TELEPHONY
   priority level 1 percent 30

  class P2P
   bandwidth percent 10

  class class-default
```

4. Apply policy map to the interface:

```
conf t
 interface ge1
  service-policy output QUEUING
```

- The class map and policy map names are case sensitive

- Making the name all uppercase characters is a best practice and makes it easier to read in the configuration

- Policy maps can be applied to an interface, but policy maps can also be applied to other policies (also referred to as parent policies) to create hierarchical QoS policy maps (also referred to as nested policy maps)

- The `service-policy <policy-map>` command is applied using a child policy map inside a parent policy map

- Below, a policy map called CHILD-POLICY is applied to the default class of an another policy map called PARENT-POLICY using the `service-policy <policy-map>` command:

1. Child policy:

```
conf t
 policy-map CHILD-POLICY
  class VOIP-TELEPHONY
   priority percent 35
```

2. Child policy applied to parent policy:

```
conf t
 policy-map PARENT-POLICY
  class class-default
   service-policy CHILD-POLICY
```

3. Parent policy applied to interface:

```
conf t 
 interface g1
  service-policy output PARENT-POLICY
```

### MQC Classification Configuration

- Traffic classification using MQC is performed by using the `match` command within `class-map` configuration mode:

```
conf t
 class-map <name>
  match <access-list> ...
```

- If the traffic being classified matches the condition specified by the `match` command then the condition returns a match result, and a no match result if it doesn't match

- The match command within a `class-map` has the following characteristics:

    - It matches on the packet characteristics such as COS, DSCP or ACLs (source/destination) networks and ports

    - If no `match` command is specified within the class map, `match none` is the default value

    - The `match all` command within a class map matches all packets

    - The `match protocol` command within a class map is used for NBAR classification

- Where then is more than one `match` command within a class map, the two matching options in the `class-map [match-any | match-all] <class-map-name>` are used to determine the matching criteria:

    - **Match any**: Logical OR operation: At least one of the match conditions within the class map must be met. This option is configured with:

    ```
    conf t
     class-map match-any <class-map-name>
    ```

    - **Match all**: Logical AND operation: All match conditions within the class map must be met. Match all is the default matching behaviour when the `class-map match-any` command is not specified. It can also be explicitly configured as follows:

    ```
    conf t
     class-map match-any <class-map-name>
    ```

- Most popular match command used with MQC for traffic classification:

```
Command                                                         Description

match access-group {acl-number} | name {acl-name}               Match an ACL by number or name

match any                                                       Match any packet

match cos {cos-value-list}                                      Match one of the specified Layer 2 COS values in a frame
                                                                Up to 8 different COS values can be specified in the list

match [ip] dscp {dcsp-value-list}                               With the optional `ip` keyword it matches one of the specified DSCP values in IPv4 packets
                                                                Without the optional `ip` keyword, it matches one of the specified DSCP values in IPv4 and IPv6 packets
                                                                Up to eight different DSCP values can be specified in the list

match [ip] precedence                                           With the optional `ip` keyword, it matches one of the specified IP Precedence values in IPv4 packets
                                                                Without the optional `ip` keyword it matches one of the specified Precedence values in IPv4 and IPv6 packets
                                                                Up to four different IP precedence values can be specified in the list

match ip rtp <start-port-number port-number-range>              Matches any specified RTP port number in the specified range

match protocol <protocol-name>                                  Matches the specified NBAR protocol name

match qos-group <qos-group-value>                               Matches the specified QoS group value. Only one QoS group value can be specified

match protocol http [url <url-string> | host <hostname-string>| Matches HTTP traffic to URL, hostname, or MIME type
mime <MIME-type>]

match protocol rtp [audio|video|payload-type <payload-string>]  Matches RTP based on audio or video payload type or a more granular payload type

match protocol <peer-to-peer-application>                       Matches peer-to-peer (P2P) applications such as Soulseek, BitTorrent and Skype
```

- Below we can see multiple class maps, each with different match commands

- The VOIP-TELEPHONY class-map is configured with match-all (logical AND operation) and the CONTROL class map with match-any (logical OR operation)

- For the VOIP-TELEPHONY class map to be be matched, the packet being evaluated should include a DSCP marking of AF and should also be permitted by the VOICE-TRAFFIC ACL

- For the CONTROL class map to be matched, the packet being evaluated should match any of the specified DSCP values in the list or be permitted by the CALL-CONTROL ACL

- the class-maps with the `match protocol` command show how traffic can be classified using NBAR2:

```
conf t
 ip access-list extended VOICE-TRAFFIC
  10 permit udp any any range 16384 32767
  20 permit udp any range 16384 32767 any

 ip access-list extended CALL-CONTROL
  10 permit tcp any any eq 1719
  20 permit tcp any eq 1719 any
  30 permit udp any any eq 5060
  40 permit udp any eq 5060 any
  50 permit tcp any any eq 5060
  60 permit tcp any eq 5060 any

 class-map match-all VOIP-TELEPHONY
  match dscp ef
  match access-group name VOICE-TRAFFIC

 class-map match-any CONTROL
  match dscp cs3 af31 af32 af33
  match access-group name CALL-CONTROL

 class-map match-any HTTP-VIDEO
  match protocol http mime "video/*"

 class-map match-any P2P
  match protocol bittorrent
  match protocol skype

 class-map match-all RTP-AUDIO
  match protocol rtp audio

 class-map match-all HTTP-WEB-IMAGES
  match protocol http url "*.jpeg|*.jpg"
```

- Verifying configured class-maps:

```
R2(config)#do sh class-map
 Class Map match-any class-default (id 0)
   Match any 

 Class Map match-all RTP-AUDIO (id 6)
   Match protocol rtp audio 

 Class Map match-any P2P (id 5)
   Match protocol bittorrent
   Match protocol skype

 Class Map match-any CONTROL (id 3)
   Match   dscp cs3 (24) af31 (26) af32 (28) af33 (30)
   Match access-group name CALL-CONTROL

 Class Map match-all HTTP-WEB-IMAGES (id 7)
   Match protocol http url "*.jpeg|*.jpg"

 Class Map match-all VOIP-TRAFFIC (id 2)
   Match   dscp ef (46)
   Match access-group name VOICE-TRAFFIC

 Class Map match-any HTTP-VIDEO (id 4)
   Match protocol http mime "video/*"
```

### Class-Based Marking Configuration

- Class-based marking using the MQC can be achieved using two ways:

    - Using the `set` command under a traffic class of a policy map

    - Marking traffic that has exceeded a configured threshold with the `police` command in a policy map

- Class-based marking using the `set` command option:

- List of the `set` commands that are used for class-based marking configuration

- Multiple `set` commands are supported under a single traffic class

```
Command                                                             Description

set qos-group <qos-group-id>                                        Marks the classified traffic with an internal QoS group ID

set cos <cos-value>                                                 Marks the Layer 2 COS value

set [ip] precedence <ip-precedence-value>                           Marks the Precedence value for IPv4 and IPv6 packets

set [ip] dscp <ip-dscp-value>                                       Marks the DSCP value for IPv4 and IPv6 packets
```

- Inbound policy map config using the `set` command to perform ingress traffic marking:

```
conf t
 policy-map INBOUND-MARKING-POLICY
  class VOIP-TRAFFIC
   set dscp ef

  class VIDEO
   set dscp af31

  class CONFERENCING
   set dscp af41
   set cos 4

  class class-default
   set dscp default
   set cos 0
```

- Viewing the policy map configuration (with adjustments to already existing classes):

```
R2(config-pmap-c)#do sh policy-map
  Policy Map INBOUND-MARKING-POLICY
    Class VOIP-TRAFFIC
      set dscp ef
    Class HTTP-VIDEO
      set dscp af31
    Class CONTROL
      set dscp af41
      set cos 4
    Class class-default
      set cos 0
      set dscp default
```

### Class-Based Policing Configuration

- The `police` command under a traffic class of a policy map is used for class-based policing

- With class-based policing, the classified input or output traffic can be rate-limited, marked or dropped

- The `police` command syntax is as follows:

```
conf t
 policy-map <name>
  class-map <class-name>
   police cir <cir-in-bps> [bc] <commited-burst-size-in-bytes>
                           [be] <excess-burst-size-in-bytes> [conform-action <action>] [exceed-action <action>] [violate-action <action>]
```

- Police command keywords and their description:

```
Command                                                         Description

cir                                                             Optional keyword to explicitly specify the average CIR rate

<cir-in-bps>                                                    Average CIR rate in bits per second
                                                                The CIR can be configured with the postfix values k (Kbps), m (Mbps) and g (Gbps)
                                                                The postfix values support decimal points
bc                                                              Optional keyword to explicitly specify the committed burst size
<commited-burst-size-in-bytes>                                  Optional BC size in bytes. The default is 1500 bytes or the configured CIR rate divided by 32
                                                                (CIR/32); whichever number is higher is chosen as the BC size
be                                                              Optional keyword to explicitly specify the excess burst Be size
<excess-burst-size-in-bytes>                                    Optional Be size in bytes. The default is the value of the Be
**conform-action**                                              Optional keyword to specify the action to take on packets that conform to the CIR. The default action is to transmit
**exceed-action**                                               Optional keyword to specify the action to take on packets that exceed the CIR. The default action is to drop
**violate-action**                                              Optional keyword used to specify the action to take on packets that violate the normal and maximum burst sizes. The default action is to drop.
<action>                                                        The action to take on packets. Some examples include:
                                                                drop: Drops the packet (default for exceed and violate actions)
                                                                transmit: Transmits the packet (default for conform action)
                                                                set-dscp-transmit dscp-value: Marks and transmits the packet with the specified dscp value
                                                                set-prec-transmit prec-value: Marks and transmits the packet with the specified Precedence value
                                                                set-cos-transmit cos-value: Marks and transmits the packet with the specified cos value
                                                                set-qos-transmit qos-group-value: Marks the packet with the specified internal qos-group value
                                                                This option is valid only on inbound policy maps

```

- Configuration of a **single-rate two-color policy map with two traffic classes**

- Traffic matching the VOIP-TELEPHONY traffic class is being policed to a CIR of 50 Mbps, and traffic matching the VIDEO class is being policed to 25 Mbps

- Traffic for both classes that conforms to the CIR is transmitted, exceeding traffic for VOIP-TELEPHONY traffic class is dropped, and exceeding traffic for the VIDEO class is marked down and transmitted with the DSCP value of AF21

```
conf t
 policy-map OUTBOUND-POLICY
  class VOIP-TELEPHONY
   police 50000000 conform-action transmit exceed-action drop

  class VIDEO
   police 25000000 conform-action transmit exceed-action set-dscp-transmit af21

 interface gi1
  service-policy output OUTBOUND-POLICY 
```

- Above the be, bc. and cir keywords were not specified with the `police` command.

- To see the default values:

```
R2#show policy-map OUTBOUND-POLICY
  Policy Map OUTBOUND-POLICY
    Class VOIP-TELEPHONY
     police cir 50000000 bc 1562500
       conform-action transmit 
       exceed-action drop 
    Class VIDEO
     police cir 25000000 bc 781250
       conform-action transmit 
       exceed-action set-dscp-transmit af21
```

- For the VOIP telephony class, the Bc default value is 50.000.000/32 (=1562500), and for VIDEO class the default Bc value is 25.000.000/32 (=781250)

- There is no Be, because single-rate two-color markers/policers (single token bucket algorithms) do not allow excess bursting

- The configuratiom of a **single-rate three-color policy map with one traffic class**

- Traffic matching the VOIP-TELEPHONY traffic class is policed to a CIR of 50 Mbps; traffic that conforms to the CIR is remarked and transmitted with DSCP AF31

- Exceeding traffic is marked down and transmitted with DSCP AF32, and all violating traffic is dropped

```
conf t 
 policy-map OUTBOUND-POLICY
  class VOIP-TELEPHONY
   police 50000000 conform-action set-dscp-transmit af31 exceed-action set-dscp-transmit af32 violate-action drop

 interface gi1
  service-policy output OUTBOUND-POLICY
```

- Verifying the policy:

```
R2#show policy-map OUTBOUND-POLICY
  Policy Map OUTBOUND-POLICY
    Class VOIP-TELEPHONY
     police cir 50000000 bc 1562500 be 1562500
       conform-action set-dscp-transmit af31
       exceed-action set-dscp-transmit af32
       violate-action drop 
    Class VIDEO
     police cir 25000000 bc 781250
       conform-action transmit 
       exceed-action set-dscp-transmit af21
R2#
```

- From the above output, for the VOIP-TELEPHONY class, the Bc and Be values were not specified; therefore the default Bc value is 50.000.000/32 (=1562500) and Be value defaults to the Bc value

- The configuration of a **two-rate three-color policy**:

- In addition to the CIR, the PIR needs to be specified as follows:

```
conf t
 policy-map <name>
  class <name>
   police [cir] <cir-in-bps> [bc] <commited-burst-size-in-bytes> pir <pir-in-bps>
                             [be] <excess-burst-size-in-bytes> [conform-action <action>]
                             [exceed-action <action>] [violate-action <action>]
```

- If Bc is not specified in the `police` command the default is 1500 bytes or the configured CIR rate divided by 32 (CIR/32); whichever number is higher is chosen as the Bc size

- If Be is not specified, the default of 1500 bytes or the configured PIR rate divided by 32 (PIR/32); whichever number is higher is chosen as the Be size

- Configuration of a two-rate three-color (trTCM) policy map one traffic class is below

- For trTCM policies the violate action is checked first; therefore, traffic that exceeds the CIR of 50 Mbps is marked down and transmitted with DSCP AF31, and traffic that conforms to the CIR is transmitted as is

```
conf t
 policy-map OUTBOUND-POLICY
  class VOIP-TELEPHONY
   police cir 50000000 pir 100000000 conform-action transmit  exceed-action set-dscp-transmit af31 violate-action drop

 interface gi1
  service-policy output OUTBOUND-POLICY
```

- Viewing the policy map:

```
R2(config-pmap-c)#do sh policy-map OUTBOUND-POLICY
  Policy Map OUTBOUND-POLICY
    Class VOIP-TELEPHONY
     police cir 50000000 bc 1562500 pir 100000000 be 3125000
       conform-action transmit 
       exceed-action set-dscp-transmit af31
       violate-action drop 
    Class VIDEO
     police cir 25000000 bc 781250
       conform-action transmit 
       exceed-action set-dscp-transmit af21
```

- For the VOIP-TELEPHONY class, the Bc value was not specified; therefore the default value is 50.000.000/32 (=1562500bytes)

- The Be value was also not specified; therefore, the default Be value is 100.000.000/32 (=3125000)

### CBWFQ Configuration

- With CBWFQ, each traffic class in a policy map can perform queuing actions; therefore a traffic class with queuing actions is functionally behaving like a queue

- The `priority`, `bandwidth` and `shape` commands are queuing (congestion management) actions that enable queuing for a class

- The `bandwidth` and `shape` commands can be used together in the same class to provide a minimum bandwidth guarantee using the `bandwidth` command, and a maximum bandwidth based on the mean rate of the `shape` command

- CBWFQ commands and their description (these may not be supported by all platforms - check Cisco documentation):

```
Command                                                                 Description

priority                                                                Enables LLQ strict priority queuing. With this method it is recommended to configure
                                                                        an explicit policer with the police command to rate-limit the priority traffic,
                                                                        otherwise, the other queues can be starved of bandwidth
priority [police-rate-in-kbps] [burst-in-bytes]                         Enables LLQ strict priority queuing with a conditional policing rate in kbps
                                                                        Policing is in effect only during times of congestion
priority percent [police-rate-in-percentage] [burst-in-bytes]           Enables LLQ strict priority queuing with a conditional policing rate calculated as
                                                                        a percentage of the interface bandwidth, or the shaping rate in an hierarchical policy
                                                                        Policing is in effect only during times of congestion
priority level [1 | 2]                                                  Multilevel strict priority. With this method it is recommended to configure an
                                                                        explicit policer with the police command to rate-limit the priority traffic,
                                                                        otherwise, the other queues can be starved of bandwidth
priority level [1 | 2] <police-rate-in-kbps> [burst-in-bytes]           Multilevel strict priority with policing rate in kbps
                                                                        Policing is in effect only during times of congestion
priority level [1 | 2] <police-rate-in-percenatge> [burst-in-bytes]     Multilevel strict priority with the policing rate calculated as a percentage of the
                                                                        interface bandwidth or the shaping rate in a hierarchical policy
                                                                        Policing is in effect only during times of congestion
bandwidth <bandwidth-kbps>                                              Minimum bandwidth guarantee, in kilobytes per second assigned to the class
bandwidth remaining percent <percent>                                   Minimum bandwidth guarantee based on a relative percent of the available bandwidth
bandwidth remaining ratio <ratio>                                       Minimum bandwidth guarantee based on a relative ratio of the available bandwidth
bandwidth percent <percentage>                                          Minimum bandwidth guarantee based on an absolute percent of the interface bandwidth
                                                                        or the shaping rate in an hierarchical policy
fair-queue                                                              Enables flow-based queuing to manage multiple flows contending for a single queue

shape [average | peak] <mean-rate-in-bps> [commited-burst-size]         Enables class-based traffic shaping
[excess-burst-size]                                                     Average shaping is used to forward packets at the configured mean-rate and allows bursting
                                                                        up to the Bc at every Tc, and up to Be when extra tokens are available
                                                                        This is the most used shaping method
                                                                        Peak shaping is used to forward packets at the mean rate multiplied by (1 + Be/Bc) at
                                                                        every Tc. This method is not commonly used
                                                                        The mean rate can be configured with the postfix values k (kbps), m (Mbps), and g (Gbps)
                                                                        The postfix values support decimal points
                                                                        It is recommended to use the Bc and Be default values
```

- The `queue-limit` and `random-detect` commands are used for CBWFQ congestion avoidance (queue management) actions

- Commands and description:

```
Commands                                                                Description

queue-limit <queue-limit-size> [cos <cos-value> | dscp <dscp-value>     Tail drop is the default dropping mechanism for every class
| precedence-value] [percent <percentage-of-packers>]                   The queue-limit command is used in case there is a need to change the default
                                                                        tail drop values
random-detect [dscp-based|precedence-based|cos-based]                   This command enables WRED. The precedence-based option is the default
                                                                        It is recommended to use dscp-based when using dscp for classification
                                                                        It is also recommended to use the default minimum threshold, maximum threshold and drop probability values
```

- Guidelines that should be considered when configuring queuing policies:

    - The `random-detect` and `fair-queue` commands require the `bandwidth` or `shape` commands to be present in the same user-defined class

    - This is not applicable to the default class

    - The `queue-limit` command requires the `bandwidth`, `shape` or `priority` commands to be present in the same user-defined class

    - This is not applicable to the default class

    - The `random-detect`, `shape`, `fair-queue`, and `bandwidth` commands cannot coexist with the `priority` command on the same class

    - The `bandwidth <bandwidth-kbps>` or `bandwidth percent` commands cannot coexist in the same policy map with strict priority queues configured with the `priority` or `priority level <1|2>` commands, unless the strict priority queues are being policed with the `police` command

    - The `bandwidth remaining percent` command can coexist with the `priority` or `priority level <1|2>` commands in the same policy map

    - Mixed `bandwidth` command types are not supported in a policy map. They all need to be consistent across all the classes in a policy map

    - The `priority percent <police-rate-in-percentage>` or `priority level {1 | 2} percent <police-rate-in-percentage>` commands do not support an explicit policer configured with the `police` command

    - The sum total of all class bandwidths should not exceed 100%

    - Class-based traffic shaping is supported only in an outbound direction

- Below is a policy with multiple queuing classes configured 

- The VOIP and VIDEO classes are using multilevel priority policing, where they are each guaranteed a minimum bandwidth of 30% of the interface bandwidth 

- The CRITICAL and class-default classes are guaranteed a minimum bandwidth of 10%, the TRANSACTIONAL class a bandwidth of 15 % and for the SCAVENGER class, a bandwidth of 5 %

- If the available bandwidth for the interface where the policy is applied is 1 Gbps, under congestion the VOIP and VIDEO traffic classes would each get a guaranteed minimum bandwidth of 300 Mbps (30% each), the CRITICAL and class-default classes would each get 100 Mbps (10% each), the TRANSACTIONAL class would get 150 Mbps (15%), and the SCAVENGER class would get 50 Mbps (5%)

```
conf t
 policy-map QUEUING
  class VOIP
   priority level 1 percent 30
  class VIDEO
   priority level 2 percent 30
  class CRITICAL
   bandwidth percent 10
  class SCAVENGER
   bandwidth percent 5
  class TRANSACTIONAL
   bandwidth percent 15
  class class-default
   bandwidth percent 10
   fair-queue
   random-detect dscp-based
   queue-limit 64

 interface gi1
  service-policy output QUEUING
```

- Viewing the policy:

```
R1#show policy-map QUEUING
  Policy Map QUEUING
    Class VOIP
      priority level 1 30 (%)
    Class VIDEO
      priority level 2 30 (%)
    Class CRITICAL
      bandwidth 10 (%)
    Class SCAVENGER
      bandwidth 5 (%)
    Class TRANSACTIONAL
      bandwidth 15 (%)
    Class class-default
      bandwidth 10 (%)
      fair-queue
       packet-based wred, exponential weight 9
      
      dscp    min-threshold    max-threshold    mark-probablity
      ----------------------------------------------------------
      default (0)   -                -                1/10
      queue-limit 64 packets
```

- Below is a similar policy. The difference is that in this new policy, the strict priority queues are not being policed (they are unconstrained)

- When strict priority queues are unconstrained, the rest of the clases/queues cannot be guaranteed a specific minimum bandwidth, and for this reason the `bandwidth <bandwidth-kbps>` or `bandwidth percent` commands

- The `bandwidth remaining {percent <percentage> | ratio <ratio>}` command can be used for this use case since it automatically adjusts to the relative percentage or ratio of the remaining bandwidth

- For example let's assume that the VOIP and VIDEO classes are using 800 Mbps out of the available 1 Gbps for the interface

- That would leave 200 Mbps for the remaining classes

- The CRITICAL class would get 80 Mbps (40 % of 200 Mbps), and the rest of the classses would get 40 Mbps each (20 % of 200 Mbps)

```
conf t
 policy-map QUEUING
  class VOIP
   priority level 1
  class VIDEO
   priority level 2
  class CRITICAL
   bandwidth remaining percent 40
  class SCAVENGER
   bandwidth remaining percent 20
  class TRANSACTIONAL
   bandwidth remaining percent 20
  class class-default
   bandwidth remaining percent 20
   fair-queue
   random-detect dscp-based
   queue-limit 64


 interface gi1
  service-policy output QUEUING
```

- Let's assume that the outbound traffic of the 1Gbps interface from above needs to be shaped to 100 Mbps to conform to the SLA of the SP, while keeping all the configuration of the QUEUING policy map intact

- This can be achieved with class-based shaping in a hierarchical QoS policy

- Below we can see the QUEUING policy applied as a child policy under the SHAPING parent policy

- The SHAPING parent policy shapes all traffic to 100 Mbps

- For this case, the QUEUING policy does not use the interface bandwidth of 1 Gbps as a reference for it's queue bandwidth calculations; instead, it uses the mean rate of the traffic shaping policy which is 100 Mbps

- For example, let's assume that the VOIP and VIDEO classes are using 80 Mbps out of the available 100 Mbps

- That would leave 20 Mbps for the remaining classes

- The CRITICAL class would get 8 Mbps (40 % of 20 Mbps), and the remaining three classes would each get 4 Mbps (20% of 20 Mbps)

```
conf t
 policy-map SHAPING
  class class-default
   shape average 100000000
   service-policy QUEUING

 interface gi1
  service-policy output SHAPING
```

- Viewing the policies:

```
R1#sh policy-map SHAPING
  Policy Map SHAPING
    Class class-default
      Average Rate Traffic Shaping
      cir 100000000 (bps)   
      service-policy QUEUING
R1#sh policy-map QUEUING
  Policy Map QUEUING
    Class VOIP
      priority level 1 30 (%)
    Class VIDEO
      priority level 2 30 (%)
    Class CRITICAL
      bandwidth 10 (%)
    Class SCAVENGER
      bandwidth 5 (%)
    Class TRANSACTIONAL
      bandwidth 15 (%)
    Class class-default
      bandwidth 10 (%)
      fair-queue
       packet-based wred, exponential weight 9
      
      dscp    min-threshold    max-threshold    mark-probablity
      ----------------------------------------------------------
      default (0)   -                -                1/10
      queue-limit 64 packets
```

- IOL platform support bandwidth remaining percent commands, IOSv does not

```
R3#show policy-map QUEUING
  Policy Map QUEUING
    Class VOIP
      priority level 1
    Class VIDEO
      priority level 2
    Class CRITICAL
      bandwidth remaining 40 (%)
    Class SCAVENGER
      bandwidth remaining 20 (%)
    Class TRANSACTIONAL
      bandwidth remaining 20 (%)
    Class class-default
      bandwidth remaining 20 (%)
R3#show policy-map SHAPING
  Policy Map SHAPING
    Class class-default
      Average Rate Traffic Shaping
      cir 100000000 (bps)   
      service-policy QUEUING
```
