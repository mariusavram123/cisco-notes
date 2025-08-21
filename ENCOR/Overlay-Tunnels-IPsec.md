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

    - **Tunnel Mode**: Encrypts the entire original packet and adds a new set of IPsec headers. These new headers are used to route the packet and also provide overlay functions

    - **Transport Mode**: Encrypts and authenticates only the packet payload. This mode does not provide overlay functions and routes based on the original IP headers

- Below we can see an original packet, an IPsec packet in transport mode, and an IPsec packet in tunnel mode

![orig-packet](./original-packet.png)

![ipsec-transport-mode](./ipsec-transport-mode.png)

![ipsec-tunnel-mode](./ipsec-tunnel-mode.png)

- IPsec supports the following encryption, hashing, and keying methods to provide security services:

    - **Data Encryption Standard (DES)**: A 56-bit symmetric data encryption algorithm that can encrypt the data sent over a VPN. This algorithm is very weak and should be avoided

    - **Triple DES (3DES)**: A data encryption algorithm that runs the DES algorithm 3 times with 3 different 56-bit keys. Using this algorithm is no longer recommended. The more advanced and more efficient AES should be used instead

    - **Advanced Encryption Standard (AES)**: A symmetric encryption algorithm used for data encryption that was developed to replace DES and 3DES. AES supports key lengths of 128 bits, 192 bits or 256 bits and is based on Rijndael algorithm

    - **Message Digest 5 (MD5)**: A one-way, 128-bit hash algorithm used for data authentication. Cisco devices use MD5 HMAC, which provides an additional layer of protection against MiTM attacks. Using this algorithm is no longer recommended, and SHA should be used instead

    - **Secure Hash Algorithm (SHA)**: A one-way, 160-bit hash algorithm used for data authentication. Cisco devices use the SHA1-HMAC, which provides additional protection against MiTM attacks

    - **Diffle-Hellman (DH)**: An asymmetric key exchange protocol that enables two peers to establish a secret key used by encryption algorithms such as AES over an unsecure communication channel. A DH group refers to the length of the key (modulus size) to use a DH key exchange. For example group 1 uses 768 bits, group 2 uses 1024, and group 5 uses 1536, where the larger the modulus, the more secure it is. The purpose of DH is to generate shared secret symmetric keys that are used by the two VPN peers for symmetrical algorithms, such as AES. The DH eschange itself is asymmetrical and CPU intensive, and the resulting shared secret keys that are generated are symmetrical. Cisco recommends avoiding DH groups 1, 2 and 5 and instead use DH groups 14 and higher

    - **RSA Signatures**: A public-key (digital certificate) cryptographic system used to mutually authenticate the peers

    - **Pre-Shared Key**: A security mechanism in which a locally configured key is used as a credential to mutually authenticate the peers

### Transform Sets

- A transform set is a combination of security protocols and algorithms

- During the IPsec SA negotiation, the peers agree to use a particular transform set for protecting a particular data flow

- When such a transform set is found, it is selected and applied to the IPsec SAs on both peers

- The allowed transform sets combination

```
Transform type                          Transform                               Description

Authentication Header transform         ah-md5-hmac                             Authentication Header with the MD5 algorithm (not recommended)
(only one allowed)

                                        ah-sha-hmac                             Authentication Header with the SHA authentication algorithm

                                        ah-sha256-hmac                          Authentication Header with the 256-bit AES authentication algorithm

                                        ah-sha384-hmac                          Authentication Header with the 384-bit AES authentication algorithm

                                        ah-sha512-hmac                          Authentication Header with the 512-bit AES authentication algorithm

ESP encryption transform                esp-aes                                 ESP with the 128-bit AES encryption algorithm
(only one allowed)
                                        esp-gcm                                 ESP with either 128-bit (default) or a 256-bit encryption algorithm
                                        esp-gmac

                                        esp-aes192                              ESP with the 192-bit AES encryption algorithm

                                        esp-aes256                              ESP with the 256-bit AES encryption algorithm

                                        esp-des                                 ESP with 56-bit and 168-bit DES encryption (no longer recommended)
                                        esp-3des

                                        esp-null                                ESP with null encryption algorithm

                                        esp-seal                                ESP with the 160-bit SEAL encryption algorithm

ESP authentication transform            esp-md5-hmac                            ESP with the MD5 (HMAC variant) authentication algorithm (no longer)
(only one allowed)                                                              recommended

                                        esp-sha-hmac                            ESP with the SHA (HMAC variant) authentication algorithm

IP compression transform                comp-lzs                                IP compression with the Lempel-Zis-Stac (LZS) algorithm
```

- The authentication header and ESP algorithms cannot be specified on the same transform set in Cisco IOS-XE releases

### Internet Key Exchange (IKE)

- Internet Key Exchange (IKE) is a protocol that performs authentication between two endpoints to establish security associations (SAs), also known as IKE tunnels

- These security associations, or tunnels, are used to carry control plane and data plane traffic for IPsec

- There are two versions of IKE: IKEv1 (specified in RFC 2709) and IKEv2 (specified in RFC 7296)

- IKEv2 was developed to overcome the limitations of IKEv1 and provides many improvements over IKEv1's implementation

- For example, it supports EAP (certificate-based authentication), has anti-DoS capabilities and needs fewer messages to establish an IPsec SA

- Understanding IKEv1 is still important because some legacy infrastructures have not yet migrated to IKEv2 or have devices or features that don't support IKEv2

#### IKEv1

- Internet Security Association Key Management Protocol (ISAKMP) is a framework for authentication and key exchange between two peers to establish, modify and tear down SAs

- It is designed to support many different kinds of key exchanges

- ISAKMP uses UDP port 500 for communication between peers

- IKE is the implementation of ISAKMP using the Oakley and Skeme key exchange techniques

- Oakley provides perfect forward secrecy (PFS) for keys, identity protection, and authentication

- Skeme provides anonymity, repudiability, and quick key refreshment

- For Cisco platforms, IKE is analogous to ISAKMP, and the two therms are used interchangeabily

- IKEv1 provides two phases of key negotiation for IKE and IPsec SA establishement:

    - **Phase 1**: Establishes a bidirectional SA between two IKE peers, known as ISAKMP SA. Because the SA is unidirectional, once it is established, either peer may initiate negotiations for phase 2

    - **Phase 2**: Establishes unidirectional IPsec SA, leveraging the ISAKMP SA established in phase 1 of the negotiation

- Phase 1 negotiation can occur using main mode (MM) or aggresive mode (AM). The peer that initiates the SA is known as the initiator, and the other peer is known as the receiver

- Main mode consists of six message exchanges and tries to protect all information during the negotiation so that no information is exposed to eavesdropping

    - **MM1** - this is the first message that the initiator sends to a responder. One or multiple SA proposals are offered, and the responder needs to match one of them for this phase to succeed

    - The SA proposals include different combinations of the following:

        - **Hash Algorithms**: MD5 or SHA

        - **Encryption Algorithms**: DES (bad), 3DES (better but not recommended), or AES (best)

        - **Authentication Key**: Pre-Shared key or digital certificates

        - **Diffie-Hellman (DH) group**: Group 1, 2, 5 and so on

        - **Lifetime**: How long until this IKE phase 1 tunnel must be torn down (default is 24 hours). This is the only parameter that does not have to exactly match with the other peer to be accepted. If the lifetime is different, the pers agree to use the smallest lifetime between them

    - **MM2**: This message is sent from the responder to the initiator with the SA proposal that it matches

    - **MM3**: In this message, the initiator starts the DH key exchange. This is based on the DH group the responder matches in the proposal

    - **MM4**: The responder sends it's own key to the initiator. At this point, encryption keys have been shared, and encryption is established for IPsec SA

    - **MM5**: The initiator starts authentication by sending the peer router it's IP address

    - **MM6**: The responder sends a similar packet and authenticates the session. At this point the ISAKMP SA is established

- When main mode is used, the identities of the two IKE peers are hidden

- Although this mode of operation is very secure, it takes longer than aggresive mode to complete the negotiation

- Aggresive mode consists of a three-message exchange and takes less time to negotiate keys between peers; however it does not offer the same level of encryption security provided by main mode negotiation, and the identities of the two peers trying to establish a security association are exposed to eavesdropping

- These are three aggresive mode messages:

    - **AM1**: In this message the initiator sends all the information contained in MM1 through MM3 and MM5

    - **AM2**: This message sends all the same information contained in MM2, MM4 and MM6

    - **AM3**: This message sends the authentication that is contained in MM5

- Main mode is slower than aggresive mode, but main mode is more secure and more flexible because it can offer an IKE peer more security proposals than aggresive mode

- Aggresive mode is less flexible and not as secure, but it is much faster

- Phase 2 uses the existing bidirectional IKE SA to securely exchange messages to establish one or more IPsec SAs between the two peers

- Unlike the IKE SA, which is a single bidirectional SA, a simple IPsec SA negotiation results in two unidirectional IPsec SAs, one on each peer

- The method used to establish the IPsec SA is known as quick mode

- Quick mode uses a three-message exchange:

    - **QM1**: The initiator (which could be either peer) can start multiple IPsec SAs in a single exchange message. This message includes agreed-upon algorithms for encryption and integrity decided as part of phase 1, as well as what traffic is to be encrypted or secured

    - **QM2**: This message from the responder has matching IPsec parameters

    - **QM3**: After this message, there should be two unidirectional IPsec SAs between the two peers


