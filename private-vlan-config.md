## Private VLANs configuration Cisco IOS

- VLAN 150 - primary VLAN

- VLAN 151 - community VLAN

- VLAN 152 and VLAN 153 - isolated VLANs

- Switch - all ports in primary VLAN 150:

    - f0/1 - promiscuous port
    
    - f0/2 and f0/3 - community VLAN 151
    
    - f0/4 - isolated VLAN 152
    
    - f0/5 - isolated VLAN 153
    
```
conf t

vtp mode transparent # VTP should be disabled or running in transparent mode

vlan 150
 private-vlan primary

vlan 151
 private-vlan community
 
vlan 152
 private-vlan isolated
 
vlan 153
 private-vlan isolated
 
int f0/1
 switchport mode private-vlan promiscuous
 switchport private-vlan mapping 150 add 151,152,153

int range f0/2 - 3
 switchport mode private-vlan host
 switchport private-vlan host-association 150 151
 
int f0/4
 switchport mode private-vlan host
 switchport private-vlan host-association 150 152
 
int f0/5
 switchport mode private-vlan host
 switchport private-vlan host-association 150 153
 
show vlan private-vlan

show interface f0/1 switchport

show interface f0/3 switchport
```
- For switches that do not support private vlan you can add a protected vlan port

```
int f0/6
 switchport protect
```

