## IP SLA configuration - set one node as responder and the other to send traffic to measure network performance

- See ip-sla-topology.png for the topology

- R2 is set as responder

```
conf t
ip sla responder
exit

show ip sla responder

```

- R1 - set IP SLA operation to send packets similar to VoIP traffic

```
ip sla 1
 # udp-jitter <responder ip> <codec codec_type> <codec_size codec_size> 
 udp-jitter 203.0.113.2 16384 codec g729a codec-size 20
 tos 184 # decimal value for 8-bit DSCP+ECN byte
 frequency 5
 exit

ip sla schedule 1 start-time now life forever

show ip sla statistics
```

- Influencing IP routing with IP SLA - R1

- See ip-sla-topology2.png for the topology information - threshold is in miliseconds

```
conf t
ip sla 2
 icmp-echo 203.0.113.5 source-ip 192.0.2.1 
  frequency 5
  threshold 100
  exit
ip sla schedule 2 life forever start-time now

track 2 ip sla 2 
 delay down 10 up 10
 
ip route 198.51.100.0 255.255.255.0 203.0.113.5 track 2 # current route used only if track object 2 is up

ip route 198.51.100.0 255.255.255.0 203.0.113.1 2

show track 2
```

- Redefine an ip sla operation - R1

```
no ip sla 2

ip sla 2
 icmp-echo 203.0.113.5 source-ip 192.0.2.1
  frequency 5
  threshold 1
  exit
ip sla schedule 2 life forever start-time now
```

