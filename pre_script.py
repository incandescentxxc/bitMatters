# This script serves to run a preliminary test for H.264
# Local machine uses lo
import os
import threading
import sys
import time

class myThread (threading.Thread):
   def __init__(self, cmd):
      threading.Thread.__init__(self)
      self.cmd = cmd
   def run(self):
        os.system(self.cmd)
# def parse_psnr():
#     file = open("psnr.log")
#     length = 0
#     psnr = 0
#     psnr_min = 100
#     psnr_max = 0
#     for line in file.readlines():
#         length += 1
#         line = line.split(" ")
#         val = line[5].split(":")
#         if(float(val[1]) < psnr_min):
#             psnr_min = float(val[1])
#         if(float(val[1]) > psnr_max):
#             psnr_max = float(val[1])
#         psnr += float(val[1])
#     psnr /= length
#     print(psnr)
#     print(psnr_min)
#     print(psnr_max)
#     file.close()
def get_psnr_ssim():
    file = open("psnr.log")
    lines = file.readlines()
    ssim_line, psnr_line = lines[-2].split(" "), lines[-1].split(" ")
    ssim_word, psnr_word = ssim_line[-2].split(":"), psnr_line[7].split(":")
    ssim = float(ssim_word[1])
    psnr = float(psnr_word[1])
    result = []
    result.append(ssim)
    result.append(psnr)
    file.close()
    return result

def main():
    stat_csv = open("stat.csv","w")
    stat_csv.write("bit error,coverage,ssim,psnr\n")
    bit_error = [0, 0.01, 0.1, 1, 5]
    coverage_range = [-2, 0, -1] # -2 means a full coverage
    for br in bit_error:
        print("Current bit error rate: " + str(br))
        if(br != 0):
            cmd_bit_error = "sudo tc qdisc add dev lo root netem corrupt " + str(br) + "%"
            os.system(cmd_bit_error)
        cmd_quality = "ffmpeg -i ../videos/test.mp4 -i ../videos/introBusinessEtEconomySansText_1591434698.mp4 -lavfi  \"ssim;[0:v][1:v]psnr\" -f null - 2> psnr.log"
        for coverage in coverage_range:
            print("Current coverage: " + str(coverage))
            if(coverage == -2): # udp
                cmd_recv = "ffmpeg -y -i \"udp://127.0.0.1:10002?fifo_size=1000&overrun_nonfatal=1&buffer_size=2000000&timeout=4000000\" -vcodec copy -f h264 ../videos/test.mp4 2> recv.log"
                cmd_send = "ffmpeg -re -i ../videos/introBusinessEtEconomySansText_1591434698.mp4 -vcodec libx264 -f h264 udp://127.0.0.1:10002 2> send.log"
            elif(coverage == 0): # default udplite 8 bytes header coverage
                cmd_recv = "ffmpeg -y -i \"udplite://127.0.0.1:10002?fifo_size=1000&overrun_nonfatal=1&buffer_size=2000000&timeout=4000000\" -vcodec copy -f h264 ../videos/test.mp4 2> recv.log"
                cmd_send = "ffmpeg -re -i ../videos/introBusinessEtEconomySansText_1591434698.mp4 -vcodec libx264 -f h264 \"udplite://127.0.0.1:10002?udplite_coverage=" + str(coverage) + "\" 2> send.log"
            else: # udplite with variations
                cmd_recv = "ffmpeg -y -i \"udplite://127.0.0.1:10002?fifo_size=1000&overrun_nonfatal=1&buffer_size=2000000&timeout=4000000&udplite_coverage=" + str(coverage) + "\" -vcodec copy -f h264 ../videos/test.mp4 2> recv.log"
                cmd_send = "ffmpeg -re -i ../videos/introBusinessEtEconomySansText_1591434698.mp4 -vcodec libx264 -f h264 \"udplite://127.0.0.1:10002?udplite_coverage=" + str(coverage) + "\" 2> send.log"
            thread1 = myThread(cmd_recv)
            time.sleep(2)
            thread2 = myThread(cmd_send)
            # Start new Threads
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
            os.system(cmd_quality)
            stat = get_psnr_ssim()
            ssim, psnr = stat[0], stat[1]
            stat_csv.write(str(br) + "," + str(coverage) + "," + str(ssim) + "," + str(psnr) + "\n")
        if(br != 0):
            cmd_unmask = "sudo tc qdisc del dev lo root netem"
            os.system(cmd_unmask)
    stat_csv.close()
        

main()