# DualFusion

DualFusion, dizi bölümleri için orijinal ve Türkçe dublaj sesleri birleştirip, istenirse altyazı ekleyerek tek dosyada mux işlemi yapan, PyQt5 tabanlı bir masaüstü uygulamasıdır.

## Özellikler
- Sürükle-bırak ile kolay dosya ekleme
- **Klasör sürükle-bırak desteği**: Bir klasörü bıraktığınızda içindeki tüm uygun dosyalar otomatik eklenir
- Dual (Orijinal + Türkçe) veya sadece Türkçe dublaj seçeneği
- Altyazı desteği (isteğe bağlı)
- FFmpeg ile hızlı ve kayıpsız mux işlemi
- Koyu (Nordic) tema
- Kullanıcı dostu arayüz

## Gereksinimler
- Python 3.7+
- PyQt5
- ffmpeg.exe (uygulama ile aynı klasörde olmalı)

## Kurulum
1. Gerekli paketleri yükleyin:
   ```bash
   pip install PyQt5
   ```
2. [FFmpeg](https://ffmpeg.org/download.html) indirin ve `ffmpeg.exe` dosyasını bu script ile aynı klasöre koyun.

## Kullanım
1. Uygulamayı başlatın:
   ```bash
   python main.py
   ```
2. Dizi bölümü, ses ve altyazı dosyalarını sürükleyip bırakın.
3. Ses modunu ve gecikmeyi seçin.
4. "Dizileri İşle" butonuna tıklayın.

## Lisans
MIT

## Katkı
Pull request ve issue'larınızı bekliyorum!

---

Kod: [xmtaha](https://github.com/xmtaha)
