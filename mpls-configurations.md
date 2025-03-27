# MPLS configurations using Cisco IOS routers

- See mpls-network-topology.png for the used topology

## EBGP peerings between the CE and PE routers

- CE1 router:

```
router bgp 1
 neighbor 10.10.10.2 remote-as 100
 network 192.168.11.0 mask 255.255.255.0
```

- PE1 router:

```
router bgp 100
 neighbor 10.10.10.1 remote-as 1
```

- CE2 router:

```
router bgp 2
 neighbor 10.10.50.1 remote-as 100
 network 192.168.12.0 mask 255.255.255.0
```

- PE2 router:

```
router bgp 100
 neighbor 10.10.50.2 remote-as 2
```

## OSPF configuration between PE and P routers

### Do not advertise the networks between CE and PE routers in OSPF

- PE1:

```
router ospf 1
 network 10.10.20.0 0.0.0.255 area 0
 network 1.1.1.1 0.0.0.0 area 0
 passive-interface g0/1
```

- P1:

```
router ospf 1
 network 10.10.20.0 0.0.0.255 area 0
 network 10.10.30.0 0.0.0.255 area 0
 network 2.2.2.2 0.0.0.0 area 0
```

- P2:

```
router ospf 1
 network 10.10.30.0 0.0.0.255 area 0
 network 10.10.40.0 0.0.0.255 area 0
 network 3.3.3.3 0.0.0.0 area 0
```

- PE2:

```
router ospf 1
 network 10.10.40.0 0.0.0.255 area 0
 network 4.4.4.4 0.0.0.0 area 0
 passive-interface g0/1
```

## iBGP peerings between all PE routers to exchange the information about the customer IP address prefixes

- PE1: 
```
router bgp 100
 neighbor 4.4.4.4 remote-as 100
 neighbor 4.4.4.4 update-source lo 0
 neighbor 4.4.4.4 next-hop-self
```
- PE2:

```
router bgp 100
 neighbor 1.1.1.1 remote-as 100
 neighbor 1.1.1.1 update-source lo 0
 neighbor 1.1.1.1 next-hop-self
```

- Do the same for all other PE routers - enable iBGP peerings between them

## Enable MPLS on the interfaces of PE and P routers

- PE1:

```
interface g0/2
 mpls ip
```

- P1:

```
interface g0/2
 mpls ip
interface g0/3
 mpls ip
```

- P2:
```
interface g0/3
 mpls ip
interface g0/4
 mpls ip
```

- PE2:

```
interface g0/4
 mpls ip
```

## Configure VRFs and on PE routers

- PE1:
    - RD 100:1 should be configured on both PE routers and associated with VRF GREEN
```
ip vrf GREEN
 rd 100:1
 route-target import 100:1
 route-target export 100:1
interface g0/2
 ip vrf forwarding GREEN
 
```

## Enable VPNv4 address-family in BGP for exchanging of VPNv4 routes

- PE1 - Enable vpnv4 address-family routes, and disable IPv4 routes to be exchanged:
```
router bgp 100
 address-family vpnv4
  neighbor 4.4.4.4 activate
 exit address-family
 address-family ipv4
  no neighbor 4.4.4.4 activate
 exit address-family
```

- PE2 - enable vpnv4 address-family, and disable IPv4 routes to be exchanged

```
router bgp 100
 address-family vpnv4
  neighbor 1.1.1.1 activate
 exit address-family
 address-family ipv4
  no neighbor 1.1.1.1 activate
 exit address-family
```

- Verify BGP shared information

```
show bgp vpnv4 unicast all summary
```

## Configure CE routers to exchange vpnv4 routes:

- CE1:

```
interface lo 0 
 ip address 192.168.11.1 255.255.255.0
router bgp 1
 neighbor 10.10.10.2 remote-as 100
 network 192.168.11.0 mask 255.255.255.0
```

- PE1 - activate the VRF BGP peering and neighbor

```
router bgp 100
 address-family ipv4 vrf GREEN
 neighbor 10.10.10.1 remote-as 1
```

- CE2:

```
interface l0
 ip address 192.168.12.1 255.255.255.0
router bgp 2
 neighbor 10.10.50.2 remote-as 100
 network 192.168.12.0 mask 255.255.255.0
```

- PE2 - activate the VRF BGP peering and neighbor

```
router bgp 100
 address-family ipv4 vrf GREEN
 neighbor 10.10.50.1 remote-as 2
```

- Verify BGP peering on PE1:

```
show bgp vpnv4 unicast vrf GREEN

show bgp vpnv4 unicast all 192.168.12.0

show ip cef vrf GREEN 192.168.12.0
```

- Verifying MPLS forwarding table on P1 or P2:

    - These 2 routers does not have any knowledge of VPN labels added by PEs 

```
show mpls forwarding-table
```

## MPLS layer 2 VPNs

- Configure AToM to transport Ethernet frames over MPLS

    - BGP is not needed to be configured between PE routers
    
    - PE1 configuration for EoMPLS (Ethernet over MPLS)
        
        - xconnect command creates a pseudowire (a virtual layer 2 circuit) on that interface
        
        - 4.4.4.4 is the loopback address of PE2
        
        - 20 is the virtual circuit ID (or VCID)
    
```
interface g0/0
 xconnect 4.4.4.4 20 encapsulation mpls
```
    - PE2 configuration for EoMPLS 
    
```
interface g0/5
 xconnect 1.1.1.1 20 encapsulation mpls
```

- CE1 and CE2 configuration

- CE1
    
```
interface g0/1
 ip address 192.168.10.1 255.255.255.0
```

- CE2:

```
interface g0/1
 ip address 192.168.10.2 255.255.255.0
```
- In the case of AToM EoMPLS VPN - the PE routers become LDP neighbors directly between them

- Show commands:

```
show mpls ldp neighbor 4.4.4.4

show mpls l2transport binding
```

## MPLS EVPN configuration (Ethernet VPN over MPLS)

- Configure MP BGP on the PE routers

- PE1 router 

```
router bgp 100
 neighbor 4.4.4.4 remote-as 100
 neighbor 4.4.4.4 update-source l0
 neighbor 4.4.4.4 next-hop-self
 address-family l2vpn evpn
  neighbor 4.4.4.4 activate
 exit address-family
```
- Enable customer-facing interfaces to operate in a bridge domain at layer 2 - PE1

```
conf t
bridge-domain 10
 member g0/1 service-instance 10
interface g0/1
 service instance 10 ethernet
  encapsulation dot1q 10
```


- PE2 router

```
router bgp 100
 neighbor 1.1.1.1 remote-as 100
 neighbor 1.1.1.1 update-source l0
 neighbor 1.1.1.1 next-hop-self
 address-family l2vpn evpn
  neighbor 4.4.4.4 activate
 exit address family
bridge-domain 10
 member g0/1 service-instance 10
 interface g0/1
 service instance 10 ethernet
  encapsulation dot1q 10
```

- Enable the CE routers to send traffic with vlan tag 10

- CE1:

```
interface g0/1
 no shutdown
interface g0/1.10
 encapsulation dot1q 10
 ip address 192.168.11.1 255.255.255.0
```

- CE2:

```
interface g0/1
 no shutdown
interface g0/1.10
 encapsulation dot1q 10
 ip address 192.168.11.5 255.255.255.0
```

