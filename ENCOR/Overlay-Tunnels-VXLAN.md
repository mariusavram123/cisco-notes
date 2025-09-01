## Virtusl Extensible Local Area Network (VXLAN)

- Server virtualization has placed increased demands on the lwgacy network infrastructure

- A bare-metal server now has multiple virtual machines (VMs) and containers, each with it's own MAC address

- This has led to a number of problems with traditional Layer 2 networks, such as the following:

    - The 12-bit VLAN ID yelds 4000 VLANs, which are insufficient for server virtualization

    - Large MAC address tables are needed due to hundreds of thousands of VMs and containers attached to the network

    - STP blocks links to avoid loops, and this results in a large number of disabled links, which is unacceptable

    - ECMP is not supported

    - Host mobility is difficult to implement

- VXLAN is an overlay data plane encapsulation scheme that was developed to address the various issues seen in traditional Layer 2 networks

- It extends Layer 2 and Layer 3 overlay networks over a Layer 3 underlay network, using MAC-in-IP/UDP tunneling

- Each overlay is termed a VXLAN **segment**

- The Internet Assigned Numbers Authority (IANA) assigned to VXLAN the UDP destination port 4789

- There may be some older/prestandard implementations of VXLAN that are using the UDP destination port 8472

- The reason for this discrepancy is that when VXLAN was first implemented in Linux, the VXLAN UDP destination port had not yet been officially assigned, and Linux decided to use port 8472 because many vendors at that time were using UDP destination port 8472

- Later, IANA assigned port 4789 for VXLAN, and to avoid breaking some existing deployments, some Linux distributions decided to leave port 8472 as the default value

- Be sure to check which is the right port to use when dealing with multiple vendor interoperability situations

![vxlan-packet-format](./vxlan-packet-format.png)

- Unlike the VLAN ID, which has only 12 bits and allows for 4000 VLANs, VXLAN has a 24-bit VXLAN Network Identifier (VNI), which allows for up to 16 million VXLAN segments (most commonly known as overlay networks), to coexist within the same infrastructure

- The VNI is located in the VXLAN shim header that encapsulates the original inner MAC frame originated by an endpoint

- The VNI is used to provide segmentation for Layer 2 and Layer 3 traffic

- To facilitate the discovery of VNIs over the underlay Layer 3 network, virtual tunnel endpoints (VTEPs) are used

- VTEPs are entities that originate or terminate VXLAN tunnels

- They map Layer 2 and Layer 3 packets to the VNI to be used in the overlay network

- Each VTEP has two interfaces:

    - **Local LAN interfaces**: These interfaces on the local LAN segment provide bridging between local hosts


    - **IP interface**: This is a core-facing interface for VXLAN. The IP interface's IP address helps identify the VTEP in the network

    - It is also used for VXLAN traffic encapsulation and de-encapsulation

- The VXLAN VTEP with IP interface and the local LAN interface:

![VXLAN-VTEP](./VXLAN-VTEP.png)

- Devices that are not capable of supporting VXLAN and need to use traditional VLAN segmentation can be connected to VXLAN segments by using a VXLAN gateway

- A VXLAN gateway is a VTEP device that combines a VXLAN segment and a classic VLAN segment into one common Layer 2 domain

- The VXLAN standard defines VXLAN as a data plane protocol, but it does not define a VXLAN control plane; it was left open to be used with any control plane

- Currently four different VXLAN control and data planes are supported by Cisco devices:

    - VXLAN with Multicast Underlay

    - VXLAN with static unicast VXLAN tunnels

    - VXLAN with MP-BGP EVPN control plane

    - VXLAN with LISP control plane

- MP-BGP EVPN and Multicast are the most popular control planes used in data centers and private cloud environments

- For campus environments, VXLAN with a LISP control plane is the preferred choice

- Cisco Software-Defined Access (SD-Access) is an example of implementation of VXLAN with the LISP control plane

- An interesting fact is that the VXLAN specification originated from a Layer-2 LISP specification (draft-smith-lisp-layer2-00) that aimed to introduce Layer 2 segmentation support to LISP

- The VXLAN specification introduced the term VXLAN in liew of Layer-2 LISP and didn't port over some of the fields from the Layer 2 LISP specification into the VXLAN specification

- The minor differences between the Layer 2 LISP specification and the VXLAN specification headers are the following:

![l2-lisp-vs-vxlan-packets](./l2-lisp-and-vxlan-packet-comparison.png)

- Fields that were not ported over from Layer 2 LISP into VXLAN were reserved for future use

- As you can see above, LISP encapsulation is only capable of performing IP-in-IP/UDP encapsulation, which allows it to support Layer 3 overlays only, while VXLAN encapsulation is capable of encapsulating the original Ethernet header to perform MAC-in-IP encapsulation, which allows it to support Layer 2 and Layer 3 overlays





## What is VXLAN?

- What problems does VXLAN solve?

- When should it be deployed?

- VXLAN solves some of the scalability problems involved with Layer 2 infrastructures

- Virtually all networks (big or small) are subdivided in small virtual LANs (VLANs) - these are layer 2 subdivisions of networks into segments

- Each VLAN will typically be assigned it's own IP address subnet

- VLANs are identified within a network using their VLAN ID

- VLAN IDs in a 802.1Q frame header is a 12-bit number

![dot-1q-vlan-header](./dot1q-vlan-header.png)

- VLAN ID values range from 0 to 4095

- The problem arise when we apply VLANs to cloud infrastructures and large datacenters

- The demand for more VLANs has increased with the rise of certralized server infrastructure, the rise of cloud computing and the virtualization of physical server resources into multiple VMs or containers

- In this case 4096 VLANs are not enough anymore

- In some situations we should deliver hundreds of thousands or milions of layer 2 domains

- VXLAN is used in this case

- Another used for VXLAN - to avoid the need for Spanning Tree Protocol to block redundant links

- Traditional Layer 2 switches require the use of some type of Spanning Tree Protocol

- This is a protocol that is used to ensure that a Layer 2 topology will not create any Layer 2 loops

- STP will block some of the interfaces of the switches to prevent Layer 2 loops

- This is vital for a Layer 2 network to function

- As the scale of the network increases, the number of idle links due to spanning tree blocking them increases

- In datacenters, with 25, 40, or 100 Gbps links - imagine them just sitting idle

- This is a huge waste of bandwidth and money

- The use of VXLAN also solves the ineficiency introduced by Spanning Tree, and ensure that no links remain idle

- The third problem that VXLAN solve has to do with MAC address table sizes

![vxlan-mac-addr-table-sizes](./vxlan-mac-address-table-sizes.png)

- You may run multiple servers or containers on the same physical server 

- In this case the switches serving that servers will have to learn hundreds of MAC addresses and will have to populate their MAC address tables accordingly

- Switches will have to learn many MAC addresses on a single switch port

![multiple-racks-with-switches](./multiple-racks-tor-switches.png)

- This situation will result in the accumulation of enormous ammount of MAC addresses in the MAC address tables of each on of these switches

- This is likely to be due to the large number of virtual devices that the MAC addresses being exchanged will very quickly overhelm the capacity of the switch's memory

- What is VXLAN, what does it look like?

- VXLAN is a network virtualization technology used to extend Layer 2 networks over Layer 3 networks

![vxlan-as-virtualization-technology](./vxlan-1.png)

- At the very heart of VXLAN is the concept of an overlay and an underlay network

- VXLAN creates an overlay network by encapsulating ethernet frames within UDP packets

![vxlan-encapsulation](./vxlan-encapsulation.png)

- This allows for creation of virtual layer 2 networks over a layer 3 network

- The underlay network's principal function is to transfer packets from point A to point B in a network

- It operates exclusively at layer 3 without any layer 2 involvement

- By using Layer 3 we can implement an IGP like OSPF or EIGRP so we can distribute traffic across that whole infrastructure

- Overlay and underlay networks essentially operate independently 

- The overlay network is virtual and it depends on the underlay network but modifications on the overlay network do not impact the underlay network

- You can add/remove links in the underlay network as long as your routing protocol can reach the destination, that way the overlay network will remain unaffected

- VXLAN essentially provides the flexibility to span virtual networks across different physical locations making it easier to manage and move virtual machines without being constraint by the physical network topology

- VXLAN was born out of necessity, the need to overcome the scalability issues involved with more traditional layer 2 networks

- VXLAN is an open standard described in RFC 7342

### VNIs, VTEPs and VXLAN architecture

- What is a VNI?

- VNI = VXLAN Network Identifier

- Similar functions to VLANs

- Uniquely identifies a Layer 2 segment or domain

- VNI is represented using a 24-bit number - resulting in over 16 million values

- Compare to 12-bit VLAN ID - over 4000 values - this is a huge increase

- VXLAN actually encapsulates Layer 2 frames within UDP datagrams

- When this is done, there is an extra VXLAN header that is added to the frame

- The VNI value is contained within the VXLAN header

- What is a VTEP?

- VTEP = VXLAN Tunnel EndPoint

- This is the device at which VXLAN encapsulation and de-encapsulation takes place

- This device is connected to the underlay network 

- It creates the tunneling mechanism for VXLAN

- VXLAN was created primarly for use in datacenters and cloud-based infrastructure, where there are many virtual machines and containers

- VTEPs can be either software-based or hardware-based

- Software-based VTEPs are those software switches that are typically used within an hypervisor that host the end virtual devices

- Hypervisors have software switches dealing with the network connectivity for the virtual machines and containers that it hosts

![vtep-virtual-switch](./vtep-virtual-switch.png)

- Switch exists only as software process connecting VMs and containers

- The software switch can be a VTEP

- VTEP can also be hardware-based

![vtep-hardware-based](./vtep-hardware-based-tor-switch.png)

- They can be configured within a hardware switch 

- In that case, the location at which encapsulation and de-encapsulation take place is in the hardware switch itself

- The VTEP functionality is something that you enable and configure within your hardware or software switch

- Configuration using Cisco switches -> hardware VTEPs configuration

- The configuration principles are the same for software VTEPs as well

![vxlan-topology](./vxlan-topology.png)

- In the topology - the entire topology is logically operating as a huge layer 2 switch, that can be segmented into millions of layer 2 segments

- Let's say that we want to create 3 VNIs, three segments, to be interconnected over this topology

![vxlan-segmented-3-segments](./vxlan-segmented.png)

- Each VTEP will have 2 interfaces that are involved in the process of tunneling:

    - VTEP IP interface: Physical layer 3 interface connected to the Underlay network. As long as IP connectivity is available between VTEP IP interfaces, then we can have VXLAN connectivity

    - VNI interfaces: Logical interfaces that correspond to the VNIs being terminated on VTEP. These are similar to switched virtual interfaces (SVIs)

- VNI interfaces - SW1:

    - VNI 6501

    - VNI 6503

- A VTEP can be configured with multiple VNI interfaces

- Each of these VNI interfaces, is associated with the same VTEP IP interface

- Multiple VNIs are tunneled through the same physical interface, much like a trunk

- Each VNI configured in a VTEP, essentially creates a separate layer 2 segment

![vxlan-encapsulation](./vxlan-encapsulation-infrastr.png)

- Data which is encapsulated in an IP packet, which is then encapsulated into an Ethernet frame

- This frame is a Layer 2 entity, and it is then encapsulated into a UDP datagram

- Before adding a UDP header, we first add a VXLAN header

- The VXLAN header is 8 bytes in length

![vxlan-header-structure](./vxlan-header-structure.png)

- First byte contains a flags field, where the I flag (the 5th bit), must always be set to 1 for any valid VNI

- The other 7 bits of the first byte, are reserved fields for future use and must be set to 0 on transmission, and also be ignored by the receiving VTEP

- The next 24 bits are also reserved for future use

- Then it comes the VNI field itself, this is a 24-bit field. Here the value of the VNI is stored

- For the duration of the transmission of the frame, over the VXLAN infrastructure, this is the field that tells the VTEPs to which VNI this frame belongs

- It is added upon encapsulation at ingress on the source VTEP and it is read and removed upon egress on the destination VTEP

- The last byte at the end of the VXLAN header, which is also reserved

### VXLAN - Encapsulation, Headers and Packet Transmission Process

- 

