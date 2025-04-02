## MPLS L3 VPN with almalinux VMs in GNS3

![Topology](./mpls-linux.png)

- Install required software

```
dnf makecache
dnf install -y epel-release kernel-modules-extra
dnf install -y frr
```

- The default frr version from almalinux repository does not have the ldpd daemon includes, so it will not start. 

- In this condition MPLS can't be done

- It needs to install the frr from the frr rpm repository

- Save this script as addfrr.sh and `chmod 755 ./addfrr.sh`

```bash
#!/bin/bash
# possible values for FRRVER: frr-6 frr-7 frr-8 frr-9 frr-10 frr-stable
# frr-stable will be the latest official stable release
FRRVER="frr-stable"

# add RPM repository on CentOS 6
#    Note: FRR only supported up to Version 7.4.x
#curl -O https://rpm.frrouting.org/repo/$FRRVER-repo-1-0.el6.noarch.rpm
#sudo yum install ./$FRRVER*

# add RPM repository on CentOS 7
#curl -O https://rpm.frrouting.org/repo/$FRRVER-repo-1-0.el7.noarch.rpm
#sudo yum install ./$FRRVER*

# add RPM repository on RedHat 8
#    Note: Supported since FRR 7.3
#curl -O https://rpm.frrouting.org/repo/$FRRVER-repo-1-0.el8.noarch.rpm
#sudo yum install ./$FRRVER*

# add RPM repository on RedHat 9
#    Note: Supported since FRR 8.3
curl -O https://rpm.frrouting.org/repo/$FRRVER-repo-1-0.el9.noarch.rpm
sudo dnf install ./$FRRVER*

# install FRR
sudo dnf install frr frr-pythontools
```

- Modprobe MPLS kernel modules

```
cat >/etc/modules-load.d/mpls.conf <<EOF
mpls_router
mpls_iptunnel
mpls_gso
dummy
EOF
```

- Patch sysctl for MPLS forwarding

```
modprobe mpls_router
modprobe mpls_iptunnel
cat >/etc/sysctl.d/90-mpls-router.conf <<EOF
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
net.ipv4.conf.all.rp_filter=0
net.mpls.platform_labels=1048575
net.ipv4.tcp_l3mdev_accept=1
net.ipv4.udp_l3mdev_accept=1
net.mpls.conf.lo.input=1
EOF
sysctl -p /etc/sysctl.d/90-mpls-router.conf
```

- Load daemons and start frr


    - add zebra=yes on the top of the daemons list on /etc/frr/daemons (or else the kernel will not get the routes from the routing protocol)
    - add ospfd_instances=99,1,2,3 in /etc/frr/daemons to enable multi instace support for ospfd daemon
    - add ldpd=yes to /etc/frr/daemons to enable mpls support for frr

```
sed -i "s/=no/=yes/g" /etc/frr/daemons
systemctl enable frr
systemctl restart frr

```

- Create a dummy interface on each VM

- Alma7:

```
nmcli conn add type dummy con-name dummy0 ifname dummy0 ipv4.method manual ipv4.address 10.107.107.107/32
nmcli conn up dummy0
nmcli conn add type ethernet ifname eth0 con-name eth0 ipv4.method manual ipv4.address 10.10.20.1/24
nmcli conn up dummy0
```

- Alma1: 

```
nmcli conn add type dummy con-name dummy0 ifname dummy0 ipv4.method manual ipv4.address 10.101.101.101/32
nmcli connection up dummy0
nmcli conn add type ethernet ifname eth0 con-name eth0 ipv4.method manual ipv4.address 10.10.10.1/24
nmcli conn up eth0
```

- Alma2:

```
nmcli conn add type dummy con-name dummy0 ifname dummy0 ipv4.method manual ipv4.address 10.102.102.102/32
nmcli conn up dummy0
nmcli conn add type ethernet ifname eth2 con-name eth2 ipv4.method manual ipv4.address 10.10.30.1/24
nmcli conn up eth2

nmcli connection add type vrf ifname vrf1 con-name vrf1 table 155 ipv4.method disabled ipv6.method disabled
nmcli conn up vrf1

nmcli conn add type ethernet ifname eth0 con-name eth0 master vrf1 ipv4.method manual ipv4.address 10.10.10.2/24
nmcli conn up eth0

nmcli connection add type vrf ifname vrf2 con-name vrf2 table 165 ipv4.method disabled ipv6.method disabled
nmcli conn up vrf2

nmcli conn add type ethernet ifname eth1 con-name eth1 master vrf2 ipv4.method manual ipv4.address 10.10.20.2/24
nmcli conn up eth1

ip vrf exec vrf1 ping 10.10.10.1
ip vrf exec vrf2 ping 10.10.20.1
```

- Alma3:

```
nmcli conn add type dummy con-name dummy0 ifname dummy0 ipv4.method manual ipv4.address 10.103.103.103/32
nmcli conn up dummy0
nmcli conn add type ethernet ifname eth0 con-name eth0 ipv4.method manual ipv4.address 10.10.30.2/24
nmcli conn up eth0
nmcli conn add type ethernet ifname eth1 con-name eth1 ipv4.method manual ipv4.address 10.10.40.1/24
nmcli conn up eth1
```

- Alma4:

```
nmcli conn add type dummy con-name dummy0 ifname dummy0 ipv4.method manual ipv4.address 10.104.104.104/32
nmcli conn up dummy0
nmcli conn add type ethernet ifname eth0 con-name eth0 ipv4.address 10.10.40.2/24 ipv4.method manual
nmcli conn up eth0
nmcli conn add type ethernet ifname eth1 con-name eth1 ipv4.address 10.10.50.1/24 ipv4.method manual
nmcli conn up eth1
```

- Alma5:

```
nmcli conn add type dummy con-name dummy0 ifname dummy0 ipv4.method manual ipv4.address 10.105.105.105/32
nmcli conn up dummy0
nmcli conn add type ethernet ifname eth0 con-name eth0 ipv4.address 10.10.50.2/24 ipv4.method manual
nmcli conn up eth0

nmcli connection add type vrf ifname vrf1 con-name vrf1 table 155 ipv4.method disabled ipv6.method disabled
nmcli conn up vrf1

nmcli conn add type ethernet ifname eth1 con-name eth1 master vrf1 ipv4.method manual ipv4.address 10.10.60.1/24
nmcli conn up eth1

nmcli connection add type vrf ifname vrf2 con-name vrf2 table 165 ipv4.method disabled ipv6.method disabled
nmcli conn up vrf2

nmcli conn add type ethernet ifname eth2 con-name eth2 master vrf2 ipv4.method manual ipv4.address 10.10.70.1/24
nmcli conn up eth2

ip vrf exec vrf1 ping 10.10.60.2
ip vrf exec vrf2 ping 10.10.70.2
```

- Alma6:

```
nmcli conn add type dummy con-name dummy0 ifname dummy0 ipv4.method manual ipv4.address 10.106.106.106/32
nmcli conn up dummy0
nmcli conn add type ethernet ifname eth0 con-name eth0 ipv4.method manual ipv4.address 10.10.60.2/24
nmcli conn up eth0
```

- Alma8:

```
nmcli conn add type dummy con-name dummy0 ifname dummy0 ipv4.method manual ipv4.address 10.108.108.108/32
nmcli conn up dummy0
nmcli conn add type ethernet ifname eth0 con-name eth0 ipv4.method manual ipv4.address 10.10.70.2/24
nmcli conn up eth0
```

- Enable OSPF process per interfaces 

    - Alma2 - eth2 and dummy0
    
    - Alma3 - eth0, eth1 and dummy0
    
    - Alma4 - eth0, eth1 and dummy0
    
    - Alma5 - eth0 and dummy0
    
- Alma2(PE1):

```
vtysh
 conf term
  router ospf 1
   ospf router-id 10.102.102.102
  interface eth2
   ip ospf 1 area 0
  interface dummy0
   ip ospf 1 area 0
```

- Alma3(P1):

```
vtysh
 conf term
  router ospf 1
   ospf router-id 10.103.103.103
  interface eth0
   ip ospf 1 area 0
  interface eth1
   ip ospf 1 area 0
  interface dummy0
   ip ospf 1 area 0
```

- Alma4(P2):
```
vtysh
 conf term
  router ospf 1
   ospf router-id 10.104.104.104
  interface eth0
   ip ospf 1 area 0
  interface eth1
   ip ospf 1 area 0
  interface dummy 0
   ip ospf 1 area 0
```

- Alma5(PE2):

```
vtysh
 conf t
  router ospf 1
   ospf router-id 10.105.105.105
  interface eth0
   ip ospf 1 area 0
  interface dummy0
   ip ospf 1 area 0
```

- Enable MPLS in the core routers (Alma2, Alma3, Alma4, Alma5)

- Alma2:

```
echo "net.mpls.conf.eth2.input=1" >> /etc/sysctl.conf
sysctl -p

vtysh
 conf t
  interface eth2
   mpls enable
   
  mpls ldp 
    router-id 10.102.102.102 
    address-family ipv4
     discovery transport-address 10.102.102.102
      interface eth2
```

- Alma3:

```
echo "net.mpls.conf.eth0.input=1" >> /etc/sysctl.conf
echo "net.mpls.conf.eth1.input=1" >> /etc/sysctl.conf
sysctl -p

vtysh
 conf t
  interface eth0
   mpls enable
  interface eth1
   mpls enable

 mpls ldp
  router-id 10.103.103.103
  address-family ipv4
   discovery transport-address 10.103.103.103
    interface eth0
    interface eth1
    
  
```

- Alma4:

```
echo "net.mpls.conf.eth0.input=1" >> /etc/sysctl.conf
echo "net.mpls.conf.eth1.input=1" >> /etc/sysctl.conf
sysctl -p

vtysh 
 conf t
  interface eth0
   mpls enable
  interface eth1
   mpls enable
   
  mpls ldp
   router-id 10.104.104.104
   address-family ipv4
    discovery transport-address 10.104.104.104
    interface eth0
    interface eth1
```

- Alma5:

```
echo "net.mpls.conf.eth0.input=1" >> /etc/sysctl.conf
sysctl -p

vtysh
 conf t
  interface eth0
   mpls enable
  
  mpls ldp
   router-id 10.104.104.104
   address-family ipv4
    discovery interface-address 10.105.105.105
    interface eth0
```

- Enable internal BGP between PEs (Alma2 and Alma5)

```
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

```


- Alma5

```
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

```

- Enable BGP on CE routers

- Alma1:

```
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
```

- Alma7:

```
router bgp 65003
 no bgp ebgp-requires-policy
 no bgp network import-check
 neighbor 10.10.20.2 remote-as 65000
 !
 address-family ipv4 unicast
  network 10.10.20.0/24
  network 10.107.107.107/32
 exit-address-family
exit
```

- Alma6:

```
router bgp 65002
 no bgp ebgp-requires-policy
 no bgp network import-check
 neighbor 10.10.60.1 remote-as 65000
 !
 address-family ipv4 unicast
  network 10.10.60.0/24
  network 10.106.106.106/32
 exit-address-family
exit
```

- Alma8:

```
router bgp 65004
 no bgp ebgp-requires-policy
 no bgp network import-check
 neighbor 10.10.70.1 remote-as 65000
 !
 address-family ipv4 unicast
  network 10.10.70.0/24
  network 10.108.108.108/32
 exit-address-family
exit
```
