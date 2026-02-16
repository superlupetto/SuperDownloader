import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil

# --- CONFIGURAZIONE ---
BASE_DIR = r"C:\Super Downloader"
CONFIG_FILE = os.path.join(BASE_DIR, "config.txt")
MUSIC_DIR = os.path.join(BASE_DIR, "Musica")
VIDEO_DIR = os.path.join(BASE_DIR, "Video")
FFMPEG_ROOT = r"C:\FFmpeg"
FFMPEG_EXE = os.path.join(FFMPEG_ROOT, "bin", "ffmpeg.exe")
# Inserisci i tuoi URL reali qui sotto
UPDATE_URL = "https://raw.githubusercontent.com"
FF_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip"
SCRIPT_PATH = os.path.abspath(__file__)

LANGS = {
    'it': {
        'menu_title': "      SUPER DOWNLOADER PRO V1.9.1",
        'opt1': " [1] -> Scarica MP3 (YouTube)",
        'opt2': " [2] -> Scarica MP4 (YouTube)",
        'opt3': " [3] -> Converti Video Locali in MP3",
        'opt4': " [4] -> AGGIORNA SCRIPT (Server)",
        'opt5': " [5] -> Aggiorna yt-dlp (Libreria)",
        'opt6': " [6] -> LINGUA (Cambia Lingua)",
        'opt7': " [7] -> Esci",
        'ask': "Scegli: ",
        'link': "Incolla Link (o 'x' per tornare): ",
        'done': "✅ Operazione completata!",
        'error': "❌ Errore: ",
        'ffmpeg_msg': "FFMPEG MANCANTE - INSTALLAZIONE AUTOMATICA",
        'upd_check': "Controllo aggiornamenti...",
        'conv_start': "Conversione: ",
        'wait': "Premi Invio per continuare..."
    },
    'en': {
        'menu_title': "      SUPER DOWNLOADER PRO V1.9.1",
        'opt1': " [1] -> Download MP3 (YouTube)",
        'opt2': " [2] -> Download MP4 (YouTube)",
        'opt3': " [3] -> Convert Local Videos to MP3",
        'opt4': " [4] -> UPDATE SCRIPT (Server)",
        'opt5': " [5] -> Update yt-dlp (Library)",
        'opt6': " [6] -> LANGUAGE (Change Language)",
        'opt7': " [7] -> Exit",
        'ask': "Choose: ",
        'link': "Paste Link (or 'x' to go back): ",
        'done': "✅ Operation completed!",
        'error': "❌ Error: ",
        'ffmpeg_msg': "FFMPEG MISSING - AUTOMATIC INSTALLATION",
        'upd_check': "Checking for updates...",
        'conv_start': "Converting: ",
        'wait': "Press Enter to continue..."
    }
}

CURRENT_LANG = 'it'

def carica_lingua():
    global CURRENT_LANG
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            saved = f.read().strip()
            if saved in LANGS:
                CURRENT_LANG = saved
                return True
    return False

def salva_lingua(scelta):
    global CURRENT_LANG
    CURRENT_LANG = 'en' if scelta == '1' else 'it'
    if not os.path.exists(BASE_DIR): os.makedirs(BASE_DIR)
    with open(CONFIG_FILE, 'w') as f:
        f.write(CURRENT_LANG)

# --- AUTO-INSTALLAZIONE LIBRERIE ---
try:
    import yt_dlp
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

def installa_ffmpeg_auto():
    if os.path.exists(FFMPEG_EXE): return
    L = LANGS[CURRENT_LANG]
    print(f"\n{'='*43}\n   {L['ffmpeg_msg']}\n{'='*43}")
    zip_tmp = os.path.join(os.environ.get('TEMP', 'C:\\'), "ffmpeg_btbn.zip")
    try:
        req = urllib.request.Request(FF_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(zip_tmp, 'wb') as out:
            shutil.copyfileobj(response, out)
        temp_ex = r"C:\FFmpeg_Temp"
        with zipfile.ZipFile(zip_tmp, 'r') as zip_ref: zip_ref.extractall(temp_ex)
        folder = [d for d in os.listdir(temp_ex) if os.path.isdir(os.path.join(temp_ex, d))][0]
        if os.path.exists(FFMPEG_ROOT): shutil.rmtree(FFMPEG_ROOT)
        shutil.move(os.path.join(temp_ex, folder), FFMPEG_ROOT)
        shutil.rmtree(temp_ex); os.remove(zip_tmp)
    except Exception as e: print(f"{L['error']}{e}"); input(); sys.exit()

def download(url, mode):
    L = LANGS[CURRENT_LANG]
    opts = {
        'ffmpeg_location': os.path.join(FFMPEG_ROOT, "bin"),
        'outtmpl': os.path.join(MUSIC_DIR if mode=='audio' else VIDEO_DIR, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best' if mode=='audio' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'noplaylist': True,
    }
    if mode == 'audio':
        opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]
    try:
        with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([url])
        print(f"\n{L['done']}")
    except Exception as e: print(f"{L['error']}{e}")

def main():
    if not carica_lingua():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("===========================================")
        print("  SELECT LANGUAGE / SCEGLI LINGUA")
        print("===========================================")
        print(" [1] English")
        print(" [2] Italiano")
        salva_lingua(input("\nChoose/Scegli: ").strip())

    L = LANGS[CURRENT_LANG]
    for d in [BASE_DIR, MUSIC_DIR, VIDEO_DIR]: 
        if not os.path.exists(d): os.makedirs(d)
    installa_ffmpeg_auto()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("===========================================")
        print(L['menu_title'])
        print("===========================================")
        print(f" 📂 Path: {BASE_DIR} | 🌐 Lang: {CURRENT_LANG.upper()}")
        print("-------------------------------------------")
        print(f"{L['opt1']}\n{L['opt2']}\n{L['opt3']}\n{L['opt4']}\n{L['opt5']}\n{L['opt6']}\n{L['opt7']}")
        print("===========================================")
        
        scelta = input(L['ask']).strip()
        if scelta == '7': break
        elif scelta == '6': # Cambia Lingua
            if os.path.exists(CONFIG_FILE): os.remove(CONFIG_FILE)
            main()
            break
        elif scelta in ['1', '2']:
            u = input(L['link']).strip()
            if u.lower() != 'x' and u: 
                download(u, 'audio' if scelta == '1' else 'video')
                input(f"\n{L['wait']}")
        elif scelta == '3':
            files = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith(('.mp4', '.mkv', '.webm'))]
            for f in files:
                print(f"{L['conv_start']}{f}...")
                subprocess.run([FFMPEG_EXE, "-i", os.path.join(VIDEO_DIR, f), "-vn", "-b:a", "192k", os.path.join(MUSIC_DIR, os.path.splitext(f)[0] + ".mp3"), "-y"], capture_output=True)
            print(L['done'])
            input(f"\n{L['wait']}")
        elif scelta == '4':
            print(L['upd_check'])
            try:
                urllib.request.urlretrieve(UPDATE_URL, SCRIPT_PATH + ".new")
                with open("update.bat", "w") as f:
                    f.write(f'@echo off\ntimeout /t 1 >nul\nmove /y "{SCRIPT_PATH}.new" "{SCRIPT_PATH}"\nstart python "{SCRIPT_PATH}"\ndel "%~f0"')
                subprocess.Popen("update.bat", shell=True); sys.exit()
            except: print("Server offline o URL non valido."); input()
        elif scelta == '5':
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
            input(f"\n{L['wait']}")

if __name__ == "__main__":
    main()

