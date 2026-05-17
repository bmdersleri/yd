# test_script.py

import os
import shutil
from pathlib import Path
# main_downloader.py'deki ana orkestrasyon fonksiyonunu test etmek için içe aktarılıyor.
from main_downloader import main_downloader_organizer 

# Test için kullanılan sabitler
TEST_INPUT_DIR = Path("test_input_urls/")
TEST_DOWNLOAD_DIR = Path("test_downloads/")
TEST_OUTPUT_DIR = Path("test_organized_output/")
TEST_JSON_PATH = "test_input_urls/test_links.json"

def setup_test_environment():
    """Test için gerekli tüm dizinleri temizler ve yeniden oluşturur."""
    print("--- Test Ortamı Kuruluyor ---")
    
    # Önceki test verilerini temizle
    for dir_name in ["test_input_urls", "test_downloads", "test_organized_output"]:
        path = Path(dir_name)
        if path.exists():
            shutil.rmtree(path)
            print(f"Temizlendi: {dir_name}")

    # Yeni dizinleri oluştur
    TEST_INPUT_DIR.mkdir()
    TEST_DOWNLOAD_DIR.mkdir()
    TEST_OUTPUT_DIR.mkdir()
    print("Yeni test dizinleri oluşturuldu.")

def create_dummy_json(urls: list[str]):
    """Test için örnek bir JSON dosyası oluşturur."""
    dummy_data = {"urls": urls}
    path = Path(TEST_JSON_PATH)
    with open(path, 'w', encoding='utf-8') as f:
        import json
        json.dump(dummy_data, f)
    print(f"Dummy JSON dosyası oluşturuldu: {TEST_JSON_PATH}")

def run_test_case(test_urls: list[str]):
    """
    Belirtilen URL listesi ile ana orkestrasyon fonksiyonunu test eder.
    """
    print("\n" + "="*60)
    print("         🚀 TEST BAŞLIYOR: video_downloader_organizer() 🚀")
    print("="*60)
    
    # 1. Test ortamını kur
    setup_test_environment()
    
    # 2. Dummy veriyi oluştur
    create_dummy_json(test_urls)
    
    # 3. Fonksiyonu çalıştır (Test edilecek kısım)
    try:
        main_downloader_organizer(json_file_path=TEST_JSON_PATH, target_directory=str(TEST_OUTPUT_DIR))
        print("\n✅ TEST BAŞARILI: Fonksiyon hatasız bir şekilde çalıştı.")
    except Exception as e:
        print(f"\n❌ TEST BAŞARISIZ: Bir hata oluştu. Hata Detayı: {e}")

def cleanup_test_environment():
    """Test sonrası tüm geçici dosyaları temizler."""
    print("\n--- Test Ortamı Temizleniyor ---")
    for dir_name in ["test_input_urls", "test_downloads", "test_organized_output"]:
        path = Path(dir_name)
        if path.exists():
            shutil.rmtree(path)
            print(f"Temizlendi: {dir_name}")

if __name__ == "__main__":
    # Test edilecek örnek URL'ler
    test_urls_list = [
        "https://youtube.com/watch?v=test1", 
        "https://youtube.com/watch?v=test2"
    ]
    
    try:
        run_test_case(test_urls_list)
    finally:
        # Testten bağımsız olarak temizlik yapılmalı
        cleanup_test_environment()
        print("\n===========================================================")
        print("Tüm testler tamamlandı. Ortam temizlendi.")
        print("===========================================================")

# Not: Gerçek bir test ortamında, bu script 'pytest' ile çalıştırılmalı ve 
# main_downloader.py'deki TODO kısımları doldurulduktan sonra tüm adımlar test edilmelidir.