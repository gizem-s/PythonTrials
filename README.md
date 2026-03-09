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

### Adım 2: Basit Grafikler Oluştur
```bash
python3 generate_charts.py
```
6 farklı grafik türünü oluşturur:
- Line Chart (Satış & Gider Trendi)
- Bar Chart (Kategoriye Göre Satış)
- Histogram (Satış Dağılımı)
- Scatter Plot (Müşteri vs Satış)
- Pie Chart (Bölge Dağılımı)
- Box Plot (Bölgesel Analiz)

### Adım 3: Gelişmiş Grafikler Oluştur
```bash
python3 advanced_charts.py
```
10 farklı ileri grafik türünü oluşturur:
- Heatmap
- Violin Plot
- 3D Scatter Plot
- KDE Distributions
- Correlation Heatmap
- Stacked Bar Chart
- Multi-Level Pie Charts
- Hexbin Plot
- Grouped Bar Chart
- Waterfall Chart

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

