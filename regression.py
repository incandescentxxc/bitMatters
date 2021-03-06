# This script sets up the experiment for getting data between
# PSNR, SSIM and the BER of I, NonI slices.
import os
import threading
import sys
import time


class myThread(threading.Thread):
   def __init__(self, cmd):
      threading.Thread.__init__(self)
      self.cmd = cmd

   def run(self):
        os.system(self.cmd)


def get_psnr_ssim():
    file = open("psnr.log")
    lines = file.readlines()
    if(lines[-1] != "Conversion failed!"):
        ssim_line, psnr_line = lines[-2].split(" "), lines[-1].split(" ")
        ssim_word, psnr_word = ssim_line[-2].split(":"), psnr_line[7].split(":")
        ssim = float(ssim_word[1])
        psnr = float(psnr_word[1])
        result = []
        result.append(ssim)
        result.append(psnr)
        file.close()
        return result
    file.close()
    return [-1,-1]


def run_test(istart, istep, iend, nstart, nstep, nend):

    iber = istart
    niber = nstart

    cmd_quality = "ffmpeg -i ../videos/test2.mp4 -i ../videos/test_recv.mp4 -lavfi  \"ssim;[0:v][1:v]psnr\" -f null - 2> psnr.log"
    cmd_recv = "ffmpeg -y -i \"udp://127.0.0.1:10000?fifo_size=8000&overrun_nonfatal=1&buffer_size=2000000&timeout=4000000\" -vcodec copy -f h264 ../videos/test_recv.mp4 2> recv.log"
    while(iber <= iend): #1%
        while(niber <= nend):
            print("iber is " + str(iber*100) + "%" + " and niber is " + str(niber*100) + "%")
            # need to configure the noniber in sender side # gop 30
            cmd_send = "ffmpeg -re -i ../videos/test2.mp4 -vcodec libx264 -g 3 -f h264 \"udp://127.0.0.1:10000?iber=" + str(iber) + "&noniber=" + str(niber) + "\" 2> send.log"
            thread1 = myThread(cmd_recv)
            time.sleep(0.5)
            thread2 = myThread(cmd_send)
            # Start new Threads
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
            os.system(cmd_quality)
            stat = get_psnr_ssim()
            ssim, psnr = stat[0], stat[1]
            file=open("ff_records.txt", "a")
            file.write("PSNR: " + str(psnr) + "\n")
            file.write("SSIM: " + str(ssim))
            file.write("\n------------------------\n")
            file.close()
            # print(ssim, psnr)
            niber = niber + nstep
        niber = nstart
        iber = iber + istep
        print(time.asctime())


def main():
    print(time.asctime())
    run_test(0.015, 0.001, 0.03, 0.001, 0.002, 0.03) # 40*40 = 1600
    
    print("Finished!")
    print(time.asctime())

    

main()
