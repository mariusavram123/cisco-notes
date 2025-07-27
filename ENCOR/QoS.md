## QoS

- The Need for QoS

- QoS models

- Classification and Marking

- Policing and Shaping

- Congestion Management and Avoidance

- QoS is a network infrastructure technology that relies on a set of tools and and mechanisms to assign different levels of priority to different IP traffic flows and provides special treatment to higher priority IP traffic flows

- For higher priority IP traffic flows, it reduces packet loss during times of network congestion and also helps control delay (latency) and delay variation (jitter); for low-priority IP traffic flows, it provides a best-effort delivery service

- This is analogous to how a high-occupancy vehicle (HOV) lane, also referred to as a carpool lane works: A special high priority lane is reserved for use of carpools (high-priority traffic), and those who carpool can now freely by bypassing the heavy traffic congestion in the adjacent general-purpose lanes

- Primary goals of implementing QoS on a network:

    - Expediting delivery for real-time applications

    - Ensuring business continuance for business-critical applications

    - Providing fairness for non-business-critical applications when congestion occurs

    - Establishing a trust boundary across the network edge to either accept or reject traffic markings injected by the endpoints

- Tools used by QoS to achieve the goals mentioned above:

    - Classification and marking

    - Policing and shaping

    - Congestion management and avoidance

### The Need for QoS

- Modern real-time multimedia applications such as IP telephony, telepresence, broadcast video, Cisco Webex and IP video surveillance are extremely sensitive to delivery delays and create unique quality of service (QoS) demands on a network

- When packets are delivered using a best-effort delivery model, they may not arrive in order or in a timely manner, and they may be dropped

- For video, this can result in pixelization of the image, pausing choppy video, audio and video being out of sync, or no video at all

- For audio, it could cause echo talker overlap (a walkie-talkie effect where only one person can speak at a time), uninteligible and disorted speech, voice breakups, longs silence gaps, and call drops

- The following are the leading causes of quality issues:

    - Lack of bandwidth

    - Latency and jitter

    - Packet loss

#### Lack of Bandidth

- The available bandwidth on the data path from the source to a destination equals the capacity of the lowest bandwidth link

- When the maximum capacity of the lowest bandwidth link is surpassed, link congestion takes place, resulting in traffic drops

- The obvious solution to this type of problem is to increase the link bandwidth capacity, but this is not always possible, due to budgetarry or technological constraints

- Another option is to implement QoS mechanisms such as policing and queuing to prioritize traffic according to level of importance

- Voice, video and business-critical traffic should get prioritized forwarding and sufficient bandwidth to support their application requirements, and the least important traffic should be allocated the remaining bandwidth

#### Latency and Jitter

- One-way end-to-end delay, also referred to as network latency, is the time it takes for packets to travel across a network from a source to a destination

- ITU Recommendation G.114 recommends that, regardless of the application type, a network latency of 400 ms should not be exceeded, and for real-time traffic network latency should be less than 150 ms; however, ITU and Cisco have demonstrated that real-time traffic quality does not begin to significantly degrade until network latency exceeds 200 ms

- To be able to implement these recommendations, it is important to understand what causes network latency

- Network latency can be broken down into fixed and variable latency:

    - Propagation delay (fixed)

    - Serialization delay (fixed)

    - Processing delay (fixed)

    - Delay variation (variable)

##### Propagation Delay

- Propagation delay is the time it takes for a packet to travel from source to a destination at the speed of light over a medium such as fiber-optic cables or copper wires

- The speed of light is 299,792,458 meters per second in a vacuum

- The lack of vacuum conditions in a fiber-optic cable or a copper wire slows down the speed of light by a ratio known as the refractive index; the larger the refractive index value, the slower light travels

- The average refractive index value of an optical fiber is about 1.5

- The speed of light through a medium v is equal to the speed of light in a vacuum c divided by the refractive index n or v = c / n

- This means that the speed of light through a fiber-optic cable with a refractive index of 1.5 is aproximatively 200,000,000 meters per second (that is 300,000,000 / 1.5)

- In a single fiber-optic cable with a refractive index of 1.5, were laid out around the equatorial circumference of Earth, which is about 40,075 km, the propagation delay would be equal to the equatorial circumference of earth divided by 200,000,000 meters per second

- This is aproximatively 200 ms, which would be an acceptable value even for real-time traffic

- Keep in mind that optical fibers are not always placed over the shortest path between two points

- Fiber-optic cables can be hundreds or even thousands of miles longer than expected

- In addition, other components required by fiber-optic cables, such as repeaters and amplifiers, may introduce additional delay

- A provider's service level agreement (SLA) can be reviewed to estimate and plan for the minimum, maximum and average latency for a circuit

- Sometimes it is necessary to use satellite communication for hard-to-reach locations

- The propagation delay for satellite circuits is the time it takes a radio wave travelling at the speed of light from the Earth's surface to a satellite (which could mean multiple satellite hops) and back to the Earth's surface; depending on the number of hops, this may surpass the recommended 400 ms

- For cases like this there is nothing that can be done to reduce the delay other than to try to find a satellite provider that offers lower propagation delays

#### Serialization Delay

- Serialization delay is the time it takes to place all the bits of a packet onto a link

- It is a fixed value that depends on the link speed; the higher the link speed the lower the delay

- The serialization delay s is equal to the packet size in bits divided by the line speed in bits per second

- For example the serialization delay for a 1500-bytes packet over an 1Gbps interface is 12 us and can be calculated as follows:

    - s = packet size in bits / line speed in bps

    - s = (1500 bytes x 8) / 1Gbps

    - 12,000 bits / 1000.000.000 bps = 0.000012 s x 1000 = .012 ms x 1000 = 12 us

#### Processing Delay

- Processing delay is the fixed ammount of time it takes for a networking device to take the packet from an input interface and place the packet into the output queue of the output interface

- The processing delay depends on factors such as the following:

    - CPU speed (for software-based platforms)

    - CPU utilization (load)

    - IP packet switching mode (process switching, software CEF or hardware CEF)

    - Router architecture (centralized or distributed)

    - Configured features on both input and output interfaces

#### Delay Variation

- Delay variation, also referred to as jitter, is the diference in latency between the packets in a single flow

- For example if one packet takes 50 ms to traverse the network from the source to destination, and the following packet takes 70 ms, the jitter is 20 ms

- The major factors affecting variable delays are queuing delay, dejitter buffers and variable packet sizes

- Jitter is experienced due to queuing delay experienced by packets during periods of network congestion

- Queuing delay depends on the number and sizes of packets already in the queue, the link speeds and the queuing mechanisms

- Queuing introduces unequal delays for packets of the same flow, thus producing jitter

- Voice and video endpoints typically come equipped with de-jitter buffers that can help smooth out changes in packet arrival due to jitter

- A de-jitter buffer is often dynamic and  can adjust for aproximatively 30 ms changes in arrival times of packets

- If a packet is not received within the 30 ms window allowed for by the de-jitter buffer, the packet is dropped, and this affects the overall voice or video quality

- To prevent jitter for high-priority real-time traffic, it is recommended to use queuing mechanisms such as low-latency queuing (LLQ) that allow matching packets to be forwarded prior to any other low priority traffic during periods of network congestion

#### Packet Loss

- Packet loss is usually a result of congestion on an interface

- Packet loss can be prevented by implementing one of the following approaches:

    - Increase link speed

    - Implement QoS congestion-avoidance and congestion-management mechanism

    - Implement traffic policing to drop low-priority packets and allow high-priority traffic through

    - Implement traffic shaping to delay packets instead of dropping them since traffic may burst and exceed the capacity of an interface buffer. Traffic shaping is not recommended for real-time traffic because it relies on queuing that can cause jitter

- Standard traffic shaping is unable to handle data bursts that occur on a microsecond time interval (that is, micro-bursts)

- Microsecond or low-burst shaping is required for cases where micro-bursts need to be smoothed out by a shaper

### QoS Models

- There are three different QoS implementation models:

    - **Best effort**: QoS is not enabled for this model. It is used for traffic that does not require any special threatment

    - **Intergrated Services (IntServ)**: Applications signal the network to make a bandwidth reservation and to indicate that they require special QoS treatment

    - **Differentiated Services (DiffServ)**: The network identifies classes that require special QoS treatment

- **The IntServ model** was created for real-time applications such as voice and video that require bandwidth, delay and packet-loss guarantees to ensure both predictable and guaranteed service levels

- In this model, applications signal they requirements to the network to reserve end-to-end resources (such as bandwidth) they require to provide an acceptable user experience

- IntServ uses Resource Reservation Protocol (RSVP) to reserve resources throughout a network for a specific application and to provide call admission control (CAC) to guarantee that no other IP traffic can use the reserved bandwidth

- The bandwidth by an application that is not used is wasted

- To be able to provide end-to-end QoS, all nodes, including the endpoints running the applications, need to support, build and maintain RSVP path state for every single flow

- This is the biggest drawback of IntServ because it means it cannot scale well on large networks that might have thousands or milions of flows due to large number of RSVP flows that would need to be maintained

- In the below figure we can see how RSVP issue bandwidth reservations

![rsvp-reservation](./rsvp-reservation-flow.png)

- On the above scheme each of the hosts in the left side (senders) are attempting to establish a one-to-one bandwidth reservation to each of the hosts on the right side (receivers)

- The senders start by sending RSVP PATH messages to the receivers along the same path used by regular data packets

- RSVP PATH messages carry the receiver source address, the destination address, and the bandwidth they wish to reserve

- This information is stored in RSVP path state for each node

- Once the RSVP PATH messages reach the receivers, each receiver sends RSVP reservation request (RESV) messages in the reverse path of the data flow toward the receivers, hop-by-hop

- At each hop, the IP destination address of a RESV message is the IP address of the previous-hop node obtained from the RSVP path state of each node

- As RSVP RESV messages cross each hop, they reserve bandwidth on each of the links for the traffic flowing from the receiver to the sender hosts

- If bandwidth reservations are required from the hosts on the right side to the hosts on the left side, the hosts on the right side need to follow the same procedure of sending RSVP PATH messages, which doubles the RSVP state on each networking device in the data path

- This demonstrates how RSVP state can increase quickly as more hosts reserve bandwidth

- Apart from the scalability issues, long distances between hosts could also trigger long bandwidth reservation delays

- **DiffServ** was designed to address the limitations of the best-effort and IntServ models

- With this model there is no need for a signalling protocol, and there is no RSVP flow state to maintain on every single node, which makes it highly scalable; QoS characteristics (such as bandwidth and delay) are managed on an hop-by-hop basis with QoS policies that are defined independently at each device in the network

- DiffServ is not considered an end-to-end QoS solution because end-to-end QoS guarantees cannot be enforced

- DiffServ divides IP classes and marks it based on business requirements so that each of the classes can be assigned a different level of service

- As IP traffic traverses a network, each of the network devices identifies the packet class by it's marking and services the packets according to it's class

- Many levels of service can be chosen with DiffServ

