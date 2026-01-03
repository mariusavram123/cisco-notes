## Syslog

- Devices can generate a tremendous amount of useful information, including messages sent to the console, to the logging buffer, and to off-box `syslog` collectors

- In fact, all three can be sent the same or different message types

- By default, all syslog messages are sent to the console

- (This is how the debug commands from before are displayed on the console port)

- However, this can be adjusted, as can what messages are sent to the login buffer or off-box syslog collector

- It is critical to note that prior to configuring any device to send log information, the date and time of the clock *must* be properly configured for accurate time

- If it is not, the time stamps on all the logging messages will not reflect the appropriate and accurate time, which will make troubleshooting much more difficult because you will not be able to correlate issues with the logs using the time stamps generated

- Ensuring that NTP is configured properly helps with this issue

- Messages that are generated have specific severity levels associated with them, but these levels can be changed

- The default severity level for each message type is listed below

```
Local keyword                       Level                           Description                             syslog definition

emergencies                         0                               System unstable                         LOG_EMERG

alerts                              1                               Immediate action needed                 LOG_ALERT

critical                            2                               Critical Conditions                     LOG_CRIT

errors                              3                               Error conditions                        LOG_ERR

warnings                            4                               Warning conditions                      LOG_WARNING

notification                        5                               Normal but significant conditions       LOG_NOTICE

informational                       6                               Informational messages only             LOG_INFO

debugging                           7                               Debugging messages                      LOG_DEBUG
```

- These messages can be used to provide valuable information to the network operations staff, so they can be so overwhelming that they make it difficult to sift through to find or pinpoint an issue

- It is important to note that having syslog configured doesn't mean that an issue will be found

- It still takes the proper skill to be able to look at the messages and determine the root cause of the issue

- However, syslog is helpful in guiding you toward the issue at hand

- The logging buffer is the first area to focus on

- On a router, R1 you can enable logging to the buffer as follows:

    1. Enable logging to the buffer

    2. Set the severity level of syslog messages to send to the buffer

    3. Set the logging buffer to a large size

- The `logging buffered ?` command is issued from the global configuration mode to see the available options

- Below is shown the list of available options:

```
R1(config)#logging buffered ?
  <0-7>              Logging severity level
  <4096-2147483647>  Logging buffer size
  alerts             Immediate action needed           (severity=1)
  critical           Critical conditions               (severity=2)
  debugging          Debugging messages                (severity=7)
  discriminator      Establish MD-Buffer association
  emergencies        System is unusable                (severity=0)
  errors             Error conditions                  (severity=3)
  filtered           Enable filtered logging
  informational      Informational messages            (severity=6)
  notifications      Normal but significant conditions (severity=5)
  warnings           Warning conditions                (severity=4)
  xml                Enable logging in XML to XML logging buffer
  <cr>               <cr>
```

- It is important to note that you can configure the severity level by simply specifying the level with a number from 0 to 7 or the name of severity (listed next to the severity level number)

- The default size of the logging buffer is 4096 bytes

- This size can get overwritten quite quickly

- It is good practice to expand the buffer size so that you can capture more logging information

- Debugging or severity 7 is the level that will be configured below; with this configuration, any debugging can be sent to the logging buffer instead of the console, which makes working on a device and troubleshooting less daunting because the debugging doesn't interfere with the console output - that is, as long as the debugging level is not set on the console as well

- Below, the logging is configured to debugging level 7, and it is set to 100000 bytes

- The `do show logging` command is then run to confirm the changes

- Notice the syslog message that shows the logging size was changed

```
R1(config)#logging buffered 1000000
*Oct 30 20:08:16.602: %SYS-5-LOG_CONFIG_CHANGE: Buffer logging: level debugging, xml disabled, filtering disabled, size (100000)
R1(config)#logging buffered debugging
*Oct 30 20:08:34.992: %SYS-5-LOG_CONFIG_CHANGE: Buffer logging: level debugging, xml disabled, filtering disabled, size (8192)
```

```
R1(config)#do sh logging           
Syslog logging: enabled (0 messages dropped, 3 messages rate-limited, 0 flushes, 0 overruns, xml disabled, filtering disabled)

No Active Message Discriminator.



No Inactive Message Discriminator.


    Console logging: level debugging, 40 messages logged, xml disabled,
                     filtering disabled
    Monitor logging: level debugging, 0 messages logged, xml disabled,
                     filtering disabled
    Buffer logging:  level debugging, 1 messages logged, xml disabled,
                    filtering disabled
    Exception Logging: size (8192 bytes)
    Count and timestamp logging messages: disabled
    Persistent logging: disabled

No active filter modules.

    Trap logging: level informational, 44 message lines logged
        Logging Source-Interface:       VRF Name:

Log Buffer (1000000 bytes):

*Oct 30 20:11:12.527: %SYS-5-LOG_CONFIG_CHANGE: Buffer logging: level debugging, xml disabled, filtering disabled, size (1000000)
```

- Below is shown how to disable console logging and run `debug ip ospf hello` command followed by the `show logging` command to reveal the debugging on R1

```
R1(config)#no logging console
R1#debug ip ospf hello 
```

```
R1#show logging 
Syslog logging: enabled (0 messages dropped, 2 messages rate-limited, 0 flushes, 0 overruns, xml disabled, filtering disabled)

No Active Message Discriminator.



No Inactive Message Discriminator.


    Console logging: disabled
    Monitor logging: level debugging, 0 messages logged, xml disabled,
                     filtering disabled
    Buffer logging:  level debugging, 34 messages logged, xml disabled,
                    filtering disabled
    Exception Logging: size (4096 bytes)
    Count and timestamp logging messages: disabled
    Persistent logging: disabled
    Trap logging: level informational, 51 message lines logged
        Logging Source-Interface:       VRF Name:

Log Buffer (1000000 bytes):

*Oct 31 19:19:56.656: %SYS-5-LOG_CONFIG_CHANGE: Buffer logging: level debugging, xml disabled, filtering disabled, size (1000000)
*Oct 31 19:20:18.426: %SYS-5-CONFIG_I: Configured from console by console
*Oct 31 19:20:29.680: %SYS-5-LOG_CONFIG_CHANGE: Console logging disabled
*Oct 31 19:20:44.134: %SYS-5-CONFIG_I: Configured from console by console
*Oct 31 19:20:51.344: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:20:52.792: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:20:53.198: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:20:55.470: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:20:57.444: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:20:58.647: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:21:00.478: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:21:02.113: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:21:02.794: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:21:05.387: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:21:06.508: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:21:07.890: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:21:09.582: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:21:11.399: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:21:12.698: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:21:15.188: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:21:16.364: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:21:17.626: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:21:18.706: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:21:20.673: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:21:22.371: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:21:24.754: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:21:25.803: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:21:27.240: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:21:28.301: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:21:30.256: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:21:31.645: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:21:34.339: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:21:35.743: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:21:36.368: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
R1#un all
All possible debugging has been turned off
```

- If a network operations team wanted to send these same logs to a off-box collector, that could be configured as well

- By default, these messages are sent to the logging host through UDP port 514, but this can be changed if necessary

- Configuring logging to a host is similar to configuring logging on the console or buffer

- It this case, it is configured by using the following steps:

    1. Enable logging to host 192.168.144.100

    2. Set the severity level of syslog messages to send to the host

- Below is shown the basic configuration for syslog messages to a collector or host from R1

```
R1(config)#logging host 192.168.144.100

R1(config)#logging trap 7
```

```
R1(config)#do sh logg            
Syslog logging: enabled (0 messages dropped, 2 messages rate-limited, 0 flushes, 0 overruns, xml disabled, filtering disabled)

No Active Message Discriminator.



No Inactive Message Discriminator.


    Console logging: disabled
    Monitor logging: level debugging, 0 messages logged, xml disabled,
                     filtering disabled
    Buffer logging:  level debugging, 92 messages logged, xml disabled,
                    filtering disabled
    Exception Logging: size (4096 bytes)
    Count and timestamp logging messages: disabled
    Persistent logging: disabled
    Trap logging: level debugging, 106 message lines logged
        Logging to 192.168.144.100  (udp port 514, audit disabled,
              link up),
              41 message lines logged, 
              0 message lines rate-limited, 
              0 message lines dropped-by-MD, 
              xml disabled, sequence number disabled
              filtering disabled
        Logging Source-Interface:       VRF Name:

Log Buffer (1000000 bytes):

*Oct 31 19:19:56.656: %SYS-5-LOG_CONFIG_CHANGE: Buffer logging: level debugging, xml disabled, filtering disabled, size (1000000)
*Oct 31 19:20:18.426: %SYS-5-CONFIG_I: Configured from console by console
*Oct 31 19:20:29.680: %SYS-5-LOG_CONFIG_CHANGE: Console logging disabled
*Oct 31 19:20:44.134: %SYS-5-CONFIG_I: Configured from console by console
*Oct 31 19:20:51.344: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:20:52.792: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:20:53.198: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:20:55.470: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:20:57.444: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:20:58.647: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:21:00.478: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:21:02.113: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:21:02.794: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:21:05.387: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:21:06.508: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:21:07.890: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:21:09.582: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:21:11.399: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:21:12.698: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:21:15.188: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:21:16.364: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:21:17.626: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:21:18.706: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:21:20.673: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:21:22.371: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:21:24.754: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:21:25.803: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:21:27.240: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:21:28.301: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:21:30.256: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:21:31.645: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:21:34.339: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:21:35.743: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:21:36.368: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:21:37.905: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:21:39.668: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:21:41.609: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:31:44.289: %SYS-6-TTY_EXPIRE_TIMER: (exec timer expired, tty 0 (0.0.0.0)), user 
*Oct 31 19:36:30.946: %LINK-3-UPDOWN: Interface Ethernet0/3, changed state to up
*Oct 31 19:36:31.945: %LINEPROTO-5-UPDOWN: Line protocol on Interface Ethernet0/3, changed state to up
*Oct 31 19:42:17.418: %SYS-5-CONFIG_I: Configured from console by console
*Oct 31 19:47:37.533: %OSPF-5-ADJCHG: Process 1, Nbr 4.4.4.4 on Ethernet0/1 from LOADING to FULL, Loading Done
*Oct 31 19:47:56.707: %OSPF-5-ADJCHG: Process 1, Nbr 4.4.4.4 on Ethernet0/1 from FULL to DOWN, Neighbor Down: Interface down or detached
*Oct 31 19:47:56.712: %OSPF-5-ADJCHG: Process 1, Nbr 4.4.4.4 on Ethernet0/1 from LOADING to FULL, Loading Done
*Oct 31 19:48:10.063: %OSPF-5-ADJCHG: Process 1, Nbr 7.7.7.7 on Ethernet0/2 from FULL to DOWN, Neighbor Down: Interface down or detached
*Oct 31 19:48:10.063: %OSPF-5-ADJCHG: Process 1, Nbr 4.4.4.4 on Ethernet0/1 from FULL to DOWN, Neighbor Down: Interface down or detached
*Oct 31 19:48:10.063: %OSPF-5-ADJCHG: Process 1, Nbr 2.2.2.2 on Ethernet0/0 from FULL to DOWN, Neighbor Down: Interface down or detached
*Oct 31 19:48:10.065: %OSPF-5-ADJCHG: Process 1, Nbr 7.7.7.7 on Ethernet0/2 from LOADING to FULL, Loading Done
*Oct 31 19:48:10.065: %OSPF-5-ADJCHG: Process 1, Nbr 4.4.4.4 on Ethernet0/1 from LOADING to FULL, Loading Done
*Oct 31 19:48:10.065: %OSPF-5-ADJCHG: Process 1, Nbr 2.2.2.2 on Ethernet0/0 from LOADING to FULL, Loading Done
*Oct 31 19:50:01.880: %SYS-6-LOGGINGHOST_STARTSTOP: Logging to host 192.168.144.100 port 0 CLI Request Triggered
*Oct 31 19:50:02.880: %SYS-6-LOGGINGHOST_STARTSTOP: Logging to host 192.168.144.100 port 514 started - CLI initiated
*Oct 31 19:51:31.024: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:51:34.968: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:51:35.442: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:51:38.240: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:51:38.301: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:51:39.018: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:51:39.119: OSPF-1 HELLO Et0/3: Send hello to 224.0.0.5 area 0 from 192.168.144.1
*Oct 31 19:51:40.802: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:51:44.255: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:51:45.213: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:51:47.366: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:51:47.473: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:51:48.232: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:51:48.655: OSPF-1 HELLO Et0/3: Send hello to 224.0.0.5 area 0 from 192.168.144.1
*Oct 31 19:51:49.915: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:51:53.909: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:51:54.440: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:51:57.052: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:51:57.057: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:51:57.936: OSPF-1 HELLO Et0/3: Send hello to 224.0.0.5 area 0 from 192.168.144.1
*Oct 31 19:51:58.196: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:51:59.708: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:52:03.217: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:52:04.096: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:52:06.177: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:52:06.913: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:52:07.631: OSPF-1 HELLO Et0/3: Send hello to 224.0.0.5 area 0 from 192.168.144.1
*Oct 31 19:52:07.910: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:52:09.393: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:52:12.970: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:52:13.724: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:52:16.013: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
*Oct 31 19:52:16.038: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:52:17.296: OSPF-1 HELLO Et0/2: Send hello to 224.0.0.5 area 0 from 192.168.17.1
*Oct 31 19:52:17.404: OSPF-1 HELLO Et0/3: Send hello to 224.0.0.5 area 0 from 192.168.144.1
*Oct 31 19:52:19.285: OSPF-1 HELLO Et0/0: Rcv hello from 2.2.2.2 area 0 192.168.12.2
*Oct 31 19:52:22.098: OSPF-1 HELLO Et0/1: Rcv hello from 4.4.4.4 area 0 192.168.14.4
*Oct 31 19:52:23.660: OSPF-1 HELLO Et0/2: Rcv hello from 7.7.7.7 area 0 192.168.17.7
*Oct 31 19:52:25.048: OSPF-1 HELLO Et0/0: Send hello to 224.0.0.5 area 0 from 192.168.12.1
*Oct 31 19:52:25.391: OSPF-1 HELLO Et0/1: Send hello to 224.0.0.5 area 0 from 192.168.14.1
```

- The power of using syslog is evident even in these basic examples

- It can be used to notify of power supply failures, CPU spikes, and a variety of other things

- It is important not to underestimate the level of granularity and detail that can be achieved by setting up proper notification policies in a network

- It is ultimately up to the network operations team to determine how deep is appropriate to meet the business's needs

- Many options are available, such as multiple logging destinations and ways to systematically set up different levels of logging

- It all depends on what the network operations team feel is appropriate for their environment

- Syslog server on debian 13 with syslog-ng:

```
sudo apt install syslog-ng
```

- Create custom file to store the logs from remote clients on (/etc/syslog-ng/conf.d/custom.conf):

```
cat /etc/syslog-ng/conf.d/custom.conf 
# =========================
# === SYSLOG-NG CONFIG ===
# =========================

# ======= OPTIONS =======
options {
   keep-hostname(yes);
   use-dns(no);
   create-dirs(yes);
   owner("splunk");
   dir-owner("splunk");
   group("splunk");
   dir-group("splunk");
   perm(0750);
   dir-perm(0755);
};

# ======= SOURCES =======
source s_udp_514 {
   network(transport("udp") port(514));
};

source s_tcp_514 {
   network(transport("tcp") port(514));
};

# ======= FILTERS =======
filter f_cisco_iosv {
   host(172.16.29.16) or host(172.16.29.16);
};

# ======= DESTINATIONS =======
# Write Cisco IOSv logs to disk
destination d_cisco_iosv {
   file("/syslog-data/cisco-iosv/$HOST/$HOST-$YEAR$MONTH$DAY$HOUR.log");
};

# ======= LOG RULE =======
log {
   source(s_udp_514);
   filter(f_cisco_iosv);
   destination(d_cisco_iosv);
   flags(final);
};

# =========================
# === CATCH-ALL CONFIG ===
# =========================

# ======= DESTINATIONS =======
# Catchall for TCP sources
destination d_catchall_tcp {
   file("/syslog-data/catchall_tcp/$HOST/$HOST-$YEAR$MONTH$DAY-$HOUR.log");
};

# Catchall for UDP sources
destination d_catchall_udp {
   file("/syslog-data/catchall_udp/$HOST/$HOST-$YEAR$MONTH$DAY-$HOUR.log");
};

# ======= LOG CATCH-ALL RULES =======
log {
   source(s_tcp_514);
   destination(d_catchall_tcp);
   flags(final);
};

log {
   source(s_udp_514);
   destination(d_catchall_udp);
   flags(final);
};

```

- Create splunk user:

```
adduser splunk
```

- Start the syslog-ng service:

```
systemctl restart syslog-ng.service
```

- Viewing the logs from the devices (on router: `debug ip bgp events` and `debug ip bgp updates`):

```
less /syslog-data/cisco-iosv/172.16.29.16/172.16.29.16-2025110109.log

Nov  1 09:13:47 172.16.29.16 %SYS-5-CONFIG_I: Configured from console by console
Nov  1 09:14:26 172.16.29.16 BGP: Regular scanner timer event
Nov  1 09:14:26 172.16.29.16 BGP: Performing BGP general scanning
Nov  1 09:14:26 172.16.29.16 BGP: tbl IPv4 Unicast:base Performing BGP Nexthop scanning for general scan
Nov  1 09:14:26 172.16.29.16 BGP(0): Future scanner version: 25, current scanner version: 24
Nov  1 09:14:26 172.16.29.16 BGP: tbl IPv4 Multicast:base Performing BGP Nexthop scanning for general scan
Nov  1 09:14:26 172.16.29.16 BGP(6): Future scanner version: 26, current scanner version: 25
Nov  1 09:14:26 172.16.29.16 BGP: tbl L2VPN E-VPN:base Performing BGP Nexthop scanning for general scan
Nov  1 09:14:26 172.16.29.16 BGP(10): Future scanner version: 26, current scanner version: 25
Nov  1 09:14:26 172.16.29.16 BGP: tbl MVPNv4 Unicast:base Performing BGP Nexthop scanning for general scan
Nov  1 09:14:26 172.16.29.16 BGP(15): Future scanner version: 26, current scanner version: 25
Nov  1 09:14:59 172.16.29.16 BGP: aggregate timer expired
Nov  1 09:15:07 172.16.29.16 BGP: aggregate timer expired
Nov  1 09:15:26 172.16.29.16 BGP: Regular scanner timer event
Nov  1 09:15:26 172.16.29.16 BGP: Performing BGP general scanning
Nov  1 09:15:26 172.16.29.16 BGP: tbl IPv4 Unicast:base Performing BGP Nexthop scanning for general scan
Nov  1 09:15:26 172.16.29.16 BGP(0): Future scanner version: 26, current scanner version: 25
Nov  1 09:15:26 172.16.29.16 BGP: tbl IPv4 Multicast:base Performing BGP Nexthop scanning for general scan
Nov  1 09:15:26 172.16.29.16 BGP(6): Future scanner version: 27, current scanner version: 26
Nov  1 09:15:26 172.16.29.16 BGP: tbl L2VPN E-VPN:base Performing BGP Nexthop scanning for general scan
Nov  1 09:15:26 172.16.29.16 BGP(10): Future scanner version: 27, current scanner version: 26
Nov  1 09:15:26 172.16.29.16 BGP: tbl MVPNv4 Unicast:base Performing BGP Nexthop scanning for general scan
Nov  1 09:15:26 172.16.29.16 BGP(15): Future scanner version: 27, current scanner version: 26
Nov  1 09:15:35 172.16.29.16 BGP: aggregate timer expired
Nov  1 09:15:44 172.16.29.16 BGP: aggregate timer expired
Nov  1 09:16:26 172.16.29.16 BGP: Regular scanner timer event
Nov  1 09:16:26 172.16.29.16 BGP: Performing BGP general scanning
Nov  1 09:16:26 172.16.29.16 BGP: tbl IPv4 Unicast:base Performing BGP Nexthop scanning for general scan
Nov  1 09:16:26 172.16.29.16 BGP(0): Future scanner version: 27, current scanner version: 26
Nov  1 09:16:26 172.16.29.16 BGP: tbl IPv4 Multicast:base Performing BGP Nexthop scanning for general scan
Nov  1 09:16:26 172.16.29.16 BGP(6): Future scanner version: 28, current scanner version: 27
Nov  1 09:16:26 172.16.29.16 BGP: tbl L2VPN E-VPN:base Performing BGP Nexthop scanning for general scan
Nov  1 09:16:26 172.16.29.16 BGP(10): Future scanner version: 28, current scanner version: 27
Nov  1 09:16:26 172.16.29.16 BGP: tbl MVPNv4 Unicast:base Performing BGP Nexthop scanning for general scan
Nov  1 09:16:26 172.16.29.16 BGP(15): Future scanner version: 28, current scanner version: 27
Nov  1 09:17:28 172.16.29.16 %SYS-5-CONFIG_I: Configured from console by console
Nov  1 09:18:13 172.16.29.16 BGP(0): 10.12.1.2 rcv UPDATE about 10.3.3.3/32 -- withdrawn
Nov  1 09:18:13 172.16.29.16 BGP(0): no valid path for 10.3.3.3/32
Nov  1 09:18:13 172.16.29.16 BGP(0): 10.12.1.2 rcv UPDATE about 10.4.4.4/32 -- withdrawn
Nov  1 09:18:13 172.16.29.16 BGP(0): no valid path for 10.4.4.4/32
Nov  1 09:18:13 172.16.29.16 BGP: topo global:IPv4 Unicast:base Remove_fwdroute for 10.3.3.3/32
Nov  1 09:18:13 172.16.29.16 BGP(0): no valid path for 10.3.3.3/32
Nov  1 09:18:13 172.16.29.16 BGP(0): 10.12.1.2 rcv UPDATE about 10.4.4.4/32 -- withdrawn
Nov  1 09:18:13 172.16.29.16 BGP(0): no valid path for 10.4.4.4/32
Nov  1 09:18:13 172.16.29.16 BGP: topo global:IPv4 Unicast:base Remove_fwdroute for 10.3.3.3/32
Nov  1 09:18:13 172.16.29.16 BGP: topo global:IPv4 Unicast:base Remove_fwdroute for 10.4.4.4/32
Nov  1 09:18:13 172.16.29.16 BGP(0): 10.12.1.2 rcv UPDATE about 10.23.1.0/24 -- withdrawn
Nov  1 09:18:13 172.16.29.16 BGP(0): no valid path for 10.23.1.0/24
Nov  1 09:18:13 172.16.29.16 BGP(0): 10.12.1.2 rcv UPDATE about 10.24.1.0/24 -- withdrawn
Nov  1 09:18:13 172.16.29.16 BGP(0): no valid path for 10.24.1.0/24
Nov  1 09:18:13 172.16.29.16 BGP: topo global:IPv4 Unicast:base Remove_fwdroute for 10.23.1.0/24
Nov  1 09:18:13 172.16.29.16 BGP: topo global:IPv4 Unicast:base Remove_fwdroute for 10.24.1.0/24
Nov  1 09:19:11 172.16.29.16 BGP(0): 10.12.1.2 rcvd UPDATE w/ attr: nexthop 10.12.1.2, origin i, localpref 100, metric 0
Nov  1 09:19:11 172.16.29.16 BGP(0): 10.12.1.2 rcvd 10.23.1.0/24
Nov  1 09:19:11 172.16.29.16 BGP(0): Revise route installing 1 of 1 routes for 10.23.1.0/24 -> 10.12.1.2(global) to main IP table
Nov  1 09:19:12 172.16.29.16 BGP(0): 10.12.1.2 rcvd UPDATE w/ attr: nexthop 10.12.1.2, origin i, localpref 100, metric 0
Nov  1 09:19:12 172.16.29.16 BGP(0): 10.12.1.2 rcvd 10.24.1.0/24
Nov  1 09:19:12 172.16.29.16 BGP(0): Revise route installing 1 of 1 routes for 10.24.1.0/24 -> 10.12.1.2(global) to main IP table
Nov  1 09:19:22 172.16.29.16 BGP(0): 10.12.1.2 rcvd UPDATE w/ attr: nexthop 10.12.1.2, origin i, localpref 100, metric 0, merged path 65004, AS_PATH 
Nov  1 09:19:22 172.16.29.16 BGP(0): 10.12.1.2 rcvd 10.4.4.4/32
Nov  1 09:19:22 172.16.29.16 BGP(0): Revise route installing 1 of 1 routes for 10.4.4.4/32 -> 10.12.1.2(global) to main IP table
Nov  1 09:19:34 172.16.29.16 BGP(0): 10.12.1.2 rcvd UPDATE w/ attr: nexthop 10.12.1.2, origin i, localpref 100, metric 0, merged path 65003, AS_PATH 
Nov  1 09:19:34 172.16.29.16 BGP(0): 10.12.1.2 rcvd 10.3.3.3/32
Nov  1 09:19:34 172.16.29.16 BGP(0): Revise route installing 1 of 1 routes for 10.3.3.3/32 -> 10.12.1.2(global) to main IP table
Nov  1 09:20:40 172.16.29.16 %GRUB-5-CONFIG_WRITING: GRUB configuration is being updated on disk. Please wait...
Nov  1 09:20:41 172.16.29.16 %GRUB-5-CONFIG_WRITTEN: GRUB configuration was written to disk successfully.
```

- More documentation for syslog (Read the origin-id command)

[DOC-SYSLOG](https://packet-lab.com/main/images/stories/configuringsyslog/configuring%20syslog%20server%20on%20cisco%20routers%20slides.pdf)

## Configuration backup functionality

- To enable automatic backup of the running config to a certain server or on a file on the device itself the archive functionality can be used

- Example configuration:

```
conf t
 archive
  path flash:config.cli
  write-memory
  time-period 1
```

- Path can be a local or a remote device:

```
R1(config-archive)#path ?
  bootflash:  Write archive on bootflash: file system
  flash:      Write archive on flash: file system
  ftp:        Write archive on ftp: file system
  http:       Write archive on http: file system
  https:      Write archive on https: file system
  pram:       Write archive on pram: file system
  rcp:        Write archive on rcp: file system
  scp:        Write archive on scp: file system
  sftp:       Write archive on sftp: file system
  tftp:       Write archive on tftp: file system
```

- Verifying:

```
R1#sh archive 
The maximum archive configurations allowed is 10.
There are currently 3 archive configurations saved.
The next archive file will be named bootflash:config.cli-<timestamp>-3
 Archive #  Name
   1        bootflash:config.cli-Jan--1-12-15-49.924-0 
   2        bootflash:config.cli-Jan--1-12-16-52.585-1 
   3        bootflash:config.cli-Jan--1-12-17-52.684-2 <- Most Recent
   4         
   5         
   6         
   7         
   8         
   9         
   10        
```

- Viewing the files:

```
more flash:config.cli-Jan--1-12-16-52.585-1
```

- Disable archive function:

```
R1(config)#no archive
```

- Applying the archive to the device's running config:

```
R1#copy flash:config.cli-Jan--1-12-16-52.585-1 running-config 
Destination filename [running-config]? 
A system RELOAD is required before templating state change

(...)

reload ! (with config save)
```
