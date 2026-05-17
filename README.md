# 🎥 Video Downloader & Organizer Pipeline

## 📜 Project Overview
This automated system is designed to ingest a list of video URLs from a JSON file, extract comprehensive metadata, download the videos at high speed, and organize them into a structured, user-friendly output directory. The entire pipeline is encapsulated as a callable tool via the Model Context Protocol (MCP).

## 🌟 Key Features
*   **Metadata Extraction:** Uses `yt-dlp` to reliably extract titles, durations, and uploaders.
*   **High-Speed Downloading:** Employs `aria2c` for efficient, multi-threaded downloading.
*   **Organization:** Automatically renames and moves the downloaded files into a clean, structured output folder based on extracted metadata.
*   **Tooling:** The entire process is exposed via the `video_downloader_organizer` MCP tool.

## 🛠️ Kurulum ve Çalıştırma (Setup & Execution)

### 1. Ön Koşullar (Prerequisites)
Bu projenin çalışması için sisteminizde aşağıdaki araçların kurulu olması ve PATH'te bulunması gerekir:
*   **Python 3.x**
*   **yt-dlp:** Video metaverisi çekmek için.
*   **aria2c:** Yüksek hızlı indirme için.

### 2. Kurulum Adımları
1.  **Ortamı Aktif Etme:**
    ```bash
    source venv/bin/activate
    ```
2.  **Bağımlılıkları Yükleme:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Çalışma Akışı (Workflow)
1.  **Giriş Verisi:** İşlenecek URL'leri `input_urls/` klasöründeki bir JSON dosyasına yerleştirin.
    *   **Format:** `{"urls": ["url1", "url2", ...]}`
2.  **Çalıştırma:** Sistemi ana orkestrasyon aracı üzerinden çağırın. (MCP ortamında bu, aracı çağırmak anlamına gelir.)

    ```bash
    # Test amaçlı manuel çalıştırma (MCP ortamı yoksa)
    python3 mcp_tools.py 
    ```

## ⚙️ Teknik Detaylar (Technical Deep Dive)

### 📂 Dosya Yapısı
*   `input_urls/`: Giriş JSON dosyaları.
*   `downloads/`: Tüm ham indirme işlemleri bu geçici alanda yapılır.
*   `organized_output/`: Kullanıcıya sunulacak, düzenlenmiş ve sıralanmış son videolar.
*   `main_downloader.py`: İş akışını yöneten çekirdek Python mantığı.
*   `mcp_tools.py`: Bu mantığı LLM'e sunulan standart bir araç (tool) imzasına dönüştürür.

## 🔄 Güncelleme Geçmişi (Changelog)
*   **v1.0.0 (Initial Release):** Core pipeline logic implemented.
    *   Added metadata extraction using `yt-dlp`.
    *   Implemented high-speed downloading using `aria2c`.
    *   Added file organization logic using `shutil`.
    *   Encapsulated the entire process into the `video_downloader_organizer` MCP tool.

***

**Bu dosya, projenin tüm geliştirme sürecini ve kullanım kılavuzunu kapsayan nihai dokümantasyondur.**
