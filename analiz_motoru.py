import numpy as np
from scapy.all import PcapReader
from scipy.fft import fft, fftfreq

def pcap_analiz_et(dosya_yolu):
    zamanlar = []
    with PcapReader(dosya_yolu) as reader:
        for i, paket in enumerate(reader):
            zamanlar.append(float(paket.time))
            if i > 40000: break

    if not zamanlar: return None

    zamanlar = np.array(zamanlar) - zamanlar[0]
    toplam_sure = zamanlar[-1]
    bin_sayisi = 100
    sinyal, _ = np.histogram(zamanlar, bins=bin_sayisi)
    
    N = len(sinyal)
    yf_raw = fft(sinyal)
    xf = fftfreq(N, toplam_sure/bin_sayisi)[:N//2]
    yf = 2.0/N * np.abs(yf_raw[0:N//2])
    
    # Pik ve Ortalama Analizi
    pik_genlik = np.max(yf[1:]) if len(yf) > 1 else 0
    ortalama_sinyal = np.mean(sinyal)
    
    # --- MÜHENDİSLİK METRİKLERİ ---
    anomali_orani = pik_genlik / (ortalama_sinyal + 1e-9)
    tehdit_yuzdesi = min(100, int(anomali_orani * 50))

    rapor = (f"----------------------------------------\n"
             f"TOPLAM PAKET SAYISI  : {len(zamanlar)}\n"
             f"KAYIT SÜRESİ         : {toplam_sure:.2f} saniye\n"
             f"ANOMALİ SKORU        : {anomali_orani:.2f}\n"
             f"TEHDİT SEVİYESİ      : %{tehdit_yuzdesi}\n"
             f"----------------------------------------\n")

    if tehdit_yuzdesi > 65:
        durum = "Saldırı Tespit Edildi"
        rapor += "ANALİZ: Periyodik Flood saldırısı karakteristiği doğrulandı.\n"
        rapor += "EYLEM: IP bloklama ve Rate Limiting önerilir."
    else:
        durum = "Normal Trafik"
        rapor += "ANALİZ: Trafik akışı standart gürültü eşiğinde.\n"
        rapor += "EYLEM: Rutin monitoring devam ediyor."

    return {"zaman_sinyal": sinyal, "xf": xf, "yf": yf, "durum": durum, "bilgi": rapor}