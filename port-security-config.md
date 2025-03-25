# Port security configuration Cisco IOS

- #SW1 F0/1, F0/2, F0/3#
    - Violation mode: Shutdown
    - Maximum addresses: 1
    - Sticky learning: Disabled
    - Aging time: 1 hour
    
```
interface range f0/1 - 3
 switchport mode access
 switchport port-security
 switchport port-security maximum 1
 switchport port-security aging time 60
 swithport port-security violation shutdown
 no switchport port-security mac-address sticky
```

- #SW2 G0/1#
    - Violation mode: Restrict
    - Maximum addresses: 4
    - Sticky learning: Enabled
    
```
interface g0/1
 swithport mode trunk
 switchport port-security
 switchport port-security maximum 4
 switchport port-security violation restrict
 switchport port-security mac-address sticky
```

- Please see port-security-topology.png for the network topology
