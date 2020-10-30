I will write down some frequently used commands for my personal learning in this markdown.

### Linux system
1. check/ modify udp buffer size:

        sysctl net.core.rmem_max
        sysctl net.core.rmem_default
        sudo sysctl net.core.rmem_max=2621440
        sudo sysctl net.core.rmem_default=2621440

    System default value = 212992. 2621440 is 25 Mb, which is a recommendation.
2. traffic control:
    before adding masks, firstly remove all existing masks

        sudo tc qdisc del root dev eth2

    whatever parameters, use add command first:

        sudo tc qdisc add dev eth2 root netem loss 1%

    eth2 is the NIC
    - **Loss rate**

            sudo tc qdisc change dev eth2 root netem loss 5% 25%

        5% means LR, 25% means the packet loss 25% depends on the previous packet (OPTIONAL). LR cannot be 0, smallest number
        is 0.0000000232%.
    - **Delay**

            sudo tc qdisc add dev eth2 root netem delay 100ms 10ms 25%

        This causes the added delay to be 100ms ± 10ms with the next random element depending 25% on the last one. This isn't true statistical correlation, but an approximation.
    - **Corruption**

            sudo tc qdisc change dev eth2 root netem corrupt 5%

        Random noise can be emulated with the corrupt option. This introduces a single bit error at a random offset in the packet.
    
### FFMPEG

UDP Streaming
- **Receiver**

        ffplay -f h264 "udp://127.0.0.1:10000?fifo_size=1000&overrun_nonfatal=1&buffer_size=1000000"
        
    ? is followed by a few options, which are the fifo size, overrun_nonfatal and **udp buffer size**.
- **Sender**

        ffmpeg -re -i ../video720p.mp4 -vcodec copy -f h264 udp://127.0.0.1:10000

RTP Streaming
- **Receiver**

        ffplay -protocol_whitelist "file,udp,rtp" -i test.sdp 


- **Sender**

Run this first to generate test.sdp

        ffmpeg -re -i ../t1_half.mp4 -vcodec copy -an -f rtp rtp://127.0.0.1:11111>test.sdp

Then,
    
        ffmpeg -re -i ../t1_half.mp4 -vcodec copy -an -f rtp rtp://127.0.0.1:11111

