This file will take the notes of my progess on what I did for the FYP everyday.
- Oct.29
    - Read about FFMPEG docs, commands, and operations.
    - Find commands about H.264 for sending and receiving udp/udplite streams
- Oct.30
    - Finish the script of prelimniary test
    - Consult with supervisor 
    - Write some docs
...
- Nov.20
    - Add new functions in FFMPEG: give different coverage when transmitting I frames and non-Iframe
    - Identified the NaLu type for every packet
    - UDP-lite coverage needs to be given to both recv and send command
    - The acutal implementation shows that send and recv should be cooridinated to the same in order to make udplite work
- Nov.21
    - Sender bit error generator finished
    - Sender bit error rate breakdown for I/non-I frames finished
...
-Dec. 4
    - experiment on bit error rate for I/non-I frames universially finished
    - regression analysis finished
