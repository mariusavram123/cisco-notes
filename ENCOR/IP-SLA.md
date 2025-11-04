## IP SLA

- IP SLA is a is a tool built into Cisco IOS software that allows for the continuous monitoring of various aspects of the network

- The different types of probes that can be configured to monitor traffic within a network environment include the following:

    - Delay (both round-trip and one-way)

    - Jitter (directional)

    - Packet loss (directional)

    - Packet sequencing (packet ordering)

    - Path (per hop)

    - Connectivity (directional)

    - Server or website download time

    - Voice quality scores

- IP SLA has proven to be a useful tool because it provides a variety of flexible monitoring options

- Typically, any SLA received from a service provider only monitors or guarantees the traffic as it flows across the service provider's network

- This doesn't provide an end-to-end SLA - or visibility for that matter

- However, IP SLA is a robust tool that can help with troubleshooting

- Below is shown a scenario and illustrates why IP SLA provides more visibility than a typical service provider SLA

![typical-service-provider-sla](./typical-service-provider-sla.png)

- There are many options and probes available for IP SLA

- We will focus only on the ICMP and HTTP operations of the IP SLA

- The ICMP echo operation can functionally be thought of as testing reachability by leveraging ICMP echo and echo replies or pings

- Below is illustrated how the ICMP echo operation works in IP SLA

![ip-sla-icmp-echo](./ip-sla-icmp-echo-operation.png)

- To configure any IP SLA operation the following command should be used to enter the IP SLA configuration mode:

```
conf t
 ip sla <operation-nr>
```

- Here, the operation number is the configuration for the individual IP SLA probe

- This is necessary because there can be multiple IP SLA instances configured on a single device, all doing different operations or verification tasks

- Configure the IP SLA operation for ICMP echo:

```
conf t
 ip sla 1
  icmp-echo <destnation-ip-address | destination-hostname> source-ip <ip-address | hostname> | source-interface <interface-name>
```

- The next step is to specify how often the ICMP echo operation should run

- It can be done as follows:

```
conf t
 ip sla 1
  frequency <seconds>
```

- Note that many additional optional parameters are available for configuring IP SLA

- 