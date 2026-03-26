import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import os

class SiberFFTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NİHAT FFT - Network Anomaly Detection System v4.0")
        self.root.geometry("1100x950")
        self.root.configure(bg="#050505")

        # --- Akıllı Font Seçimi ---
        mevcut_fontlar = font.families()
        self.siber_font = "Courier" if "Courier" in mevcut_fontlar else "Monospace"
        if "Courier New" in mevcut_fontlar: self.siber_font = "Courier New"
        
        self.font_header = (self.siber_font, 20, "bold")
        self.font_terminal = (self.siber_font, 10)
        self.font_status = (self.siber_font, 12, "bold")
        
        # --- Sol Panel ---
        self.side_panel = tk.Frame(root, bg="#0a0a0a", width=300, bd=1, relief="flat")
        self.side_panel.pack(side="left", fill="y")
        
        # Dekoratif Çizgi
        tk.Frame(self.side_panel, bg="#00ff41", height=2).pack(fill="x", pady=10)
        tk.Label(self.side_panel, text="NİHAT FFT\nENGINE", fg="#00ff41", bg="#0a0a0a", 
                 font=self.font_header, justify="center").pack(pady=20)
        tk.Frame(self.side_panel, bg="#00ff41", height=2).pack(fill="x", pady=10)

        self.btn_select = tk.Button(self.side_panel, text="[ PCAP YUKLE ]", command=self.dosya_sec, 
                                    bg="#111", fg="#00ff41", font=self.font_status, 
                                    relief="flat", width=20, cursor="hand2", activebackground="#00ff41")
        self.btn_select.pack(pady=15)

        self.btn_analyze = tk.Button(self.side_panel, text="[ ANALIZI BASLAT ]", command=self.analiz_thread_baslat, 
                                     bg="#00ff41", fg="black", font=self.font_status, 
                                     relief="flat", width=20, cursor="hand2")
        self.btn_analyze.pack(pady=10)

        # --- YUVARLAK TEKNOLOJİK SPINNER ---
        self.loader_frame = tk.Frame(self.side_panel, bg="#0a0a0a")
        self.loader_frame.pack(pady=60)
        
        # Yuvarlak döner karakterler için büyük etiket
        self.spinner_label = tk.Label(self.loader_frame, text="", fg="#00ff41", bg="#0a0a0a", font=(self.siber_font, 40, "bold"))
        self.spinner_label.pack()
        
        self.loading_text = tk.Label(self.loader_frame, text="SİSTEM BEKLEMEDE", fg="#555", bg="#0a0a0a", font=self.font_terminal)
        self.loading_text.pack(pady=10)

        # --- Sağ Panel ---
        self.main_panel = tk.Frame(root, bg="#050505")
        self.main_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.canvas_frame = tk.Frame(self.main_panel, bg="#0a0a0a", bd=1, relief="solid")
        self.canvas_frame.pack(fill="both", expand=True)

        self.report_frame = tk.LabelFrame(self.main_panel, text=" [ ANALIZ CIKTISI ] ", 
                                          bg="#050505", fg="#00ff41", font=self.font_terminal)
        self.report_frame.pack(fill="x", pady=15)

        self.report_text = tk.Text(self.report_frame, height=10, bg="black", fg="#00ff41", 
                                   font=self.font_terminal, relief="flat", padx=15, pady=15)
        self.report_text.pack(fill="x", padx=10, pady=10)
        self.report_text.config(state="disabled")

    def dosya_sec(self):
        dosya = filedialog.askopenfilename(filetypes=[("Pcap Files", "*.pcap")])
        if dosya:
            self.target_path = dosya
            self.loading_text.config(text=f"DOSYA: {os.path.basename(dosya)}", fg="#00d4ff")

    def analiz_thread_baslat(self):
        if not hasattr(self, 'target_path'): return
        self.btn_analyze.config(state="disabled")
        threading.Thread(target=self.analiz_yap, daemon=True).start()

    def dondur_animasyon(self):
        # Yuvarlak döngü için siber karakterler
        spinner_frames = ['◐', '◓', '◑', '◒'] # Daha yuvarlak ve teknolojik karakterler
        idx = 0
        while self.is_loading:
            self.spinner_label.config(text=spinner_frames[idx])
            idx = (idx + 1) % len(spinner_frames)
            time.sleep(0.15)

    def analiz_yap(self):
        self.is_loading = True
        threading.Thread(target=self.dondur_animasyon, daemon=True).start()
        
        # Adım adım loglama ve yapay gecikme (Sunum için)
        mesajlar = ["VERI PAKETLERI AYRISTIRILIYOR...", "FREKANS SPEKTRUMU HESAPLANIYOR...", "ANOMALI SKORU BELIRLENIYOR..."]
        for m in mesajlar:
            self.loading_text.config(text=m, fg="#ffcc00")
            time.sleep(1.0)

        try:
            from analiz_motoru import pcap_analiz_et
            res = pcap_analiz_et(self.target_path)
            self.root.after(0, self.grafik_guncelle, res)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("HATA", str(e)))
        
        self.is_loading = False
        self.btn_analyze.config(state="normal")
        self.spinner_label.config(text="✔", fg="#00ff41")
        self.loading_text.config(text="ANALIZ TAMAMLANDI", fg="#00ff41")

    def grafik_guncelle(self, res):
        for w in self.canvas_frame.winfo_children(): w.destroy()
        
        # Matplotlib'de font hatasını engellemek için genel monospace kullanalım
        plt.rcParams['font.family'] = 'monospace'
        plt.style.use('dark_background')
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5))
        fig.patch.set_facecolor('#0a0a0a')
        
        ax1.plot(res["zaman_sinyal"], color='#00d4ff', linewidth=1.5)
        ax1.set_title("TRAFIK YOGUNLUK GRAFIGI", color="#00ff41", fontsize=10)
        
        ax2.plot(res["xf"], res["yf"], color='#ff0055', linewidth=1.5)
        ax2.set_title("FFT SPEKTRAL ANALIZ", color="#00ff41", fontsize=10)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.report_text.config(state="normal")
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, res["bilgi"])
        self.report_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = SiberFFTApp(root)
    root.mainloop()