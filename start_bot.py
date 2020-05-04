import subprocess
from time import sleep


filename = 'travian_bot.py'
while True:
    p = subprocess.Popen('python '+filename, shell=True).wait()
    sleep(5)


    if p != 0:
        continue
    else:
        break