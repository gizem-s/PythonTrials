# PythonTrial - Veri Analiz Proje

İlk Python projesi - Veri görselleştirme ve analiz pratiği.

## 📁 Proje Yapısı

```
PythonTrial/
├── main.py                  # Ana dosya
├── create_data.py          # Random CSV veri oluşturma
├── generate_charts.py      # Basit grafikler
├── advanced_charts.py      # Gelişmiş grafikler (10 çeşit)
├── GRAFIKLER.md           # Grafiklerin detaylı açıklaması
├── charts/                # Oluşturulan grafikler klasörü
│   ├── 01_heatmap.png
│   ├── 02_violin_plot.png
│   ├── 03_3d_scatter.png
│   ├── 04_kde_distributions.png
│   ├── 05_correlation_heatmap.png
│   ├── 06_stacked_bar.png
│   ├── 07_multi_pie.png
│   ├── 08_hexbin.png
│   ├── 09_grouped_bar.png
│   └── 10_waterfall.png
├── sales_data.csv         # Random satış verisi
└── .gitignore            # Git yapılandırması
```

## 🚀 Hızlı Başlangıç

### Adım 1: Veri Oluştur
```bash
python3 create_data.py
```
Bu komut `sales_data.csv` dosyasını 100 satırlık random veri ile oluşturur.

### Adım 2: İnteraktif Grafik Seçer Kullan
```bash
python3 interactive_charts.py [grafik_adi]
```

#### 🎯 Temel Grafikler (6):
```bash
python3 interactive_charts.py line_chart       # Zaman serisine göre trend
python3 interactive_charts.py bar_chart        # Kategori/bölge karşılaştırması
python3 interactive_charts.py histogram        # Değişken dağılımı
python3 interactive_charts.py scatter_plot     # İki değişken ilişkisi
python3 interactive_charts.py pie_chart        # Yüzdelik dağılım
python3 interactive_charts.py box_plot         # Dörtlü analiz
```

#### 📈 İleri Grafikler (6):
```bash
python3 interactive_charts.py heatmap          # Kategorik ilişkiler
python3 interactive_charts.py violin_plot      # Dağılım şekli
python3 interactive_charts.py scatter_3d       # Üç değişken analizi
python3 interactive_charts.py kde_plot         # Yoğunluk tahmini
python3 interactive_charts.py hexbin_plot      # 2D yoğunluk
python3 interactive_charts.py waterfall_chart  # Satış/gider/kar akışı
```

#### 🎨 Köşeli Grafikler (6):
```bash
python3 interactive_charts.py stacked_bar      # Yığılı çubuklar
python3 interactive_charts.py grouped_bar      # Gruplandırılmış çubuklar
python3 interactive_charts.py area_chart       # Alan grafiği
python3 interactive_charts.py density_contour  # Yoğunluk konturları
python3 interactive_charts.py correlation_matrix # Korelasyon tablosu
python3 interactive_charts.py swarm_plot       # Veri noktaları çiçeği
```

#### 📊 Özet Grafikler (1):
```bash
python3 interactive_charts.py dashboard        # Hepsi bir arada
```

### Adım 3: İstatistiksel Anlamlılık Grafikleri Oluştur
```bash
python3 interactive_charts.py statistical_significance_demo
```
Bu komut istatistiksel anlamlılık gösteren kapsamlı bir grafik oluşturur:
- T-Test karşılaştırmaları
- Güven aralıkları
- p-Value ısı haritası
- İstatistiksel yorumlar

### Adım 4: Tüm Grafikleri Bir Kerede Oluştur
```bash
python3 interactive_charts.py all
```
25 farklı grafik türünü otomatik olarak oluşturur.

### Adım 3 (İsteğe Bağlı): Eski Script'ler
```bash
python3 generate_charts.py       # 6 basit grafik
python3 advanced_charts.py       # 10 gelişmiş grafik
```

## 📊 Grafikler Hakkında

Tüm grafiklerin detaylı açıklaması için `GRAFIKLER.md` dosyasını okuyun.

## 📦 Gerekli Kütüphaneler

```bash
pip install pandas matplotlib seaborn numpy scipy
```

## ⚙️ Teknolojiler

- **Python 3.9+**
- **Pandas**: Veri işleme
- **Matplotlib**: Grafik oluşturma
- **Seaborn**: İleri görselleştirmeler
- **NumPy**: Sayısal hesaplamalar
- **SciPy**: Bilimsel hesaplamalar

## 🔧 Git Yapılandırması

`.gitignore` dosyası aşağıdakileri GitHub'a yüklemeyecek:
- `.png`, `.jpg`, `.jpeg`, `.gif` (görüntü dosyaları)
- `.csv` (veri dosyaları)
- `charts/` (grafik klasörü)
- Python cache dosyaları
- Virtual environment

## 📝 Notlar

- Veriler random olarak oluşturulur (`np.random.seed(42)`)
- Her seferinde `create_data.py` çalıştırıldığında yeni veriler oluşur
- Grafikler `charts/` klasöründe 300 DPI'da kaydedilir

---

**Hazırlayan**: GitHub Copilot  
**Tarih**: Mart 2026  
**Durum**: Eğitim Amaçlı

