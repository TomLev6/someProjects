from scapy.layers.inet import IP, TCP
from scapy.all import *
from scapy.packet import Packet
from datetime import datetime
from sql_db import Odbc

# packet_count = 0
# max_packets = 128  # (200)
# start_time = time.time()
# users_list = Clients()
# black_list = Black_client()
db = Odbc()


def handle_packets(packet: Packet):
    # global packet_count, start_time
    if "IP" in str(packet.layers()):
        ip = packet[IP].src
        if not db.find_in_users(ip):
            db.insert_new_user(ip, 1, str(datetime.now()))

        msg_pack = IP(dst=packet[IP].src) / Raw(load="You are not an attacker!, phew..")
        send(msg_pack, inter=.001)
        # db.update_user_data(ip, db.get_user_packets(ip) + 1)
        #     if db.get_user_packets(ip) > 128:
        #         elapsed_time = float(time.time()) - float(db.get_user_time(ip))
        #         # print(f"if {users_list.get_packets_count(ip)} > {max_packets} and {elapsed_time} < 2")
        #         if db.get_user_packets(ip) > max_packets and elapsed_time < 3:  # 1
        #             print("******************************  Attack detected!  ******************************")
        #             now = datetime.now()
        #             db.insert_to_blacklist(ip, "attacker", now)
        print("routing the request to the site...")

    else:
        print("Error!")
        pass


def custom_three_way_handshake(packt: Packet):
    global db
    if IP and TCP in packt.layers():
        if str(packt[TCP].flags) == "A":
            print("compares:", int(packt[TCP].sport) * int(packt[IP].src.split(".")[-1]) + 1, "to", int(packt[TCP].ack))
            if int(packt[TCP].seq) == 0 or \
                    int(packt[TCP].sport) * int(packt[IP].src.split(".")[-1]) + 1 != int(packt[TCP].ack):  # seq != y+1
                now = datetime.now()
                db.insert_to_blacklist(packt[IP].src, "attacker", now)
            else:
                return True

        elif str(packt[TCP].flags) == "S":
            print("[S]:")
            print("sport:", int(packt[TCP].sport), "ip:", int(packt[IP].src.split(".")[-1]))
            new_seq = (int(packt[TCP].sport) * int(packt[IP].src.split(".")[-1]))  # y
            ip = IP(src=packt[IP].dst, dst=packt[IP].src)
            # Store the new_seq value in a variable and use it when constructing the SYN-ACK packet
            new_seq_ack = new_seq + 1
            tcp = TCP(dport=packt[TCP].sport, sport=packt[TCP].dport, flags='SA', seq=new_seq, ack= new_seq_ack)
            p = ip / tcp
            p.show()
            send(p, inter=.0001, verbose=0)

    return False


def filters(pkt: Packet):
    global db
    if IP in pkt.layers():
        if str(pkt[IP].src) == "192.168.1.32" and str(pkt[IP].dst) == "192.168.1.5":
            # if db.find_in_blacklist(pkt[IP].src):
            #     print(f"access denied!, blocked user({pkt[IP].src})!") ###########
            #     return False
            # else:
            return custom_three_way_handshake(pkt)


def main():
    db.connect()
    while True:
        sniff(prn=handle_packets, lfilter=filters)
    # db.close_connection()


if __name__ == '__main__':
    main()
