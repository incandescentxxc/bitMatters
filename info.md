This file serves as my learning journal throughout the FYP

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
### Video related

1. Container
mp4, flv, webm, avi, ts, they are video containers which contain the information of the meta-info of the videos. They normally can accomodate different videos encoded. 

2. Codecs
H.264, H.265, VP9 etc. They are codecs that define the encoding methods of the videos. They include different compression algorithms.

3. Resolution, bitrate, frame rate (fps), GOP（Group of picture）
    - Resolution:
    It refers to the frame size. Higher resolution, higher width and height. Therefore,     resolution raises,  sole frame contains more data in general but subject to the compression as well.
    - Bit rate (BR)
    It is the absolute metric of the file size per second. Higher bit rate -> either higher resolution is used, or less compressed the video is, or the frame rate is higher. They all contribute to finer video quality.
    Therefore, a concrete example is that Youtube's suggested bit rate for videos with different resolutions. As frame rate is normally restricted, say 25. Then if possible, higher bit rate is preferred to decrease the burden of encoder. But it needs to match the uploading speed (network bandwidth).
    - Frame Rate (FPS)
    The number of frame per second. FPS higher, video more smooth. 
    - GOP（Group of picture）
    This is more specific to the encoders. Encoder would normally encode the videos as per frame type. For example, in  H.264, we have I frame, P frame, and B frame. GOP measures the number of frames between two I frames.

### FFMPEG

1. Basic understanding
https://www.ruanyifeng.com/blog/2020/01/ffmpeg.html

        ffmpeg [global para] [input para] [-i input file] [output para] [outputfile]

        $ ffmpeg \
        -y \ # global para
        -c:a libfdk_aac -c:v libx264 \ # input para
        -i input.mp4 \ # input file
        -c:v libvpx-vp9 -c:a libvorbis \ # output para
        output.webm # output file

2. Some basic parameters
        -y overwrite the existing file
        -f force to use format
        -vcodec video codec
        -c:a audio codec
        -c:v video codec
        copy use original codec (No re-encoding/decoding)
        -crf num # compression rate 23 in default
        -g num #gop size setting

3. FFMPEG File redirection
    Use stderr as default output. So redirection need: 2> output.txt

4. Streaming
- UDP Streaming
    - **Receiver**

            ffplay -f h264 "udp://127.0.0.1:10000?fifo_size=1000&overrun_nonfatal=1&buffer_size=1000000"
            
        ? is followed by a few options, which are the fifo size, overrun_nonfatal and **udp buffer size**.

            ffmpeg -y -i "udplite://127.0.0.1:10002?fifo_size=1000&overrun_nonfatal=1&buffer_size=2000000&timeout=5000000" -vcodec copy -f h264 ../videos/test1.mp4

    - **Sender**

            ffmpeg -re -i ../video720p.mp4 -vcodec copy -f h264 "udplite://127.0.0.1:10000?udplite_coverage=20"
    Note:     
    - UDP-lite coverage needs to be given to both recv and send command
    - The acutal implementation shows that send and recv should be cooridinated to the same in order to make udplite work
            ffmpeg -re -i ./videos/test2.mp4 -vcodec libx264 -g 30 -crf 20 -f h264 "udp://127.0.0.1:10000?iber=0&niber=0"
            #another example with more paras



- RTP Streaming
    - **Receiver**

            ffplay -protocol_whitelist "file,udp,rtp" -i test.sdp 

    - **Sender**

        Run this first to generate test.sdp

                ffmpeg -re -i ../t1_half.mp4 -vcodec copy -an -f rtp rtp://127.0.0.1:11111>test.sdp

        Then,
            
                ffmpeg -re -i ../t1_half.mp4 -vcodec copy -an -f rtp rtp://127.0.0.1:11111

5. PSNR/SSIM Calculation
        ffmpeg -i video1.mp4 -i video_origin.mp4 -lavfi  "ssim;[0:v][1:v]psnr" -f null - 2> psnr.log

