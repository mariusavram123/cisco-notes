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
