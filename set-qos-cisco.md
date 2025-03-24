Cisco IOS:

Set a bandwith of 10% for https traffic and set dscp AF31 and a priority queue for it

Set a bandwidth of 10% for http traffic and set dscp AF32

Set a bandwidth of 5% for icmp traffic and set dscp CS2

Apply the policy on g0/0/0 output traffic.

1. Create class maps to match specific traffic:
```
class-map HTTPS_map
match protocol https
exit

class-map HTTP_MAP
match protocol http
exit

class-map ICMP_MAP
match protocol icmp
exit
```
2. Create policy maps to set the required policies for traffic:

```
policy-map G0/0/0_OUT
 class HTTPS_map
  priority percent 10
  set ip dscp af31
exit
 class HTTP_MAP
  bandwidth percent 10
  set ip dscp af32
exit
 class ICMP_MAP
  bandwidth percent 5
  set ip dscp cs2
exit
```

3. Apply the policy map on the g0/0/0 interface of traffic.
```
int g0/0/0
 service-policy output G0/0/0_OUT
exit
```
