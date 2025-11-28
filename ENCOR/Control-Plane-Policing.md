## Control Plane Policing (CoPP)

- A **control plane policing (CoPP)** policy is a QoS policy that is applied to traffic to or sourced by the router's control plane CPU

- CoPP policies are used to limit known traffic to a given rate while protecting the CPU from unexpected extreme rates of traffic that could impact the stability of the router

- Typically CoPP implementations use only an input policy that allows traffic to the control plane to be policed to a desired rate

- In a properly planned CoPP policy, network traffic is placed into various classes, based on the type of traffic (management, routing protocols or known IP addresses)

- The CoPP policy is then implemented to limit traffic to the control plane CPU to a specific rate for each class
