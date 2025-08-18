## IPsec fundamentals

- IPsec is a framework of open standards for creating highly secure virtual private networks (VPNs) using various protocols and technologies for secure communication across unsecure networks, such as the Internet

- IPsec tunnels provide the security services as listed below:

```
Security service                        Description                                     Methods used

Peer Authentication                     Verifies the identity of the VPN                Pre-Shared Key (PSK)
                                        peer through authentication                     Digital certificates

Data confidentiality                    Protects data from eavesdropping attacks        Data Encryption Standard (DES)
                                        through encryption algorithms. Changes          Triple DES (3DES)
                                        plaintext into encrypted cyphertext             Advanced Encryption Standard (AES)
                                                                                        The use of DES and 3DES is not recommended

Data integrity                          Prevents man-in-the-middle (MITM) attacks       Hash Message Authentication Code (HMAC)
                                        by ensuring that data has not been tampered     - Message Digest 5 (MD5) algorithm
                                        with during it's transit across an unsecure     - Secure Hash Algorithm (SHA-1, SHA-2)
                                        network                                         The use of MD5 is not recommended

Replay detection                        Prevents MITM attacks where an attacker         Every packet si marked with a unique sequence number
                                        captures VPN traffic and replays it back        A VPN device keeps track of the sequence number and does
                                        to a VPN peer with the intention of building    not accept a packet with a sequence number it has already
                                        an illegitimate VPN tunnel                      processes
```

- IPsec uses two different packet headers to deliver the security services mentioned above

    - Authentication header

    - Encapsulating Security Payload (ESP)

### Authentication Header (AH)

- The IP Authentication Header provides data integrity, authentication, and protection from hackers replaying packets

- The authentication header ensures that the original data packet (before encapsulation) has not been modified during transport on the public network

- It created a digital signature similar to a checksum to ensure that the packet has not been modified, using protocol number 51 located in the IP header

- The authentication header does not support encryption (data confidentiality) and NAT traversal (NAT-T), and for this reason it's use is not recommended, unless authentication is all it's desired

### Encapsulating Security Payload (ESP)

- Encapsulation Security Payload (ESP) provides data confidentiality, authentication, and protection from hackers replaying packets

- Typically, payload refers to the actual data minus any headers, but in the context of ESP, the payload is the portion of the original packet that is encapsulated within the IPsec headers

- ESP ensures that the original payload (before encapsulation) maintains data confidentiality by encrypting the payload and adding a new set of headers during transport across a public network

- ESP uses the protocol number 50, located in the IP header

- Unlike the authentication header, ESP provides data confidentiality and supports NAT-T

- Traditional IPsec provides two modes for packet transport:

    - **Tunnel Mode**:

    - **Transport Mode**:

