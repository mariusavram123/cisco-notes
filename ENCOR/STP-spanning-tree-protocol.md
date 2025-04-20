## Spanning Tree Protocol

1. Spanning Tree Protocol Fundamentals

2. Rapid Spanning Tree Protocol

3. Advanced STP tunning

4. Multiple Spanning Tree Protocol


### Spanning Tree Protocol Fundamentals

- Spanning Tree Protocol (STP) enables switches to become aware of other switches through the advertisement and receipt of Bridge Protocol Data Units (BPDUs)

- STP builds a Layer 2 loop-free topology in an environment by temporarly blocking traffic on redundant ports.

- STP operates by selecting a specific switch as the master switch and running a tree-based algorithm to identify which redundant ports should not forward traffic

- STP iterations:

	- 802.1D - the original specification
	
	- Per-VLAN Spanning Tree (PVST)
	
	- Per-VLAN Spanning Tree Plus (PVST+)
	
	- 802.1W - Rapid Spanning Tree Protocol (RSTP)

	- 802.1S - Multiple Spanning Tree Protocol (MST)

- Catalyst switches operate in PVST+, RSTP, and MST modes. All three of these modes are backwards compatible with 802.1D

### 802.1D STP

- 802.1D STP provides support for ensuring a loop-free topology for one VLAN. 

- In 802.1D standard every port transitions through the following states:

	- **Disabled**: The port is in an administratively off position (Shut down)
	
	- **Blocking**: The switch port is enabled, but the port does not forward any traffic to ensure that a loop is not created.
		
		- The switch does not modify the MAC address table
		
		- It can only receive BPDUs from other switches
	
	- **Listening**: The switch port has transitioned from a blocked state and now can send or receive BPDUs
		
		- It cannot forward any other network traffic
		
		- The MAC address table cannot be modified 
		
		- The duration of the state is correlated to STP forwarding time
		
	- **Learning**: The switch can now modify the MAC address table with any network traffic that it receives
	
		- The switch does not forward any other network traffic besides BPDUs
		
		- The duration of the state correlates with STP forwarding time
		
	- **Forwarding**: The switch can forward all network traffic and can update the MAC address table as expected
	
		- Thid is the final state of a switch port to forward network traffic
		
	- **Broken**: The switch has detected a configuration or an operational problem that can have major effects.
	
		- The port discards packets as long as the problem continues to exist
		
- The entire 802.1D STP initialization time takes about 30 seconds for a port to enter the forwarding state using default timers

- 802.1D Port Types:

	- **Root Port**(RP): A port that connects to the root bridge or an upstream switch in the spanning-tree topology
	
		- There should be only one Root port per VLAN on a switch
		
	- **Designated Port**(DP): A port that receives and forwards BPDU frames to other switches
	
		- Designated ports provide connectivity to downstream devices and switches 
		
		- There should be only one active designated port on a link
		
	- **Blocking Port**(BP): A port that is not forwarding traffic because of STP calculations

- STP terminology

	- **Root Bridge**: The root bridge is the most important switch in the Layer 2 topology
	
		- All ports are in a forwarding state on root bridge
		
		- The switch is considered the top of the spanning tree for all path calculations by other switches
		
		- All ports on the Root Bridge are categorized as Designated ports
		
	- **Bridge Protocol Data Unit**(BPDU): This network packet is used for network switches to identify a hierarchy and notify of changes in the topology
	
		- A BPDU uses destination MAC address 01:80:c2:00:00:00
		
		- There are 2 types of BPDUs:
		
			- **Configuration BPDU**: This type of BPDU is used to identify the root bridge, root ports, designated ports and blocking ports
			
				- The configuraton BPDU consist of the following fields: STP type, root path cost, root bridge identifier, local bridge identifier, max age, hello time and forward delay
				
			- **Topology change notification(TCN) BPDU**: This type of BPDU is used to communicate changes in the layer 2 topology to other switches
			
	- **Root path cost**: This is the combined cost for a specific path towards the root switch
	
	- **System priority**: This 4-bit value indicates the preference for a switch to be the root bridge. The default value is 32768.
	
	- **System ID extension**: This 12-bit value indicates the VLAN that the BPDU correlates to. The system priority and system ID extension are combined as part of the switch's identification as the root bridge.
	
	- **Root Bridge Identifier**: This is a combination of root bridge system MAC address, system ID extension, and system priority of the root bridge
	
	- **Local Bridge Identifier**: This is a combination of local switch's bridge system MAC address, system ID extension, and system priority of the root bridge
	
	- **Max Age**: This is the maximum length of time that passes before a bridge port saves it's BPDU information. 
	
		- The default value is 20 seconds
		
		- This can be configured with the command:
		```
		conf t
		 spanning-tree vlan <id> max-age <maxage>
		```
		
		- If a switch loses contact with the BPDU's source, it assumes it assumes the BPDU information is still valid for the duration of Max Age timer
		
	- **Hello Time**: This is the time that a BPDU is avertised out of a port
	
		- The default value is 2 seconds
		
		- Can be configured from 1 to 10 seconds with the command:
		```
		conf t
		 spanning-tree vlan <id> hello-time <hello-time>
		```
	- **Forward delay**: This is the ammount of time that a port stays in listening and learning state
	
		- The default value is 15 seconds
		
		- Can be changed to a value between 15 to 30 seconds with the command:
		```
		conf t
		 spanning-tree vlan <id> forward-time <forward-time>
		```

### Spanning Tree Path cost

- The interface cost is an essential component for root path calculation because root path is found based on cummulative interface STP cost to reach the root bridge

- The interface STP cost was originally stored as 16-bit value with a reference value of 20 Gbps. As swithes have developed with higher-speed interfaces, 10Gbps may not be enough

- Another method, called long mode, uses a 32-bit value and uses a reference speed of 20 Tbps.

- The original method, called short mode is the default mode

- Path cost chart

![Path cost chart](./STP-cost-chart.png)

- Devices can be configured with the long-mode interface cost with the command:

```
conf t
 spanning-tree pathcost method long
```

- The entire Layer 2 topology SHOULD use the same setting for every device in the environment to ensure a consistent topology.

### Building the STP topology

- In the topology the configuration of all switches does not include any customizations for STP

- The focus is primarly for VLAN 1 but VLANs 10, 20 and 99 also exist in the topology

![STP topology](./basic-stp-topology.png)

### Root bridge election

- The first step with STP is to identify the root bridge

- As a switch initializes, it assumes that it is the root bridge and uses the local bridge identifier and the root bridge identifier

- Then it listens to it's neighbor's configuration BPDU and does the following:

	- If the neighbor's configuration BPDU is inferior to it's own BPDU, the switch ignores that BPDU
	
	- If the neighbor's configuration BPDU is preferred to it's own BPDU, the switch updates it's BPDUs to include the new root bridge identifier along with a new root path cost that correlates to the total path cost to reach the new root bridge. This process continues until all switches in a topology have identified the new root bridge switch.
	
- STP deems a switch more preferrable if the priority of the bridge identifier is lower than the priority of other switch's configuration BPDUs

- If the priority is the same, then the switch prefers the BPDU with the lowest system MAC

- Generally older switches have a lower MAC address and are considered more preferable 

- Configuration changes can be made for optimizing placement of the root switch in a Layer 2 topology

- In our topology. SW1 can be identified as root bridge because it's system MAC address (0062.ec9d.c500) is the lowest in the topology

- You can verify which is the spanning tree root using the following command:

```
show spanning-tree root
```

- The output includes the VLAN number, root bridge identifier, root path cost, hello time, max age time, and forwarding delay

- Because SW1 is the root bridge, all ports are designated ports so the Root Port field is empty

- This is one way to verify that the connected switch is the root switch for the VLAN

- Root bridge priority for VLAN 1 is 32769 and not 32768. The priority in the configuration BPDU packets is actually the priority plus the value of sys_id_ext(which is the VLAN number)

- Can be confirmed by looking at VLAN 10 which haves priority 32778, which is 10 higher than 32768

![Command output](./spanning-tree-root.png)

- The advertised root path cost is always the value calculated on the local switch

- As the BPDU is received, the local root path cost is the advertised root path cost plus the local interface port cost

- The root path cost is always 0 on the root bridge

![Path advertisements](./path-cost-advertisements.png)

### Locating root ports

- After the switches have identified the root bridge they must determine their root ports (RP)

- The root bridge continue to advertise configuration BPDUs out of all it's ports

- The switch compares the BPDU information to identify the root port(RP)

- RP selection logic (the next criterion is used in the event of a tie)

	1. The interface associated with the **lowest path cost** to the root bridge is more preferred
	
	2. The interface associated to the **lowest system priority of the advertising(neighbor)** switch is preferred next
	
	3. The interface associated to the **lowest system MAC address of the advertising(neighbor)** switch is preferred next
	
	4. When multiple links are associated to the same switch, the **lowest port priority from the advertising(neighbor)** switch is preffered (lowest neighbor port priority)
	
	5. When multiple links are associated to the same switch, the **lowest port number from the advertising(neighbor)** switch is preferred
	
- The root bridge can be identified for a specific VLAN using the command `show spanning-tree root` and examining the CDP or LLDP neighbor information to identify the host name of the RP switch

### Locating Blocked Designated Switch Ports

- Now that the root bridge and RPs have been identified, all other ports are considered designated ports

- However if two non-root switches are connected to each-other on their designated ports, one of these switch ports must be set to a blocking state to prevent a forwarding loop

- In our topology there will be the following links:

	- SW2 Gi1/0/3 -> SW3 Gi1/0/2
	
	- SW4 Gi1/0/5 -> SW3 Gi1/0/4
	
	- SW4 Gi1/0/6 -> SW5 Gi1/0/5
	
- The logic to calculate which ports should be blocked between two non-root switches is the following:

	1. The interface is a designated port and must not be considered an RP
	
	2. The switch with the **lowest path cost** to the root bridge forwards packets and the one with the higher path cost blocks
	
	3. The **system priority of the local switch** is compared with the **system priority of the remote switch**. The local port is moved to a blocked state if the **remote system priority is lower** than that of the local switch
	
	4. The **system MAC address of the local switch** is compared to the **system MAC address of the remote switch**. The local designated port is moved to a blocked state if the remote system MAC address is lower than that of the local switch. If the links are connected to the same switch they move on to the next step (lowest port number of the neighbor switch)
	
- All three links (SW2 Gi10/3 -> SW3 Gi1/0/2, SW4 Gi1/0/5 -> SW5 Gi1/0/4, SW4 Gi1/0/6 -> SW5 Gi1/0/5) would use step 4 of the process just listed to identify which ports will move to a blocking state

- SW3 Gi1/0/2, SW5 Gi1/0/5 and SW5 Gi1/0/6 ports will all transition to a blocking state because the MAC addresses are lower for SW2 and SW4

- The command `show spanning-tree vlan <id>` provides useful information for locating the port states

- These port types are expected on Catalyst switches:

	- **Point-to-point (P2P)**: This port type connects to another network device (PC or RSTP switch)
	
	- **P2P edge**: This port type specifies that portfast is enabled on this port
	
- If on the command `show spanning-tree vlan <id>`, the type field includes *TYPE_Inc-, this indicates a port configuration mismatch between the Catalyst switch and the switch it is connected to.

- Common issues are the port type being incorrect and the port mode (access vs trunk) being misconfigured

![Type Inc](./stp-type-inc.png)

- Assigning a port type for a interface

```
conf t
 interface e0/2
  spanning-tree link-type point-to-point # or
  spanning-tree link-type shared # usually shared is used if the port is connected to a hub
```

- In our topology all ports on SW2 are in a forwarding state, but port Gi1/0/2 on SW3 is in a blocking (BLK) state

- Specifically SW3's G1/0/2 has been designated as an alternate port to reach the root in the event that Gi1/0/1 connection fails

- The reason that SW3's Gi1/0/2 port rather than SW2 Gi1/0/3 was placed into a blocking state is that SW2's system MAC address(0081.c4ff.8d00) is lower than SW3's system MAC address(189c.5d11.9980) 

- This can be deduced by looking at the system MAC address in the output of `show spanning-tree vlan 1` command

### Verification of VLANs on trunk links

- All interfaces that participate in a VLAN are listed in the output of the command `show spanning-tree`.

- Using this command can be a daunting task for trunk ports that carry multiple VLANs

- The output includes the STP state for every VLAN on an interface for every switch interface

- The command `show spanning-tree interface <interface_id> <detail>` reduces the output to the STP state for the specified interface

- The optional `detail` keyword provides information on port cost, port priority, number of transitions, link type and count of BPDUs send or received for every VLAN supported on that interface

- If a VLAN is missing from a trunk port you can check the trunk port configuration for accuracy: `show interfaces trunk`

- A common problem is that a VLAN may be missing from the allowed VLANs list on that trunk interface

### STP topology changes

