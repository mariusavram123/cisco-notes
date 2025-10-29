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
