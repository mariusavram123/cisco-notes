## VRF forwarding and Tunnel VRF 

### VRF forwarding

![tunnel-vrf-forwarding](./tunnel-vrf-forwarding.png)

- VRF config: R2 and R3

```
R2#sh run | s vrf def 
vrf definition TEST1
 !
 address-family ipv4
 exit-address-family
```

```
R3#show run | s vrf def
vrf definition TEST1
 !
 address-family ipv4
 exit-address-family
```

- Tunnel1 interface config: R2 and R3

```
R2#sh run int tunn 1
Building configuration...

Current configuration : 150 bytes
!
interface Tunnel1
 vrf forwarding TEST1
 ip address 10.111.111.2 255.255.255.0
 tunnel source GigabitEthernet0/0
 tunnel destination 10.1.13.2
end

```

```
R3#sh run int tunn 1
Building configuration...

Current configuration : 150 bytes
!
interface Tunnel1
 vrf forwarding TEST1
 ip address 10.111.111.3 255.255.255.0
 tunnel source GigabitEthernet0/0
 tunnel destination 10.1.12.2
end

```

- R2 and R3 routing table (global)

```
R2#show ip route 
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 3 subnets, 2 masks
C        10.1.12.0/30 is directly connected, GigabitEthernet0/0
L        10.1.12.2/32 is directly connected, GigabitEthernet0/0
S        10.1.13.0/30 [1/0] via 10.1.12.1
```

```
R3#show  ip route 
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 3 subnets, 2 masks
S        10.1.12.0/30 [1/0] via 10.1.13.1
C        10.1.13.0/30 is directly connected, GigabitEthernet0/0
L        10.1.13.2/32 is directly connected, GigabitEthernet0/0
```

- The routes that are on the **underlying tunnel** source/destination are in the **global routing table**

- The tunnel itself and G0/1 interfaces are forwarding on the VRF, the static routes are added on the the vrf instance (for networks between R2 -> H1/R3 -> H2)

```
R2#show vrf
  Name                             Default RD            Protocols   Interfaces
  TEST1                            <not set>             ipv4        Tu1
                                                                     Gi0/1
R2#sh
R2#show ip route vrf TEST1

Routing Table: TEST1
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 5 subnets, 2 masks
C        10.2.12.0/24 is directly connected, GigabitEthernet0/1
L        10.2.12.1/32 is directly connected, GigabitEthernet0/1
S        10.2.13.0/24 [1/0] via 10.111.111.3
C        10.111.111.0/24 is directly connected, Tunnel1
L        10.111.111.2/32 is directly connected, Tunnel1
```

```
R3#sh vrf
  Name                             Default RD            Protocols   Interfaces
  TEST1                            <not set>             ipv4        Tu1
                                                                     Gi0/1
R3#sh
R3#show ip route vrf TEST1

Routing Table: TEST1
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 5 subnets, 2 masks
S        10.2.12.0/24 [1/0] via 10.111.111.2
C        10.2.13.0/24 is directly connected, GigabitEthernet0/1
L        10.2.13.1/32 is directly connected, GigabitEthernet0/1
C        10.111.111.0/24 is directly connected, Tunnel1
L        10.111.111.3/32 is directly connected, Tunnel1
```

- R2 and R3 routes:

```
R2#sh run | i ip route
ip route 10.1.13.0 255.255.255.252 10.1.12.1
ip route vrf TEST1 10.2.13.0 255.255.255.0 10.111.111.3
```

```
R3#sh run | i ip route
ip route 10.1.12.0 255.255.255.252 10.1.13.1
ip route vrf TEST1 10.2.12.0 255.255.255.0 10.111.111.2
```

- Routing table of R1:

```
R1#show vrf

R1#show ip route 
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
C        10.1.12.0/30 is directly connected, GigabitEthernet0/0
L        10.1.12.1/32 is directly connected, GigabitEthernet0/0
C        10.1.13.0/30 is directly connected, GigabitEthernet0/1
L        10.1.13.1/32 is directly connected, GigabitEthernet0/1
```

### Tunnel VRF

- Using `tunnel vrf` on the interface, we tell the tunnel to search for the **underlay routes** in the vrf specified

- Using the `vrf forwarding` command on the interface, we tell to the tunnel to put it's routes (**overlay**) in the specified tunnel

![tunnel-vrf-topology](./tunnel-vrf-topology.png)


- VRF config on R2 and R3:

```
R2(config)#do sh run | s vrf def
vrf definition GREEN
 !
 address-family ipv4
 exit-address-family
vrf definition RED
 !
 address-family ipv4
 exit-address-family
```

```
R3(config)#do sh run | s vrf def
vrf definition GREEN
 !
 address-family ipv4
 exit-address-family
vrf definition RED
 !
 address-family ipv4
 exit-address-family
```

- R2:

```
R2#sh ip route 
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

R2#sh
R2#show ip ro vrf GREEN

Routing Table: GREEN
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 3 subnets, 2 masks
C        10.1.12.0/30 is directly connected, GigabitEthernet0/0
L        10.1.12.2/32 is directly connected, GigabitEthernet0/0
S        10.1.13.0/30 [1/0] via 10.1.12.1
R2#sh vrf
  Name                             Default RD            Protocols   Interfaces
  GREEN                            <not set>             ipv4        Gi0/0
  RED                              <not set>             ipv4        Tu1
                                                                     Gi0/1
R2#sh
R2#show ip route vrf RED

Routing Table: RED
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 5 subnets, 2 masks
C        10.2.12.0/24 is directly connected, GigabitEthernet0/1
L        10.2.12.1/32 is directly connected, GigabitEthernet0/1
S        10.2.13.0/24 [1/0] via 10.111.111.3
C        10.111.111.0/24 is directly connected, Tunnel1
L        10.111.111.2/32 is directly connected, Tunnel1
```

```
R2#sh run int tunn 1
Building configuration...

Current configuration : 166 bytes
!
interface Tunnel1
 vrf forwarding RED
 ip address 10.111.111.2 255.255.255.0
 tunnel source GigabitEthernet0/0
 tunnel destination 10.1.13.2
 tunnel vrf GREEN
end

```

```
R2#sh run | i ip route
ip route vrf GREEN 10.1.13.0 255.255.255.252 10.1.12.1
ip route vrf RED 10.2.13.0 255.255.255.0 10.111.111.3
```

- R3:

```
R3#sh ip route 
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

R3#sh ip route vrf GREEN

Routing Table: GREEN
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 3 subnets, 2 masks
S        10.1.12.0/30 [1/0] via 10.1.13.1
C        10.1.13.0/30 is directly connected, GigabitEthernet0/0
L        10.1.13.2/32 is directly connected, GigabitEthernet0/0
R3#sh vrf
  Name                             Default RD            Protocols   Interfaces
  GREEN                            <not set>             ipv4        Gi0/0
  RED                              <not set>             ipv4        Tu1
                                                                     Gi0/1
R3#sh ip route vrf RED

Routing Table: RED
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 5 subnets, 2 masks
S        10.2.12.0/24 [1/0] via 10.111.111.2
C        10.2.13.0/24 is directly connected, GigabitEthernet0/1
L        10.2.13.1/32 is directly connected, GigabitEthernet0/1
C        10.111.111.0/24 is directly connected, Tunnel1
L        10.111.111.3/32 is directly connected, Tunnel1
```

```
R3#sh run int tunn 1
Building configuration...

Current configuration : 166 bytes
!
interface Tunnel1
 vrf forwarding RED
 ip address 10.111.111.3 255.255.255.0
 tunnel source GigabitEthernet0/0
 tunnel destination 10.1.12.2
 tunnel vrf GREEN
end

```

```
R3#sh run | i ip route
ip route vrf GREEN 10.1.12.0 255.255.255.252 10.1.13.1
ip route vrf RED 10.2.12.0 255.255.255.0 10.111.111.2
```

### IPSEC IKEV1 with FVRF (IPSEC tunnel with IKEv1 in VRF)

- Define crypto keyring:

- R2:

```
crypto keyring KR1 vrf GREEN 
  pre-shared-key address 10.1.13.2 key MARIUS12345
 rsa-pubkey address 10.1.13.2
  address 10.1.13.2
  serial-number 00111111
  key-string
  00101110
  quit
```

- R3:

```
crypto keyring KR1 vrf GREEN 
  pre-shared-key address 10.1.12.2 key MARIUS12345
 rsa-pubkey address 10.1.12.2
  address 10.1.12.2
  serial-number 00111111
  key-string
  00101110
  quit
```

- Define isakmp-profile and isakmp policy

- R2:

```
crypto isakmp policy 10
 encr aes 256
 hash sha256
 authentication pre-share
 group 16
crypto isakmp key MARIUS12345 address 0.0.0.0        
crypto isakmp profile MYPROFILE
   vrf GREEN
   keyring KR1
   match identity address 10.1.13.2 255.255.255.255 GREEN
```

- R3:

```
crypto isakmp policy 10
 encr aes 256
 hash sha256
 authentication pre-share
 group 16
crypto isakmp key MARIUS12345 address 0.0.0.0        
crypto isakmp profile MYPROFILE
   vrf GREEN
   keyring KR1
   match identity address 10.1.12.2 255.255.255.255 GREEN
```

- Define IPSEC transport set and crypto map params:

- R2:

```
crypto ipsec transform-set IPSEC-TUNNEL esp-aes 256 esp-sha256-hmac 
 mode tunnel
crypto map IPSEC-MAP isakmp-profile MYPROFILE
crypto map IPSEC-MAP 10 ipsec-isakmp 
 set peer 10.1.13.2
 set transform-set IPSEC-TUNNEL 
 set isakmp-profile MYPROFILE
 match address GRE-IPSEC
```

- R3:

```
crypto ipsec transform-set IPSEC-TUNNEL esp-aes 256 esp-sha256-hmac 
 mode tunnel
crypto map IPSEC-MAP isakmp-profile MYPROFILE
crypto map IPSEC-MAP 10 ipsec-isakmp 
 set peer 10.1.12.2
 set transform-set IPSEC-TUNNEL 
 set isakmp-profile MYPROFILE
 match address GRE-IPSEC
```

- Set the crypto map to the interface:

- R2:

```
interface g0/0
  crypto map IPSEC-MAP
```

- R3:

```
interface g0/0
  crypto map IPSEC-MAP
```

- Cisco docs:

[Cisco-IKEV1-FVRF](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_ikevpn/configuration/xe-3s/VRF-Aware_IPsec.html)

### IPSEC IKEV1 with FVRF (IPSEC tunnel with IKEv2 in VRF)

1. IKEV2 proposal

2. IKEV2 policy

3. IKEV2 keyring (not really needed if you set local/remote auth methods as in this example)

4. IKEV2 profile

5. Transform set

6. Crypto map

- R2:

1. 

```
crypto ikev2 proposal IKEv2PROPOSAL1 
 encryption aes-cbc-256
 integrity sha256
 group 16
```

2. 

```
crypto ikev2 policy IKEv2POLICY1 
 match fvrf GREEN
 proposal IKEv2PROPOSAL1
```

3. 

```
crypto ikev2 keyring IKEv2KEYRING1
 peer any
  address 0.0.0.0 0.0.0.0
  pre-shared-key local MARIUS12345
  pre-shared-key remote MARIUS12345
```

4. 

```
crypto ikev2 profile IKEv2PROFILE1
 match fvrf GREEN
 match identity remote address 10.1.13.2 255.255.255.255 
 identity local address 10.1.12.2
 authentication remote pre-share key MARIUS12345
 authentication local pre-share key MARIUS12345
```

5. 

```
crypto ipsec transform-set IPSEC-TUNNEL esp-aes 256 esp-sha256-hmac 
 mode tunnel
```

6. 

```
crypto map IPSEC-MAP 10 ipsec-isakmp 
 set peer 10.1.13.2
 set transform-set IPSEC-TUNNEL 
 set ikev2-profile IKEv2PROFILE1
 match address GRE-IPSEC
```

```
R2#sh run int g0/0
Building configuration...

Current configuration : 160 bytes
!
interface GigabitEthernet0/0
 vrf forwarding GREEN
 ip address 10.1.12.2 255.255.255.252
 duplex auto
 speed auto
 media-type rj45
 crypto map IPSEC-MAP
end

```

- R3:

1. 

```
crypto ikev2 proposal IKEv2PROPOSAL1 
 encryption aes-cbc-256
 integrity sha256
 group 16
```

2. 

```
crypto ikev2 policy IKEv2POLICY1 
 match fvrf GREEN
 proposal IKEv2PROPOSAL1
```

3. 

```
crypto ikev2 keyring IKEv2KEYRING1
 peer any
  address 0.0.0.0 0.0.0.0
  pre-shared-key local MARIUS12345
  pre-shared-key remote MARIUS12345
 !
```

4. 

```
crypto ikev2 profile IKEv2PROFILE1
 match fvrf GREEN
 match identity remote address 10.1.12.2 255.255.255.255 
 identity local address 10.1.13.2
 authentication remote pre-share key MARIUS12345
 authentication local pre-share key MARIUS12345
```

5. 

```
crypto ipsec transform-set IPSEC-TUNNEL esp-aes 256 esp-sha256-hmac 
 mode tunnel
```

6. 

```
crypto map IPSEC-MAP 10 ipsec-isakmp 
 set peer 10.1.12.2
 set transform-set IPSEC-TUNNEL 
 set ikev2-profile IKEv2PROFILE1
 match address GRE-IPSEC
```

```
R3#sh run int g0/0
Building configuration...

Current configuration : 160 bytes
!
interface GigabitEthernet0/0
 vrf forwarding GREEN
 ip address 10.1.13.2 255.255.255.252
 duplex auto
 speed auto
 media-type rj45
 crypto map IPSEC-MAP
end

```

- IKEv2 profile using the keyring for peers:

- R2:

```
crypto ikev2 profile IKEv2PROFILE1
 match fvrf GREEN
 match identity remote address 10.1.13.2 255.255.255.255 
 identity local address 10.1.12.2
 authentication remote pre-share
 authentication local pre-share
 keyring local IKEv2KEYRING1
```

- R3:

```
crypto ikev2 profile IKEv2PROFILE1
 match fvrf GREEN
 match identity remote address 10.1.12.2 255.255.255.255 
 identity local address 10.1.13.2
 authentication remote pre-share
 authentication local pre-share
 keyring local IKEv2KEYRING1
```

[Cisco-IKEV2-FVRF](https://community.cisco.com/t5/security-knowledge-base/implementing-ikev2-vrf-aware-crypto-map-vpn/ta-p/5316297)