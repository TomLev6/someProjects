import threading
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
    print(threading.active_count())
    if custom_three_way_handshake(packet):
        ip = packet[IP].src
        if not db.find_in_users(ip):
            db.insert_new_user(ip, 1, str(datetime.now()))

        msg_pack = IP(dst=packet[IP].src) / TCP(dport=packet[TCP].sport, sport=packet[TCP].dport) / Raw(
            load="You are not an attacker!, phew..")
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


def sr1_ignore_rst(p: Packet, inter=.0001, verbose=False) -> Union[Packet, None]:
    answer = sr1(p, inter=inter, verbose=verbose)  # probably return RST + ACK from the operating system
    print("[SA]")
    answer2 = sniff(count=1, lfilter=filters, timeout=5) # lambda x, port=p[TCP].dport: filters2(x, port)
    if answer is not None and TCP in answer.layers() and answer[TCP].flags == "A":
        answer.show()
        if int(answer[TCP].seq) == 0 or \
                int(answer[TCP].sport) * int(answer[IP].src.split(".")[-1]) + 1 != int(answer[TCP].ack):
            now = datetime.now()
            db.insert_to_blacklist(answer[IP].src, "attacker", now)
        else:
            return answer
    elif answer2 and answer is not None and TCP in answer.layers() and answer[TCP].flags in ["RA", "R"]:
        answer2 = answer2[0]
        answer2[0].show()
        if answer2 is not None and TCP in answer2.layers() and answer2[TCP].flags == "A":
            if int(answer2[TCP].seq) == 0 or \
                    int(answer2[TCP].sport) * int(answer2[IP].src.split(".")[-1]) + 1 != int(answer2[TCP].ack):
                now = datetime.now()
                db.insert_to_blacklist(answer2[IP].src, "attacker", now)
            else:
                return answer2
    return None


def custom_three_way_handshake(packt: Packet):
    global db
    if str(packt[TCP].flags) == "S":
        print("[S]")
        new_seq = (int(packt[TCP].sport) * int(packt[IP].src.split(".")[-1]))  # y
        ip = IP(src=packt[IP].dst, dst=packt[IP].src)
        tcp = TCP(dport=packt[TCP].sport, sport=packt[TCP].dport, flags='SA', seq=new_seq, ack=packt[TCP].seq + 1)
        p_sa = ip / tcp
        p_ack = sr1_ignore_rst(p_sa)
        if p_ack is not None:
            print("[A]")
            p_ack.show()
            return True
        else:
            print("None")
    return False


def filters(pkt: Packet):
    global db
    if IP in pkt.layers() and TCP in pkt.layers():
        if str(pkt[IP].src) == "192.168.1.32" and str(pkt[IP].dst) == "192.168.1.13" and str(pkt[TCP].dport) == "8000":
        #     if TCP in pkt.layers():
        #         if pkt[TCP].flags not in ["RA", "R"]:
            # if db.find_in_blacklist(pkt[IP].src):
            #     print(f"access denied!, blocked user({pkt[IP].src})!") ###########
            #     return False
            # else:
            return True
            # return custom_three_way_handshake(pkt)
    return False


def thread_handle_packet(pkt: Packet):
    thread = threading.Thread(target=handle_packets, args=(pkt,))
    thread.start()


def sniffs():
    sniff(prn=lambda p: queue.put(p), lfilter=filters)


def main():
    db.connect()
    # sniffs()
    thread = threading.Thread(target=sniffs)
    thread.start()
        # sniff(prn=handle_packets, lfilter=filters)
    # db.close_connection()


if __name__ == '__main__':
    main()
