# mcp_tools.py

from main_downloader import main_downloader_organizer
from pathlib import Path
import os

def video_downloader_organizer(json_file_path: str, target_directory: str) -> str:
    """
    Model Context Protocol (MCP) Aracı: 
    Verilen JSON dosyasındaki video URL listesini alır, metaveri çıkarır, 
    videoları yüksek hızda indirir ve belirtilen hedef dizinde düzenli bir şekilde düzenler.
    
    Args:
        json_file_path (str): URL'lerin bulunduğu JSON dosyasının yolu.
        target_directory (str): İndirilen videoların düzenleneceği hedef dizin.
        
    Returns:
        str: İşlemin başarılı olup olmadığına dair özet bir mesaj.
    """
    print(f"--- MCP Aracı Başlatıldı: {json_file_path} -> {target_directory} ---")
    
    try:
        # Ana iş akışını çağırıyoruz.
        main_downloader_organizer(json_file_path, target_directory)
        
        return f"✅ Başarıyla tamamlandı! {json_file_path} dosyasındaki videolar başarıyla indirildi ve '{target_directory}' klasörüne düzenlendi."
    except Exception as e:
        return f"❌ Bir hata oluştu: {e}"

# Bu dosya, MCP sunucusunun yükleyeceği araç arayüzünü temsil eder.
