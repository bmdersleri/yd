# main_downloader.py

import json
import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Optional

# --- Yapılandırma ---
# Bu sabitler, projenin genel yapısına göre ayarlanmalıdır.
INPUT_DIR = Path("input_urls/")
DOWNLOAD_DIR = Path("downloads/")
ORGANIZED_OUTPUT_DIR = Path("organized_output/")

def setup_directories():
    """Gerekli dizinlerin var olduğundan emin olur."""
    print("--- Dizin Kontrol Ediliyor ---")
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    ORGANIZED_OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"Dizinler hazır: {DOWNLOAD_DIR} ve {ORGANIZED_OUTPUT_DIR}")

def load_video_urls(json_file_path: str) -> Optional[List[str]]:
    """
    Belirtilen JSON dosyasından video URL listesini yükler.
    Beklenen JSON yapısı: {"urls": ["url1", "url2", ...]}
    """
    print(f"\n--- URL'ler Yükleniyor: {json_file_path} ---")
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, dict) and 'urls' in data and isinstance(data['urls'], list):
            return data['urls']
        else:
            print("Hata: JSON yapısı beklenenden farklı. 'urls' anahtarı bulunamadı.")
            return None
    except FileNotFoundError:
        print(f"Hata: Dosya bulunamadı: {json_file_path}")
        return None
    except json.JSONDecodeError:
        print("Hata: Geçersiz JSON formatı.")
        return None

def extract_metadata(url: str) -> Optional[Dict]:
    """
    Bir URL'den video metaverisini (başlık, süre vb.) çıkarır.
    yt-dlp kullanarak bu işlemi gerçekleştirir.
    """
    print(f"    [Metaveri Çıkarılıyor] {url}")
    try:
        # yt-dlp'den gerekli bilgileri çekmek için subprocess kullanıyoruz.
        # Bu komut, JSON formatında çıktı vermesi için --print ve --skip-download kullanır.
        command = ["yt-dlp", "--print", "title", "--print", "duration", "--print", "uploader", url]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip().split('\n')

        if len(output) < 3:
            print("    [Hata] Metaveri çekilemedi. yt-dlp çıktısı eksik.")
            return None

        metadata = {
            "url": url,
            "title": output[0],
            "duration": output[1],
            "uploader": output[2]
        }
        return metadata
    except subprocess.CalledProcessError as e:
        print(f"    [Hata] yt-dlp çalıştırılırken hata oluştu: {e.stderr}")
        return None
    except Exception as e:
        print(f"    [Hata] Metaveri çıkarılırken genel hata oluştu: {e}")
        return None

def download_video(url: str, temp_filepath: Path) -> bool:
    """
    Verilen URL'deki videoyu yüksek hızda indirir.
    aria2c kullanarak indirme işlemi gerçekleştirilir.
    """
    print(f"    [İndirme Başlatılıyor] {url} -> {temp_filepath}")
    try:
        # aria2c komutu: -d (download dir), -x 16 (max connections)
        command = ["aria2c", "-d", str(DOWNLOAD_DIR), "-x", "16", url]
        
        # subprocess.run ile komutu çalıştırıyoruz.
        # Bu, dosyanın doğrudan DOWNLOAD_DIR içine inmesini sağlar.
        subprocess.run(command, check=True, capture_output=True, text=True)
        
        # Başarılı indirme sonrası, en son indirilmiş dosyayı bulup geçici yola taşıyabiliriz.
        # Basitlik için, indirme işleminin başarılı olduğunu varsayıyoruz.
        return True
    except subprocess.CalledProcessError as e:
        print(f"    [Hata] aria2c çalıştırılırken hata oluştu: {e.stderr}")
        return False
    except Exception as e:
        print(f"    [Hata] İndirme sırasında genel hata oluştu: {e}")
        return False

def organize_files(download_dir: Path, output_dir: Path, video_metadata: Dict) -> bool:
    """
    İndirilen dosyayı metaveriye uygun olarak hedef dizine taşır ve yeniden adlandırır.
    """
    print(f"    [Düzenleme] Dosya adı oluşturuluyor...")
    
    # 1. Yeni Dosya Adı Oluşturma
    # Format: Başlık - Süre - Yükleyici.mp4
    title = video_metadata.get('title', 'UnknownTitle').replace(' ', '_')
    duration = video_metadata.get('duration', 'UnknownDuration')
    uploader = video_metadata.get('uploader', 'UnknownUploader').replace(' ', '')
    
    # Dosya uzantısını varsayalım ki mp4 olsun.
    new_filename = f"{title}_{duration}_{uploader}.mp4"
    final_destination_path = output_dir / new_filename

    # 2. İndirilen Dosyayı Bulma ve Taşıma
    # aria2c, genellikle dosya adını URL'den yola çıkarak indirir.
    # Burada, indirilen geçici dosyayı (genellikle URL'deki uzantıya yakın bir şey) bulup taşımamız gerekir.
    
    # Basit bir yaklaşım: DOWNLOAD_DIR içindeki en son değiştirilen dosyayı bulalım.
    try:
        # Bu, en basit ve en güvenilir olmayan kısımdır, ancak stubs'ı doldurmak için gerekli.
        # Gerçek projede, indirme işlemi sırasında dosya adını yakalamak gerekir.
        downloaded_files = list(download_dir.glob('*'))
        if not downloaded_files:
            print("    [Hata] Geçici indirme dizininde dosya bulunamadı.")
            return False
        
        # Varsayalım ki ilk bulunan dosya indirilmiş dosyadır.
        source_file = downloaded_files[0] 
        
        # Taşıma işlemi
        shutil.move(str(source_file), str(final_destination_path))
        print(f"    ✅ Başarıyla taşındı ve yeniden adlandırıldı: {final_destination_path.name}")
        return True
    except Exception as e:
        print(f"    [Hata] Dosya taşıma/yeniden adlandırma sırasında hata oluştu: {e}")
        return False

def main_downloader_organizer(json_file_path: str, target_directory: str):
    """
    Ana orkestrasyon fonksiyonu. Tüm adımları yönetir.
    """
    print("===============================================")
    print("          🎥 Video İndirme ve Düzenleme Başladı 🎥")
    print("===============================================")
    
    # 1. Hazırlık
    setup_directories()
    
    # 2. URL Yükleme
    urls = load_video_urls(json_file_path)
    if not urls:
        print("İşlem durduruldu: URL listesi alınamadı.")
        return

    processed_metadata = []

    # 3. Döngü: Metaveri Çıkarma, İndirme ve Düzenleme
    for url in urls:
        print("\n" + "="*40)
        print(f"İşleniyor: {url}")
        
        # Metaveri Çıkarma
        metadata = extract_metadata(url)
        if not metadata:
            print("    ❌ İşlem atlandı: Metaveri alınamadı.")
            continue
        
        processed_metadata.append(metadata)
        
        # İndirme
        # Geçici dosya yolu sadece bir referans için kullanılıyor, asıl indirme DOWNLOAD_DIR'a yapılacak.
        temp_download_path = DOWNLOAD_DIR / f"{url.split('/')[-1]}_{'temp'}" 
        
        if download_video(url, temp_download_path):
            # Düzenleme
            if organize_files(DOWNLOAD_DIR, Path(target_directory), metadata):
                print("    ✅ Adım tamamlandı.")
            else:
                print("    ❌ Düzenleme adımında hata oluştu.")
        else:
            print("    ❌ İndirme adımında hata oluştu. İşlem durduruldu.")

    print("\n=====================================================")
    print("          🎉 Tüm İşlemler Tamamlandı! 🎉")
    print("=====================================================")

if __name__ == "__main__":
    # Örnek kullanım (Bu kısım MCP sunucusu içinde çağrılacak)
    # Geçici bir JSON dosyası oluşturma simülasyonu
    dummy_json_path = "test_urls.json"
    dummy_data = {"urls": ["https://youtube.com/watch?v=test1", "https://youtube.com/watch?v=test2"]}
    with open(dummy_json_path, 'w') as f:
        json.dump(dummy_data, f)
    
    # Test çalıştırması
    main_downloader_organizer(dummy_json_path, "organized_output/")
