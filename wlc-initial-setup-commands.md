## C9800 WLC configuration - initial install from terminal

- You should have 2 or 3 interfaces in the VM

```
show ip interface brief

cont f
 hostname C9800-1
 user-name admin
  priviledge 15
  password 0 Cisco123

 interface gig1
  no switchport
  ip address 10.10.10.10 255.255.255.0
  no shut

 interface gig2
  switchport
  switchport mode trunk
  switchport trunk native vlan 77
  no shut

 interface vlan 77
  ip address 192.168.77.10 255.255.255.0
  no shut

 ip route 10.10.10.0 255.255.255.0 10.10.10.1
 ip route 0.0.0.0 0.0.0.0 192.168.77.1

 wireless management interface vlan 77 
 exit

 ap dot11 24ghz shutdown
 ap dot11 5ghz shutdown
 ap country BE,US
 no ap dot11 24ghz shutdown
 np ap dot11 5ghz shutdown

 wireless config vwlc-ssc key size 2048 signature-algo sha256 password 0 Cisco123

 ip name-server 1.1.1.1 8.8.8.8
 ntp server pool.ntp.org
 do write memory
```

- For proxmox to enable vlan tagging on interfaces:

```
apt install net-tools
ifconfig ens224 promisc
ifconfig ens224 down
ifconfig ens224 up
```

