from scapy.all import IP, TCP, wrpcap
import random

def pcap_olustur(dosya_adi, paket_sayisi, saldiri_mi=False):
    paketler = []
    su_an = 0
    for i in range(paket_sayisi):
        # Normal trafikte rastgele gecikmeler, saldırıda çok düzenli/hızlı paketler [cite: 6, 7]
        aralik = random.uniform(0.01, 0.1) if not saldiri_mi else 0.005
        su_an += aralik
        p = IP(dst="192.168.1.1")/TCP(sport=1234, dport=80)
        p.time = su_an
        paketler.append(p)
    wrpcap(dosya_adi, paketler)
    print(f"--- {dosya_adi} oluşturuldu! ---")

if __name__ == "__main__":
    pcap_olustur("normal_trafik.pcap", 500, saldiri_mi=False)
    pcap_olustur("saldiri_trafigi.pcap", 2000, saldiri_mi=True)