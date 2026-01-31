```
interface Tunnel0
 vrf forwarding TEST
 ip address 10.22.11.1 255.255.255.252
 tunnel source GigabitEthernet0/0
 tunnel destination 100.65.1.2
end
```

```
interface Tunnel0
 vrf forwarding TEST
 ip address 10.22.11.2 255.255.255.252
 tunnel source GigabitEthernet0/0
 tunnel destination 100.64.1.2
end
```

