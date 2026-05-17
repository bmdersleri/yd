# down.py

import subprocess
import os
from pathlib import Path

# --- Yapılandırma ---
DOWNLOAD_DIR = Path("downloads/")
TARGET_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def get_metadata(url: str) -> dict | None:
    """yt-dlp kullanarak video metaverisini çeker."""
    print("=============================================================")
    print(f"🔎 Adım 1/2: Metaveri Çekiliyor ({url})...")
    try:
        # yt-dlp komutunu çalıştırarak metaveriyi çekiyoruz.
        command = ["yt-dlp", "--print", "title", "--print", "duration", "--print", "uploader", url]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip().split('\n')

        if len(output) < 3:
            print("❌ Hata: Metaveri çekilemedi. yt-dlp çıktısı eksik.")
            return None
        
        metadata = {
            "title": output[0],
            "duration": output[1],
            "uploader": output[2]
        }
        print("✅ Metaveri Başarıyla Çekildi.")
        return metadata
    except subprocess.CalledProcessError as e:
        print(f"❌ Hata: yt-dlp çalıştırılırken hata oluştu: {e.stderr}")
        return None

def download_video(url: str, metadata: dict) -> bool:
    """aria2c kullanarak videoyu indirir."""
    print("\n=============================================================")
    print(f"⬇️ Adım 2/2: Video İndiriliyor ({url})...")
    
    # İndirme klasörünün var olduğundan emin ol
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    
    # aria2c komutu: -d (download dir), -x 16 (max connections)
    command = ["aria2c", "-d", str(DOWNLOAD_DIR), "-x", "16", url]
    
    try:
        # Komutu çalıştır ve çıktıyı yakala
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ İndirme Başarıyla Tamamlandı. Dosya, '{DOWNLOAD_DIR}' klasöründe.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Hata: aria2c çalıştırılırken hata oluştu: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Hata: İndirme sırasında genel hata oluştu: {e}")
        return False

def main():
    """Ana akış fonksiyonu."""
    print("=============================================================")
    print("         🎬 Video İndirme ve Metaveri Çekme Testi 🎬")
    print("=============================================================")
    
    metadata = get_metadata(TARGET_URL)
    
    if metadata:
        print("\n--- 🌟 Elde Edilen Metaveri (Kullanıcıya Gösterilecek Bilgi) ---")
        print(f"  🎬 Başlık: {metadata['title']}")
        print(f"  ⏱️ Süre: {metadata['duration']}")
        print(f"  👤 Yükleyici: {metadata['uploader']}")
        print("------------------------------------------------------------")
        
        download_video(TARGET_URL, metadata)
    else:
        print("\n🚨 İşlem durduruldu: Metaveri alınamadığı için indirme yapılamadı.")

if __name__ == "__main__":
    main()
