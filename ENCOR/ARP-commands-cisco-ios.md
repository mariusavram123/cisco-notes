## ARP commands Cisco IOS

- View the ARP table:

```
show arp
```

- or

```
show ip arp
```

- Showing an ARP entry for an IP, with details:

```
show arp 192.168.1.2 detail
```

- Enabling debug for arp messages:

```
debug arp
```

### Enable/disable proxy ARP and local proxy ARP

- Global

```
conf t
 [no] ip arp proxy disable
```

- On the interface

```
conf t
 interface g0/0
  [no] ip proxy-arp
```

- View the proxy ARP status on an interface

```
show ip interface g0/0
```

- Configure local proxy ARP per interface

```
conf t
 interface g0/0
  ip local-proxy-arp
```

### Manual ARP entry configuration

- Manual ARP entry:

```
conf t
 arp 192.168.1.2 5254.001e.b897 arpa
```

- View in detail an ARP entry:

```
show arp 192.168.1.2 detail
```

### Clearing ARP entries

- Clearing ARP entries on router:

```
clear arp
```

### Configure ARP timeout

- Per interface

```
conf t
 interface g0/0
  arp timeout 180 # timer is in seconds
```
