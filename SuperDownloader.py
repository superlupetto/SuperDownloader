import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil

# --- CONFIGURAZIONE ---
BASE_DIR = r"C:\Super Downloader"
MUSIC_DIR = os.path.join(BASE_DIR, "Musica")
VIDEO_DIR = os.path.join(BASE_DIR, "Video")
FFMPEG_ROOT = r"C:\FFmpeg"
FFMPEG_EXE = os.path.join(FFMPEG_ROOT, "bin", "ffmpeg.exe")
UPDATE_URL = "http://lunaremagicafata.duckdns.org/SuperDownloader.py"
# Link GitHub BtbN Shared richiesto
FF_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip"
SCRIPT_PATH = os.path.abspath(__file__)

# --- AUTO-INSTALLAZIONE LIBRERIE ---
try:
    import yt_dlp
except ImportError:
    print("Installazione yt-dlp...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

def installa_ffmpeg_auto():
    """Scarica ed estrae FFmpeg BtbN in C:\\FFmpeg se manca"""
    if os.path.exists(FFMPEG_EXE):
        return

    print("\n" + "="*43)
    print("   FFMPEG MANCANTE - INSTALLAZIONE AUTOMATICA")
    print("="*43)
    
    zip_tmp = os.path.join(os.environ['TEMP'], "ffmpeg_btbn.zip")
    temp_extract = r"C:\FFmpeg_Temp_Zip"
    
    try:
        print(f">>> Download da GitHub (BtbN Shared)...")
        # Header necessario per evitare blocchi da GitHub
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(FF_URL, zip_tmp)

        print(">>> Estrazione in corso in C:\\FFmpeg...")
        if os.path.exists(FFMPEG_ROOT): shutil.rmtree(FFMPEG_ROOT)
        if os.path.exists(temp_extract): shutil.rmtree(temp_extract)

        with zipfile.ZipFile(zip_tmp, 'r') as zip_ref:
            zip_ref.extractall(temp_extract)
        
        # Gestione sottocartella specifica di BtbN
        sub = [d for d in os.listdir(temp_extract) if os.path.isdir(os.path.join(temp_extract, d))][0]
        shutil.move(os.path.join(temp_extract, sub), FFMPEG_ROOT)
        
        shutil.rmtree(temp_extract)
        os.remove(zip_tmp)
        print("✅ FFmpeg BtbN installato con successo!")
        print("="*43 + "\n")
    except Exception as e:
        print(f"❌ ERRORE: {e}\nEsegui come AMMINISTRATORE!")
        input("Premi Invio per uscire..."); sys.exit()

def inizializza():
    for d in [BASE_DIR, MUSIC_DIR, VIDEO_DIR]:
        if not os.path.exists(d): os.makedirs(d)
    installa_ffmpeg_auto()

def download(url, mode='video'):
    folder = MUSIC_DIR if mode == 'audio' else VIDEO_DIR
    opts = {
        'ffmpeg_location': os.path.join(FFMPEG_ROOT, "bin"),
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best' if mode == 'audio' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}] if mode == 'audio' else []
    }
    with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([url])

def update_script():
    print(f"\nControllo aggiornamenti su: {UPDATE_URL}")
    try:
        temp_file = SCRIPT_PATH + ".new"
        urllib.request.urlretrieve(UPDATE_URL, temp_file)
        if os.path.exists(temp_file):
            with open("update.bat", "w") as f:
                f.write(f'@echo off\ntimeout /t 1 >nul\nmove /y "{temp_file}" "{SCRIPT_PATH}"\nstart python "{SCRIPT_PATH}"\ndel "%~f0"')
            subprocess.Popen("update.bat", shell=True)
            sys.exit()
    except Exception as e:
        print(f"❌ Errore aggiornamento: {e}")

def main():
    inizializza()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("===========================================")
        print("      SUPER DOWNLOADER PRO V1.7")
        print("===========================================")
        print(f" Cartelle: C:\\Super Downloader\\")
        print("-------------------------------------------")
        print(" [1] ->Scarica MP3")
        print(" [2] ->Scarica MP4")
        print(" [3] ->Converti Video Locali in MP3")
        print(" [4] ->AGGIORNA SCRIPT (dal Server)")
        print(" [5] ->Aggiorna yt-dlp (Libreria)")
        print(" [6] ->Esci")
        print("===========================================")
        
        scelta = input("Scegli: ").strip()
        if scelta == '6': break
        elif scelta in ['1', '2']:
            u = input("Incolla Link: ").strip()
            if u: download(u, 'audio' if scelta == '1' else 'video')
        elif scelta == '3':
            files = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith(('.mp4', '.mkv'))]
            for f in files:
                subprocess.run([FFMPEG_EXE, "-i", os.path.join(VIDEO_DIR, f), "-vn", "-b:a", "192k", os.path.join(MUSIC_DIR, os.path.splitext(f)[0]+".mp3"), "-y"], capture_output=True)
                print(f"✅ Convertito: {f}")
        elif scelta == '4': update_script()
        elif scelta == '5': subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
        
        input("\nPremi Invio...")

if __name__ == "__main__":
    main()
