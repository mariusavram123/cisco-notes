## Cisco WLC controller configuration 

- Create dynamic interfaces:

    - Controller -> Interfaces -> New

        - Interface name: Internal
        
        - VLAN ID: 100
        
        - Apply
        
        - Enter IP address, netmask, gateway, DHCP server address 
        
        - Apply
        
    - Controller -> Interfaces -> New
    
        - Interface name: Guest
        
        - VLAN ID: 200
        
        - Apply
        
        - Enter IP address, netmask, gateway, DHCP server address
        
        - Apply
        

- Configure WLANs:

    - WLANs -> Click on the WLAN ID (number 1) on the left 
    
    - Interface -> Interface groups -> Map the Internal WLAN with the "Internal" interface
    
    - Security -> Layer 2 Security -> Authentication key management -> Turn off 802.1X and select PSK
    
    - Format ASCII and set up the PSK (password) - password should have 8 letters or more
    
    - Apply

    - QoS tab -> Quality of service -> Silver (best effort)
    
    - Advanced -> (scroll down) Flexconnect local switching 
    
    - Apply (to finish editing the WLAN)
    
- Create new -> Go

    - Type -> WLAN
    
    - Profile Name -> Guest
    
    - SSID -> Guest
    
    - ID -> 2
    
    - Apply
    
    - Status: Enabled
    
    - Inteface: Guest
    
    - Security -> Layer 2 Security -> Authentication key management -> Turn off 802.1X and select PSK
    
    - Format ASCII and set up the PSK
    
    - Apply
    
- Monitoring

    - Clients (to see the list of clients)
    
- Wireless

    - Click on an AP name and check the settings
    
    - Mode (the mode of the AP) 
    
- Management 

    - See the list of allowed/enabled protocols (SNMP, syslog, HTTP, HTTPS, telnet)
    
    - Mgmt via Wireless -> Check the box and then click Apply
    
    
- Security

    - Access control lists -> New 
    
    - Name: MANAGEMENT_ACL 
    
    - ACL type: IPv4
    
    - Apply
    
    - Add new rule
    
    - Sequence number
    
    - Source -> 192.168.1.0 255.255.255.0
    
    - Destination -> 192.168.1.100 255.255.255.255
    
    - Apply
    
    - Added 2 more rules in this ACL (second rule: allow mgmt from 10.0.0.0/24, third rule: deny all traffic)
    
    - CPU access control lists:
    
        - Enable CPU ACL (enabled)
        
        - ACL name: MANAGEMENT_ACL
        
        
    
