# QoS configuration example on Cisco IOS

- Match all MAIL traffic - SMTP, IMAP, POP3

```
class-map match-any EMAIL
 match protocol pop3
 match protocol smtp
 match protocol imap
 match protocol exchange
 exit
```

- Match VoIP traffic

```
class-map VOICE
 match protocol rtp audio
 exit
```

- Match Scavenger traffic

```
class-map SCAVENGER
 match protocol bittorrent
 exit
```

- Create a policy map for the traffic

```
policy-map DEMO
 class EMAIL
  bandwidth 512 # this is in kbps
  random-detect dscp-based  # default is IPP(IP Precedence) 
  random-detect ecn # This turns on ECN
  exit
 class VOICE
  priority 256 # this is in kbps - priority queue
  exit
 class SCAVENGER
  police 128000 # this is in bits per second, not kbps
   exit
  exit
 exit
```

- Apply the policy to the interface

```
interface g0/2
 service-policy output DEMO
 exit
 
```

- Verification commands

```
show policy-map interface g0/2
```


## Switch-based AutoQoS configuration for VoIP

- This should be applied to interfaces only connected to Cisco IP phones

- A lot of mls qos and policy map commands get added when enabling this auto qos 

```
interface range f0/13 - 14
 auto qos voip cisco-phone
```


## Router-based AutoOoS configuration ofor VoIP

- This cannot be applied on ethernet interfaces. Only works for Serials (HDLC/PPP) or Frame relay

- This creates class-maps and access-lists for voice automatically

```
interface serial 0/1/0
 auto qos voip
```

## Router-based AutoOoS enterprise 

- Enable traffic monitoring for a 2 -3 days period and the router will create a policy that will match the traffic patterns, and will suggest a policy for it

- Required enabling ip cef

```
ip cef

int serial 0/1/0
 auto discover qos
 exit
exit

show auto discovery qos interface s0/1/0

interface serial 0/1/0
 auto qos
end
```

## Switch OoS 

- Configure QoS settings on the switch (C3750) such that:

  - The switch should map the signalling CoS value (CoS=3) and RTP media CoS values (Video CoS=4 and Voice CoS=5) to appropiate DSCP values:
  
  - The switch should trust CoS values if those values come from a Cisco IP phone
  
  - Enable the egress expedite queue on Cisco IP phone ports
  
  - Globally enable QoS on the switch
  
  - Only queue #1 can be a priority queue
  
```
mls qos

mls qos map cos-dscp 0 8 16 24 34 46 48 56

interface range fa 1/0/7 - 8
 mls qos trust cos
 mls qos trust device cisco-phone
 priority-queue out
```
  
