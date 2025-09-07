## Wireless Signals and Modulation

- Understanding Basic Wireless Theory

- Carying Data Over an RF Signal

- Wireless LANs must transmit a signal over radio frequencies to move data from one device to another

- Transmitters and receivers can be fixed in consistent locations, or they can be free to move around

- The basic theory behind wireless signals and the methods used to carry data wirelessly

### Understanding Basic Wireless Theory

- To send data across a wired link, an electrical signal is applied at one end and is carried to the other end

- The wire itself is continuous and conductive, so the signal can propagate rather easily

- A wireless link has no phisical strands of anything to carry the signal along

- How then can an electrical signal be sent across the air, or free space?

- Consider an analogy of people standing far appart, and one person wants to signal something to the other

- They are connected by a long and somewhat loose rope; the rope represents free space

- The sender on one end decides to lift it's end of the rope high and hold it there so that the other end of the rope will also raise and notify the partner

- After all, if the rope were a wire, he knows that he could apply a steady voltage at one end of the wire and it would appear at the other end

- Below is the end result; the rope falls back down after a tiny distance and the receiver never notices a change at all

![failed-attempt](./failed-attempt.png)

- The sender decides to try a different strategy. He cannot push the rope towards the receiver, but when it begins to wave it up and down, in a steady, regular motion, a curious thing happens

- A continuous wave pattern appears along the entire length of the rope

- In fact, the waves (each representing one up and down cycle of the sender's arm), actually travel from the sender to the receiver

![sending-continuous-wave](./sending-a-continuous-wave.png)

- In free space, a similar principle occurs

- The sender (a transmitter) can send an alternating current into a section of wire (an antenna), which sets up the moving electric or magnetic fields that propagate out and away from the wire as traveling waves

- The electric and magnetic fields travel along together and are always at right angles to each other

- The signal must keep changing or alternating, by cycling up and down to keep the electric and magnetic fields cycling and pushing over outward

![electric-magnetic-fields](./electric-and-magnetic-fields.png)

- Electromagnetic waves do not travel strictly in a straight line

- Instead, they travel by expanding in all direction away from the antenna

- To get a visual image, think of dropping a pebble into a pond when the surface is still

- Where it drops in, the pebble sets the water's surface into a cyclic motion

- The waves that result begin small and expand outward, only to be replaced by new waves

- In free space, the electromagnetic waves expand outward in all three dimensions

- Below we can see a simple, idealistic antenna that is a single point, which is connected at the end of the wire

- The waves produced from the tiny point antenna expand outward in a spherical shape

- The waves will eventually reach the receiver, in addition to many other locations in other directions

![wave-propagation](./wave-propagation-idealistic-antenna.png)

- The idealistic antenna does not really exist but serves as a reference point to understand wave propagation

- In the real world, antennas can be made in various shapes and forms that can limit the direction that the waves are sent

- At the receiving end of a wireless link, the process is reversed

- As the electromagnetic waves reach the receiver's antenna, they induce an electrical signal

- If everything works right, the received signal will be a reasonable copy of the original transmitted signal

#### Understanding Frequency

- The waves involved in a wireless link can be measured and described in several ways

- One fundamental property is the *frequency* of the wave, or the number of times the signal makes one complete up and down cycle in one second

- Below we can see how a cycle of a wave can be identified

- A cycle can begin as the signal rises from the center line, falls through the center line and rises again to meet the center line

- A cycle can also ve measured from the center of one peak to the center of the next peak

- No matter where you start measuring a cycle, the signal must make a complete sequence back to it's starting position where it is ready to repeat the same cyclic pattern again

![cycles-in-a-wave](./cycles-in-a-wave.png)

- In the above scheme, during that 1 second the signal progressed through 4 complete cycles

- Therefore, it's frequency is four cycles per second, or four hertz

- A hertz (Hz) is the most commonly used frequency unit and is nothing other than one cycle per second

- Frequency can vary over a very wide range

- As frequency increases by orders of magnitude, the numbers can become quite large

- To keep things simple, the frequency unit name can be modified to denote an increasing number of zeros

```
Unit                    Abbreviation                                    Meaning

Hertz                   Hz                                              Cycles per second

Kilohertz               kHz                                             1000 Hz

Megahertz               MHz                                             1.000.000 Hz

Gigahertz               GHz                                             1.000.000.000 Hz
```

- Below is a simple representation of the continuous frequency spectrum ranging from 0 Hz to 10 ^ 22 (or 1 followed by 22 zeros)

- At the low end of the spectrum are frequencies that are too low to be heard by the human ear, followed by audible sounds

- The highest range of frequencies contains light, follwed by X, gamma and cosmic rays

![frequency-spectrum](./frequency-spectrum.png)

- The frequency range from around 3 kHz to 300 GHz is commonly called radio frequency (RF)

- It includes many different types of radio communication, such as low-frequency radio, AM radio, shortwave radio, television, FM radio, microwave and radar

- The microwave category also contains three main frequency ranges that are used for wireless LAN communication: 2,4, 5 and 6 GHz

- Because a range of frequencies might be used for the same purpose, it is customary to refer to the range as a band of frequencies

- For example, the range from 530 kHz to arround 1710 kHz is used by AM radio stations; therefore, it is commonly called the AM band or the AM broadcast band

- One of the three main frequency ranges used for wireless LAN communication lies between 2.400 and 2.4835 Ghz. This is usually called the 2.4 GHz band, even though it does not encompass the entire range between 2.4 and 2.5 GHz

- It is much more convenient to refer to the band name instead of the specific range of frequencies included

- The 2.4 GHz band is also known as one of the industrial, scientific, and medical (ISM) bands that is available for use without a license

- Another wireless LAN range is usually called the 5GHz band because it lies between 5.150 and 5.825 GHz

- The 5GHz band actually contains the following four separate and district bands, which are also known as Unlicenssed National Information Infrastructure (U-NII)

    - 5150 to 5250 GHz - U-NII-1

    - 5250 to 5350 GHz - U-NII-2A

    - 5470 to 5725 GHz - U-NII-2C

    - 5725 to 5825 GHz - U-NII-3

- From above we can notice that most of the 5 GHz bands are contiguous except for a gap between 5350 and 5470 (also known as U-NII-2B)

- This gap exist and cannot be used for wireless LANs

- However, some government agencies have moved to reclaim the frequencies and repurpose them for wireless LANs

- Efforts are also underway to add 5825 through 5925 GHz (also known as U-NII-4)

- The 6 GHz band lies between 5925 and 7125 GHZ

- It is broken up in four smaller bands, which are also part of the U-NII structure:

    - 5925 to 6425 GHz - U-NII-5

    - 6425 to 6525 GHZ - U-NII-6

    - 6425 to 6825 GHz - U-NII-7

    - 6825 to 7125 GHz - U-NII-8

- It is interesting that the 5 GHz and 6 GHz bands can contain several smaller bands

- The term band is simply a relative term that is used for convenience

- A frequency band contains a continuous range of frequencies

- If two devices require a single frequency for a wireless link between them, which frequency they can use?

- Beyond that, how many unique frequencies can be used within a band?

- To keep everything orderly and compatible, bands are usually divided into a number of distinct channels

- Each channel is known by a channel number and it is assigned to a specific frequency

- As long as the channels are defined by a national or international standards body, they can be used consistently in all locations

- Below is the channel assignment for 2.4 GHz band that is used for wireless LAN communication

- The band contains 14 channels, numbered 1 through 14, each assigned a specific frequency

- First notice how much easier is to refer to channel numbers than the frequencies

- Second, notice that the channels are spaced at regular intervals that are 0.005 GHz (or 5 MHz) apart, except for channel 14

- The channel spacing is known as the channel separation or channel width

![channels-2.4-ghz](./channels-2-4-ghz.png)

- If devices use a specific frequency for a wireless link, why do the channels need to be spaced apart at all?

- The reason lies with the practical limitations of RF signals, the electronics involved in transmitting and receiving the signals, and the overhead needed to add data to the signal efficiently

- In practice, an RF signal is not infinitely narrow, instead it spills above and below a center frequency to some extent, occupying neighboring frequencies too

- It is the center frequency that defines the channel location within the band

- The actual frequency range needed for the transmitted signal is known as the signal bandwidth

- As the name implies, bandwidth refers to the width of frequency space required within the band

- For example, a signal with a 22 MHz bandwidth is bounded at 11 MHz above and below the center frequency

- In wireless LANs, the signal bandwidth is defined as part of a standard

- Even if the signal might extend farther above and below the center frequency than the bandwidth allows, wireless devices will use something called a spectral mask to ignore parts of the signal that fall outside the bandwidth boundaries

![signal-bandwidth](./frequency-bandwidth.png)

- Ideally the signal bandwidth should be less than the channel width so that a different signal could be transmitted on every possible channel with no change that two channels would overlap and interfere with each other

- Below we can see that such a channel spacing, where the signals on adjacent channels do not overlap

- A signal can exist on every possible channel without overlapping with others

![channel-width-non-overlap](./non-overlapping-channel-width.png)

- However you should not assume that the signals centered on the standardized channel assignments will not overlap with each other

- It is entirely possible that the channels in a band are narrower than the signal bandwidth

- Notice how two signals have been centered on two adjacent channel numbers 1 and 2, but they almost entirely overlap each other

- The problem is that the signal bandwidth is slightly wider than four channels

- In this case, signals centered on adjacent channels cannot possibly coexist without overlapping and interfering

- Instead, the channels must be placed on more distant channels to prevent overlapping, thus limiting the number of channels that can be used in the band

- How can channels be numbered such that signals overlap?

- Sometimes the channels in a band are defined and numbered for a specific use

- Later on, another technology might be developed to use the same band and channels, only the newer signals might require more bandwidth than the original channel numbering supported

- Such is the case with 2.4 GHz Wi-Fi band

![overlap-channels](./overlaping-channels.png)

- The 2.4 GHz band is made up of channels that are 5 MHz wide with Wi-Fi signals that have a 22 MHz bandwidth

- Adjacent channel numbers are not spaced far enough apart to be non-overlapping

- However, in the 5GHz and 6GHz bands, channels are non-overlapping because they are spaced every 20 MHz apart to support signals that are just about 20 MHz wide 

- That means every channel can be used without interfering with adjacent channels, maximizing the number of channels that are available for use

#### Understanding Phase

- RF signals are very dependent upon timing because they are always in motion

- By their very nature, the signals are made up by electrical and magnetic forces that vary over time

- The phase of a signal is a measure of shift in time relative to the start of a cycle

- Phase is normally measured in degrees, where 0 degrees is at the start of a cycle, and one complete cycle equals 360 degrees

- A point that is halfway along the cycle is at the 180-degree mark

- Because an oscilating signal si cyclic, you can think of the phase traveling along a cycle again and again

- When two identical signals are produced at exactly the same time, their cycles match up and they are said to be in phase with each other

- If one signal is delayed from the other, the two signals are said to be out of phase

![signals-in-phase-and-out](./in-phase-out-of-phase-signal.png)

- Phase becomes important as RF signals are received

- Signals that are in phase tend to add together, whereas signals that are 180 degrees out of phase, tend to cancel each other

#### Measuring Wavelength