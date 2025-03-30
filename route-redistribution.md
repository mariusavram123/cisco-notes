## Route redistribution between different routing protocols

- Seed metric -default metric assigned for a routing protocol routes advertised into this routing protocol by another routing protocol

    - EIGRP - seed metric infinity

    - OSPF - seed metric 20 (1 for BGP routes)
    
    - RIP - seed metric infinity
    
    - BGP - uses default IGP metric value
    
- Configuring mutual route redistribution

    - see redistribute-topology.png for the topology

    - R2
```
router ospf 1
 redistribute eigrp 1
 
router eigrp 1
 redistribute ospf 1
```

- Show commands on R1
```
show ip route

# OSPF learned routes have an metric of 20 and type E2 (External type 2)
```

- External type 2 - keeps the metric values assigned by the ASBR throught the redistribution topology (does not change it the routes pass more than one router) - example - for OSPF it remains 20 

    - R2(ASBR) -> R1(metric 20) -> R3(metric 20) -> R4(metric 20)

- External type 2 - take the metric values assigned by the ASBR and it will add cost for each router hop 

    - R2(ASBR) -> R1(metric 20) -> R3(metric 30) -> R4(metric 40)

- Show commands on R3
```
show ip route

# No EIGRP learned routes in the routing table (Routes distributed into EIGRP have default metric of infinity)
```

- Set the global default metric for eigrp - on R2

- EIGRP External have the default AD of 170

```
router eigrp 1
 # bandwidth delay reliability load mtu
 default-metric 1000000 1 255 1 1500
 
router ospf 1
 default-metric 30
```

- Set metric as part of redistribute command - R2

```
router eigrp 1
 no default-metric
 no redistribute ospf 1
 redistribute ospf 1 metric 1000000 1 255 1 1500
```

- Set metric with a route map - R2

```
route-map SET-METRIC
 set metric 1000000 1 255 1 1500
 exit
router eigrp 1
 redistribute ospf 1 route-map SET-METRIC
```

- Set route types redistributed as external type 1 for OSPF - R2

```
router ospf 1 
 no redistribute eigrp 1 
 redistribute eigrp 1 metric-type 1
```

- Set the Administrative distance for a routing protocol learned routes

```
router ospf 1
 distance 80
```

- Set a tag of 10 for routes coming from EIGRP into OSPF - R2

- Deny packets with tag 10 to be redistributed from OSPF into EIGRP

```
route-map TAG10
 set tag 10
 
route-map DENYTAG10 deny 10
 match tag 10
 exit
route map DENYTAG10 permit 20
 
router ospf 1
 redistribute eigrp 1 route-map TAG10
 
router eigrp 1
 default-metric 1000000 1 255 1 1500
 redistribute ospf 1 route-map DENYTAG10
```
