## Enterprise Network Architecture

1. Hierarchical LAN Design Model

2. High Availability Network Design

3. Enterprise Network Architecture Options

- Enterprise campus networks provide access to network services and resources to end users and endpoints spread over a single geographical location

- Campus networks typically support many different kinds of endpoint connectivity for workers and guest users, such as laptops, PCs, mobile phones, IP phones, printers, and video conferencing systems

- A small campus network environment might span a single floor or a single building, while a larger campus network might span a large group of buildings spread over an extended geographic area

- Large campus networks must have a core or backbone for interconnectivity to other networks, such as the campus end-user/endpoint access, the data center, the private cloud, the public cloud, the WAN, and the Internet edge

- The largest enterprises might have multiple campus networks distributed worldwide, each providing the end-user access and core network connectivity

- The enterprise campus architecture is designed to meet the needs of organizations that range from small single building or remote site to a large, multibuilding location

### Hierarchical LAN Design Model

- A hierarchical LAN design model divides the enterprise network architecture into modular layers

- By breaking up the design into modular layers, you can have each layer to implement specific functions

- These modular layers can be easily replicated throughout the network, which simplifies the network design and provides an easy way to scale the network as well as a consistent deployment method

- A hierarchical LAN design avoids the need for a flat and fully meshed network in which all nodes are interconnected

- In fully meshed network architectures, network changes tend to affect a large number of systems

- Hierarchical design provides fault containment by constraining the network changes to a subset of the network, which affects fewer systems and makes it easy to manage as well as improve resiliency

- In a modular layer design, network components can be placed or taken out of service with little or no impact to the rest of the network; this facilitates troubleshooting, problem isolation and network management

- The hierarchical LAN design divides networks or their modular blocks into the following three layers:

    - **Access Layer**: Gives endpoints and users direct access to the network

    - **Distribution Layer**: Provides an aggregation point for the access layer and acts as a services and control boundary between the access layer and the core layer

    - **Core Layer (also referred to as the backbone)**: Provides connections between distribution layers for large environments

![hierarchical-lan-design](./hierarchical-lan-design.png)

- Each layer provides different functionalities and capabilities to the network

- The number of layers needed depends on the characteristics of the network deployment site

- As illustrated below, a small campus in a single building might require only access and distribution layers, whereas a campus that spans multiple buildings will most likely require all three layers

- Regardless of how many layers are implemented at a geographic location, the modularity of this design ensures that each layer will provide the same services and the same design methods

![modular-design-scalability](./modular-design-scalability.png)

#### Access Layer

- The *access layer*, also commonly referred as the *network edge*, is where end user devices or endpoints connect to the network 

- It provides high-bandwidth device connectivity using wired and wireless access technologies such as GigabitEthernet and 802.11n, 802.11ac, and 802.11ax wireless

- While endpoints in most cases will not use the full capacity of these connections for extended periods of time, the ability to burst up to these high bandwidths when required helps improve the quality of experience (QoE) and productivity of the end user

- Below, the different types of endpoints that connect to the access layer, such as personal computers (PCs), IP phones, printers, wireless access points, personal telepresence devices, and IP video surveillance cameras

- Wireless access points and IP phones are prime examples of devices that can be used to extend the access layer one more layer out from the access switch

![access-layer-connectivity](./access-layer-connectivity.png)

- The access layer can be segmented (for example, by using VLANs) so that different devices can be placed into different logical networks for performance, management and security reasons

- In the hierarchical LAN design, the access layer switches are not interconnected to each other

- Communication between endpoints on different access layer switches occurs through the distribution layer

- Because the access layer is the connection point for endpoints, it plays a big role in ensuring that the network is protected from malicious attacks

- This protection includes making sure the end users and endpoints connecting to the network are prevented from accessing services for which they are not authorized

- Furthermore, the quality of service (QoS) trust boundary and QoS mechanisms are typically enabled on this layer to ensure that QoS is provided end-to-end to satisfy the end user's QoE

- For business-critical endpoints that can connect to only a single access switch, it is recommended to use access switches with redundant supervisor engines to prevent service outages

#### Distribution Layer

- The primary function of the distribution layer is to aggregate access layer switches in a given building or campus

- The distribution layer provides a boundary between the Layer 2 domain of the access layer and the core's Layer 3 domain

- This boundary provides two key functions on the LAN:

- On the Layer 2 side, the distribution layer creates a boundary for Spanning Tree Protocol (STP), limiting propagation of Layer 2 faults, and on the Layer 3 side, the distribution layer provides a logical point to summarize IP routing information when it enters the core of the network 

- The summarization reduces IP routing tables for easier troubleshooting and reduces protocol overhead for faster recovery from failures

- Below is illustrated the distribution layer

- The distribution switches need to be deployed in pairs for redundancy

- The distribution layer switch pairs should be interconnected to each other using either a Layer 2 or Layer 3 link

![distribution-layer](./distribution-layer.png)

- In a large campus environment, multiple distribution layer switches are often required when access layer switches are located in multiple geographically dispersed buildings to reduce the number of fiber-optic runs (which are costly) between buildings

- Distribution layer switches can be located in various buildings, as illustrated below

![distribution-layer-between-switches](./distribution-switches-between-buildings.png)

#### Core Layer

- As networks grow beyond three distribution layers in a single location, organizations should consider using a core layer to optimize the design

- The core layer is the backbone and aggregation point for multiple networks and provides scalability, high availability, and fast convergence to the network

- The core can provide high-speed connectivity for large enterprises with multiple campus networks distributed worldwide, and it can also provide interconnectivity between the end-user/endpoint campus access layer and other network blocks, such as the data center, the private cloud, the public cloud, the WAN, the Internet edge, and network services

- The core layer reduces the network complexity, from N (N - 1) to N links for N distributions, as shown below

![core-layer](./core-layer.png)

### High Availability Network Design

- In networking, high availability refers to a resilient network that can operate with continuous uptime without failure, for a given period of time, to ensure business continuity

- High availability can be achieved by designing a network that takes into consideration network- and system-level components

- The following guidelines can be used in the network design for network-level high availability:

    - Adding redundant devices and links at different layers of the network architecture

    - Ensuring the design has no single points of failure and it is fault tolerant

    - Simplifying the network design by using virtual network clustering technologies

    - Implementing network monitoring systems to analyze all aspects of the network, such as network capacity, faulty hardware, and security threats to prevent low network performance, network failures and outages

- The following guidelines can be used in the network design for system-level high availability:
