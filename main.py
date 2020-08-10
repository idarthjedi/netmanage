from typing import List
from scapy.all import srp
from scapy.layers import l2
from persistence.storage import Storage
from persistence.file import File
import datetime


def scannetwork(ipwithrange: str) -> List:
    # create an ARP packate
    arp = l2.ARP(pdst=ipwithrange)
    # create an Ether broadcast packet
    ether = l2.Ether(dst="ff:ff:ff:ff:ff:ff")
    # stack them
    packet = ether / arp

    # get the results
    result = srp(packet, timeout=3)[0]

    clients = {}

    for sent, received in result:
        # for each response, append ip, mac address and last_seen to clients list
        # clients.append({"mac": received.hwsrc, "ip": received.psrc, "last_seen": datetime.datetime.now().__str__()})
        clients[received.hwsrc] = {"ip": received.psrc, "last_seen": str(datetime.datetime.now())}

    return clients


def main():

    # CIDR is hard-coded for now.
    machines = scannetwork('192.168.1.1/24')

    storageobject = File()
    storageobject.save("network.local.pkl", machines)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
