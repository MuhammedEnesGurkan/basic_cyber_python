from scapy.all import *

def discover_mac():
    eth = Ether()
    arp = ARP()

    eth.dst="ff:ff:ff:ff:ff:ff"

    arp.pdst = "10.42.80.1/24"

    bcpckt = eth/arp

    bcpckt.show()

    ans, unans = srp(bcpckt,timeout=5)

    # ans.summary()
    # print("#"*30)
    # unans.summary()

    for snd,rcv in ans:
        # print(rcv.show())
        print(rcv.pdst + "->" + rcv.hwdst)


discover_mac()
