import yt_dlp

def ses_indir(url):
    """
    Verilen URL'deki videonun sadece sesini indirir ve MP3 formatına çevirir.
    """
    
    ydl_opts = {
        # Sadece en iyi ses kalitesini seçer, video indirmez
        'format': 'bestaudio/best',
        
        # İndirilen dosyanın adını belirler: "Videonun Orijinal Başlığı.mp3"
        'outtmpl': '%(title)s.%(ext)s',
        
        # İndirme sonrası işlemleri (post-processing) tanımlar
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',   # Dönüştürülecek format (mp3, m4a, wav vb. olabilir)
            'preferredquality': '192', # Ses kalitesi (kbps cinsinden, örn: 192, 256, 320)
        }],
        
        # --- aria2c Entegrasyonu (İsteğe bağlı, indirmeyi hızlandırır) ---
        'external_downloader': 'aria2c',
        'external_downloader_args': {
            'default': ['-x', '16', '-s', '16', '-k', '1M']
        },
        
        'quiet': False,
        'no_warnings': True
    }

    try:
        print(f"Hedef URL: {url}\nSadece ses indiriliyor ve MP3'e dönüştürülüyor...\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        print("\n✅ Ses indirme ve MP3'e dönüştürme işlemi başarıyla tamamlandı!")
        
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ İndirme hatası: {e}")
    except Exception as e:
        print(f"\n❌ Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    hedef_url = "https://www.youtube.com/watch?v=upshdP-1K_0"
    ses_indir(hedef_url)