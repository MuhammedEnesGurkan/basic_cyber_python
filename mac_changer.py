import random
import re
import subprocess
#basic macchanger for linux systems based on debian
maclist = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]

newmac = ""
for i in range(0,12):
    newmac += random.choice(maclist)
print(newmac)

ifconfig_res = subprocess.check_output("ifconfig eth0",shell=True).decode()
print(ifconfig_res)

oldmac = re.search("ether (.+)",ifconfig_res).group()

print(oldmac.split()[1])

subprocess.check_output("ifconfig eth0 down",shell=True)
subprocess.check_output("sudo ifconfig eth0 hw ether "+newmac,shell=True)
subprocess.check_output("ifconfig eth0 up",shell=True)

ifconfig_res2 = subprocess.check_output("ifconfig eth0",shell=True).decode()
print(ifconfig_res2)

