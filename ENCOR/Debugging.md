## Debugging

- Debugging can be a powerfull part of troubleshooting complex issues on a network

- Debugging is also informational

- Here we will see some basic OSPF debugging examples and see how to use debugging when trying to narrow down issues in a network

- One of the most common use case for debugging is when there is a need to see things at a deeper level (such as when routing protocols are having adjacency issues)

- There is a normal flow that is taken from a troubleshooting perspective, depending on the routing protocol

- However, there are times when these steps have been taken, and the issue is not evident

- With OSPF for example, when you're troubleshooting adjacency issues, it is very helpful to have debugging experience

- Using the simple topology shown below, debugging is used to fix a couple of issues in the OSPF area 0

![debugging-topology](./debugging-topology.png)

- Some of the common OSPF adjacency issues can be resolved by using debugging:

    - MTU issues

    - Incorrect interface types

    - Improperly configured network mask

- From the output of the `show ip ospf neighbor` command on R1, it can be seen that the neighbor adjacency to R4 is in the INIT state

- It can be seen that the neighbor adjacency to R4 is in INIT state

- If the command is run after a few seconds, the state changes to EXCHANGE but quickly cycles back to the INIT state when the command is run again

```
R1#show ip ospf neighbor 

Neighbor ID     Pri   State           Dead Time   Address         Interface
7.7.7.7           1   FULL/BDR        00:00:36    192.168.17.7    Ethernet0/2
4.4.4.4           1   INIT/BDR        00:00:36    192.168.14.4    Ethernet0/1
2.2.2.2           1   FULL/BDR        00:00:37    192.168.12.2    Ethernet0/0
```

```
R1#show ip ospf neighbor 

Neighbor ID     Pri   State           Dead Time   Address         Interface
7.7.7.7           1   FULL/BDR        00:00:32    192.168.17.7    Ethernet0/2
4.4.4.4           1   EXCHANGE/BDR    00:00:38    192.168.14.4    Ethernet0/1
2.2.2.2           1   FULL/BDR        00:00:36    192.168.12.2    Ethernet0/0
```

```
R1#show ip ospf neighbor 

Neighbor ID     Pri   State           Dead Time   Address         Interface
7.7.7.7           1   FULL/BDR        00:00:36    192.168.17.7    Ethernet0/2
4.4.4.4           1   INIT/BDR        00:00:36    192.168.14.4    Ethernet0/1
2.2.2.2           1   FULL/BDR        00:00:37    192.168.12.2    Ethernet0/0
```

- A typical aproach to this line of troubleshooting is to log in to both devices and look at the logs or the running configuration

- Although this approach may reveal the issue at hand, it may not be the most efficient way to troubleshoot

- For example, a considerable amount of time is needed to log in to multiple devices and start combining through the configurations to see what may be missing or misconfigured

- Below, debugging is used on R1 to try to determine what the issue is

- Below is shown the output after the `debug ip ospf adj` command is issued

```
*Oct 25 19:24:13.559: OSPF-1 ADJ   Et0/1: Rcv DBD from 4.4.4.4 seq 0x2424 opt 0x52 flag 0x7 len 32  mtu 1300 state EXCHANGE
*Oct 25 19:24:13.559: OSPF-1 ADJ   Et0/1: Nbr 4.4.4.4 has smaller interface MTU
*Oct 25 19:24:13.559: OSPF-1 ADJ   Et0/1: Send DBD to 4.4.4.4 seq 0x2424 opt 0x52 flag 0x2 len 132
```

- This command is used to reveal messages that are exchanged during the OSPF adjacency process

- With one `debug` command, it was easy to determine the root cause of the failed adjacency

- The output of the `debug ip ospf adj` command on R1 clearly states that it received a Database Descriptor (DBD) packet from neighbor 4.4.4.4, and that the neighbor 4.4.4.4 has a smaller interface MTU of 1300

- If the same `debug` command were run on R4, the output would be similar but show the reverse

- Below is shown the output after the command `debug ip ospf adj` on R4

```
*Oct 25 19:38:46.135: OSPF-1 ADJ   Et0/0: Send DBD to 1.1.1.1 seq 0x15F opt 0x52 flag 0x7 len 32
*Oct 25 19:38:46.135: OSPF-1 ADJ   Et0/0: Retransmitting DBD to 1.1.1.1 [5]
*Oct 25 19:38:46.136: OSPF-1 ADJ   Et0/0: Rcv DBD from 1.1.1.1 seq 0x15F opt 0x52 flag 0x2 len 132  mtu 1500 state EXSTART
*Oct 25 19:38:46.136: OSPF-1 ADJ   Et0/0: Nbr 1.1.1.1 has larger interface MTU
```

- The output of the `debug` command shwos that R1 has an MTU size of 1500, which is larger that the locally configured MTU of 1300 on R4

- This is a really quick way of troubleshooting this type of issue with adjacency formation

- The second issue to cover with adjacency formation is OSPF network type mismatch, which is a common reason for neighbor adjacency issues

- Often this is simply a misconfiguration issue when setting up the network

- When the `debug ip ospf hello` command is used on R1, everything appears to be normal

- Hellos are sent to the multicast group 224.0.0.5 every 10 seconds

- Examples of the output of the command on R1:

```
R1#debug ip ospf hello 
OSPF hello debugging is on
R1#
*Oct 25 19:57:40.311: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
R1#
*Oct 25 19:57:43.760: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
R1#
*Oct 25 19:57:45.065: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
R1#
*Oct 25 19:57:46.673: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 25 19:57:47.178: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 25 19:57:47.240: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
R1#
*Oct 25 19:57:49.964: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
R1#
*Oct 25 19:57:53.150: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
R1#
*Oct 25 19:57:54.934: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
R1#
*Oct 25 19:57:56.378: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 25 19:57:56.459: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 25 19:57:56.960: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
R1#un all
All possible debugging has been turned off
```

- However, the situation is different if you issue the same `debug` command on R4

- Below is the output of the `debug` command on R4

```
*Oct 25 20:02:44.727: OSPF-1 HELLO Et0/0: Rcv hello from 1.1.1.1 area 0 192.168.14.1
*Oct 25 20:02:44.727: OSPF-1 HELLO Et0/0: Mismatched hello parameters from 192.168.14.1
*Oct 25 20:02:44.727: OSPF-1 HELLO Et0/0: Dead R 40 C 120, Hello R 10 C 30
R4(config-if)#
*Oct 25 20:02:53.714: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.14.4
*Oct 25 20:02:53.916: OSPF-1 HELLO Et0/0: Rcv hello from 1.1.1.1 area 0 192.168.14.1
*Oct 25 20:02:53.916: OSPF-1 HELLO Et0/0: Mismatched hello parameters from 192.168.14.1
*Oct 25 20:02:53.916: OSPF-1 HELLO Et0/0: Dead R 40 C 120, Hello R 10 C 30
R4(config-if)#
*Oct 25 20:02:55.750: %OSPF-5-ADJCHG: Process 1, Nbr 1.1.1.1 on Ethernet0/0 from FULL to DOWN, Neighbor Down: Dead timer expired
```

- Based on the output you can see that the hello parameters are mismatched

- The output shows that R4 is receiving a dead interval of 40, while it has a configured dead interval of 120

- You can also see that the hello interval R4 is receiving is 10, and the configured hello interval is 30

- By default, the dead interval is 4 times the hello interval

- Different network types have different hello intervals and dead intervals

