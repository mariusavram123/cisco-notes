## Fabric Technologies

1. Software-Defined Access (SD-Access)

2. Software-Defined WAN (SD-WAN)

- A fabric network is an overlay network (virtual network [VN]) built over an underlay network (physical network) using overlay tunneling technologies such as VXLAN

- Fabric networks overcome shortcomings of traditional physical network by enabling host mobility, network automation, network virtualization and segmentation, and they are more manageable, flexible, secure (by means of encryption), and scalable than traditional networks

- The next generation fabric technologies:

    - Software-Defined Access (SD-Access) for campus networks

    - Software-Defined WAN (SD-WAN) for WAN networks

- The Cisco SD-Access fabric is one of the main components of the Cisco Digital Network Architecture (Cisco DNA)

- Cisco DNA is the solution for the future of intent-based networking in Cisco Enterprise Networks

- SD-Access provides policy-based network segmentation, host mobility for wired and wireless hosts, and enhanced security as well as other benefits in a fully automated fashion

- Cisco SD-Access was designed for enterprise campus and branch network environments and not for other types of network environments, such as data center, service provider, and WAN environments

- Traditional WANs are typically designed using MPLS or other overlay solutions, such as Dynamic Multipoint Virtual Private Network (DMVPN) or Intelligent WAN (IWAN) to provide connectivity between different campus and branch sites

- However, with the rise of Software as a Service (SaaS) such as Microsoft Office 365 and salesforce.com, and Infrastruture as a Service (IaaS) cloud services from Amazon Web Services (AWS), Google Compute Engine (GCE), and Microsoft Azure, traffic patterns are changing so that the majority of enterprise traffic flows to public clouds and the Internet

- Such changes are creating new requirements for security, application performance, cloud connectivity, WAN management, and operations that traditional WAN solutions were not designed to address

- The Cisco SD-WAN fabric is a cloud-based WAN solution for enterprise and data center networks that was developed to address all the new WAN requirements

### Software-Defined Access (SD-Access)

- There are many operational challenges in enterprise campus networks due to manual configuration of network devices

- Manual network configuration are slow and lead to misconfigurations that cause service disruptions in the network, and the situation is exacerbated in a constantly changing environment where more users, endpoints and applications are constantly being added

- The constant grouth in users and endpoints makes configuring user credentials and maintaining a consistent policy across the network very complex

- If policies are inconsistent, there is an added complexity involved in maintaining separate policies between wired and wireless networks that leaves the network vulnerable to security breaches

- As users move around the campus network, locating the users and troubleshooting issues also become more difficult

- In other words, traditional campus networks do not address the existing campus network needs

- With SD-Access, an evolved campus network can be built that addresses the needs of existing campus networks by leveraging the following capabilities, features and functionalities

    - **Network Automation**: SD-Access replaces manual network devices configurations with network device management through a single point of automation, orchestration, and management of network functions through the use of Cisco DNA center

    - This simplifies network design and provisioning and allows for very fast, lower-risk deployment of network devices and services using best-practice configurations

    - **Network assurance and analytics**: SD-Access enables proactive prediction of network-related and security-related risks by using telemetry to improve the performance of the network, endpoints and applications, including encrypted traffic

    - **Host mobility**: SD-Access provides host mobility for both wired and wireless clients

    - **Identity services**: Cisco Identity Services Engine (ISE) identifies users and devices connecting to the network and provides the contextual information required for users and devices to implement security policies for network access control and network segmentation

    - **Policy enforcement**: Traditional access control lists (ACLs) can be difficult to deploy, maintain, and scale because they rely on IP addresses and subnets

    - Creating access and application policies based on group-based policies using **Security Group Access Control Lists (SGACLs)** provides a much simpler and more scalable form of policy enforcement based on identity instead of an IP address

    - **Secure Segmentation**: With SD-Access, it is easier to **segment** the network to support guest, corporate, facilities and IOT-enabled infrastructure

    - **Network Virtualization**: SD-Access makes it possible to leverage a single phyisical infrastructure to support multiple virtual routing and forwarding (VRF) instances, referred to as virtual networks [VNs], which with a distinct set of access policies

#### What is SD-Access?

- SD-Access has two main components:

    1. Cisco Campus Fabric Solution

    2. Cisco DNA Center

- The campus fabric is a Cisco-validated fabric overlay solution that includes all the features and protocols (control plane, data plane, management plane, and policy plane) to operate the network infrastructure

- When the campus fabric solution is managed using the command line interface (CLI) or an **application programming interface (API)** using **Network Configuration Protocol (NETCONF)/YANG**, the solution is considered to be a campus fabric solution

- When the campus fabric solution is managed via the Cisco DNA Center, the solution is considered to be SD-Access

- SD-Access = Campus Fabric + Cisco DNA Center

![sd-access-architecture](./campus-fabric-and-cisco-dna-center.png)

#### SD-Access Architecture

- Cisco SD-Access is based on existing hardware and software technologies

- What makes Cisco SD-Access special is how these technologies are integrated and managed together

- The Cisco SD-Access fabric architecture can be divided into four basic layers, as illustrated below

![dna-center-in-sdwan](./dna-center-in-sdwan.png)

#### Physical Layer

- While Cisco SD-Access is designed for user simplicity, abstraction, and virtual environments everything runs on top of physical network devices - namely switches, routers, servers, wireless LAN controllers (WLCs), and wireless access points (APs)

- All Cisco network devices that actively participate in the SD-Access fabric must support all of the hardware application-specific integrated circuits (ASICs) and field-programable gate arrays (FPGAs) and software requirements described in the "Network Layer", below

- Cisco Access Layer switches that do not actively participate in the SD-Access fabric but that are part of it because of automation are referred to as SD-Access extension nodes

- The following are the physical layer devices of the SD-Access fabric:

    - **Cisco switches**: Switches provide wired (LAN) access to fabric. Multiple types of Cisco Catalyst switches are supported, as well as Nexus switches

    - **Cisco routers**: Routers provide WAN and branch access to the fabric

    - **Cisco wireless**: Cisco WLCs and APs provide wireless (WLAN) access to the fabric

    - **Cisco controller appliances**: Cisco DNA Center and Cisco ISE are the two controller appliances required

#### Network Layer

- The network layer consists of the underlay network and the overlay network

- These two sublayers work together to deliver data packets to and from the network devices participating in SD-Access

- All this network layer information is made available to the controller layer

- The network underlay is the underlaying physical layer, and it's sole purpose is to transport data packets between network devices for the SD-Access fabric overlay

- The overlay network is a virtual (tunneled) network that virtually interconnects all of the network devices forming a fabric of interconnected nodes

- It abstracts the inherent complexities and limitations of the underlay network
