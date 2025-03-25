# Configure Dynamic ARP inspection for Cisco Switches

- Prerequisites: enable dhcp snooping on the switches 

- SW1 configuration:

```
ip arp inspection vlan 1
ip arp inspection validate src-mac dst-mac ip

ip dhcp snooping vlan 1
no ip dhcp snooping information option
ip dhcp snooping

interface range g0/1 - 2
 ip arp inspection trust
 ip dhcp snooping trust
```

- SW2 configuration:

```
ip arp inspection vlan 1
ip arp inspection validate src-mac dst-mac ip

ip dhcp snooping vlan 1
no ip dhcp snooping information option
ip dhcp snooping

interface g0/1
 ip arp inspection trust
 ip dhcp snooping trust
```

- Set arp traffic rates on interfaces:
```
interface g0/1
 ip arp inspection limit rate 25 burst interval 2 # Allow 25 ARP messages in 2 seconds interval
```


- Show commands:

```
show ip arp inspection interfaces

show ip dhcp snooping binding
```

- Check dynamic-arp-inspection-topology.png for the network topology
