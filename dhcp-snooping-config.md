# DHCP snooping configurations on Cisco IOS switches

- Configuration on SW1:

```
ip dhcp snooping vlan 1
no ip dhcp snooping information option
ip dhcp snooping
interface g0/2
 ip dhcp snooping trust
```

- Configuration on SW2:

```
ip dhcp snooping vlan 1
no ip dhcp snooping information option
ip dhcp snooping
interface g0/1
 ip dhcp snooping trust
```

- Show commands:

```
show ip dhcp snooping binding

```

- Set limit rate for dhcp messages in a minute per interface

```
interface g0/1
 ip dhcp snooping limit rate 30
```

- See dhcp-snooping-topology.png for network topology
