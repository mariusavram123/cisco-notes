- Alma2
```
!
frr version 10.3
frr defaults traditional
hostname alma2
!
vrf vrf1
exit-vrf
!
vrf vrf2
exit-vrf
!
interface dummy0
 ip ospf 1 area 0
exit
!
interface eth2
 ip ospf 1 area 0
 mpls enable
exit
!
router bgp 65000
 neighbor 10.105.105.105 remote-as 65000
 neighbor 10.105.105.105 update-source dummy0
 !
 address-family ipv4 unicast
  no neighbor 10.105.105.105 activate
 exit-address-family
 !
 address-family ipv4 vpn
  neighbor 10.105.105.105 activate
 exit-address-family
exit
!
router bgp 65000 vrf vrf1
 neighbor 10.10.10.1 remote-as 65001
 neighbor 10.10.10.1 update-source 10.10.10.2
 !
 address-family ipv4 unicast
  label vpn export auto
  rd vpn export 65000:155
  rt vpn both 65000:155
  export vpn
  import vpn
 exit-address-family
exit
!
router bgp 65000 vrf vrf2
 neighbor 10.10.20.1 remote-as 65003
 neighbor 10.10.20.1 update-source 10.10.20.1
 !
 address-family ipv4 unicast
  label vpn export auto
  rd vpn export 65000:165
  rt vpn both 65000:165
  export vpn
  import vpn
 exit-address-family
exit
!
router ospf 1
exit
!
mpls ldp
 router-id 10.102.102.102
 !
 address-family ipv4
  discovery transport-address 10.102.102.102
  !
  interface eth2
  exit
  !
 exit-address-family
 !
exit
!
segment-routing
 traffic-eng
 exit
exit
!
end
```
- Alma3:

```

!
frr version 10.3
frr defaults traditional
hostname alma3
!
interface dummy0
 ip ospf 1 area 0
exit
!
interface eth0
 ip ospf 1 area 0
 mpls enable
exit
!
interface eth1
 ip ospf 1 area 0
 mpls enable
exit
!
router ospf 1
exit
!
mpls ldp
 router-id 10.103.103.103
 !
 address-family ipv4
  discovery transport-address 10.103.103.103
  !
  interface eth0
  exit
  !
  interface eth1
  exit
  !
 exit-address-family
 !
exit
!
segment-routing
 traffic-eng
 exit
exit
!
end

```

- Alma4

```
frr defaults traditional
hostname alma4
!
interface dummy0
 ip ospf 1 area 0
exit
!
interface eth0
 ip ospf 1 area 0
 mpls enable
exit
!
interface eth1
 ip ospf 1 area 0
 mpls enable
exit
!
router ospf 1
exit
!
mpls ldp
 router-id 10.104.104.104
 !
 address-family ipv4
  discovery transport-address 10.104.104.104
  !
  interface eth0
  exit
  !
  interface eth1
  exit
  !
 exit-address-family
 !
exit
!
segment-routing
 traffic-eng
 exit
exit
!
end
```

- Alma5:

```
frr version 10.3
frr defaults traditional
hostname alma5
!
vrf vrf1
exit-vrf
!
vrf vrf2
exit-vrf
!
interface dummy0
 ip ospf 1 area 0
exit
!
interface eth0
 ip ospf 1 area 0
 mpls enable
exit
!
router bgp 65000
 neighbor 10.102.102.102 remote-as 65000
 neighbor 10.102.102.102 update-source dummy0
 !
 address-family ipv4 unicast
  no neighbor 10.102.102.102 activate
 exit-address-family
 !
 address-family ipv4 vpn
  neighbor 10.102.102.102 activate
 exit-address-family
exit
!
router bgp 65000 vrf vrf1
 neighbor 10.10.60.2 remote-as 65002
 neighbor 10.10.60.2 update-source eth1
 !
 address-family ipv4 unicast
  label vpn export auto
  rd vpn export 65000:155
  rt vpn both 65000:155
  export vpn
  import vpn
 exit-address-family
exit
!
router bgp 65000 vrf vrf2
 neighbor 10.10.70.2 remote-as 65004
 neighbor 10.10.70.2 update-source 10.10.70.1
 !
 address-family ipv4 unicast
  label vpn export auto
  rd vpn export 65000:165
  rt vpn both 65000:165
  export vpn
  import vpn
 exit-address-family
exit
!
router ospf 1
exit
!
mpls ldp
 router-id 10.105.105.105
 !
 address-family ipv4
  discovery transport-address 10.105.105.105
  !
  interface eth0
  exit
  !
 exit-address-family
 !
exit
!
segment-routing
 traffic-eng
 exit
exit
!
end
```

- Alma1

```
!
frr version 10.3
frr defaults traditional
hostname alma1
!
router bgp 65001
 no bgp ebgp-requires-policy
 no bgp network import-check
 neighbor 10.10.10.2 remote-as 65000
 !
 address-family ipv4 unicast
  network 10.10.10.0/24
  network 10.101.101.101/32
 exit-address-family
exit
!
segment-routing
 traffic-eng
 exit
exit
!
end

```
