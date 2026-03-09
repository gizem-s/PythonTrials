# 📚 İnteraktif Grafik Sistemine Hoşgeldiniz!

## 🎯 Sistem Hakkında

Bu sistem size **19 farklı grafik türü** sunarak veri analizi ve görselleştirme yapmanızı sağlar. Her grafik, CLI parametreleri ile istenildiğinde kolayca oluşturulabilir.

---

## 📊 Grafik Kategorileri

### 🎯 TEMEL GRAFİKLER (6)
Veri analizi için en temel ve sık kullanılan grafikler.

| # | Grafik | Komut | Açıklama |
|---|--------|-------|----------|
| 1 | **Line Chart** | `python3 interactive_charts.py line_chart` | Zaman serisine göre trend gösterir |
| 2 | **Bar Chart** | `python3 interactive_charts.py bar_chart` | Kategorileri karşılaştırır |
| 3 | **Histogram** | `python3 interactive_charts.py histogram` | Değişkenin dağılımını gösterir |
| 4 | **Scatter Plot** | `python3 interactive_charts.py scatter_plot` | İki değişken arasındaki ilişkiyi gösterir |
| 5 | **Pie Chart** | `python3 interactive_charts.py pie_chart` | Yüzdelik dağılımı gösterir |
| 6 | **Box Plot** | `python3 interactive_charts.py box_plot` | Dörtlü analiz (quartile) yapır |

**Ne Zaman Kullanılır?**
- Verinin genel dağılımını görmek istediğinizde
- Kategoriler arasında basit karşılaştırma yapmak istediğinizde
- Hızlı ve anlaşılır grafikler oluşturmak istediğinizde

---

### 📈 İLERİ GRAFİKLER (6)
Daha kompleks ilişkileri ve dağılımları gösterir.

| # | Grafik | Komut | Açıklama |
|---|--------|-------|----------|
| 7 | **Heatmap** | `python3 interactive_charts.py heatmap` | Kategorik değişkenler arasındaki yoğunluğu renkle gösterir |
| 8 | **Violin Plot** | `python3 interactive_charts.py violin_plot` | Dağılımın şeklini detaylı gösterir |
| 9 | **3D Scatter** | `python3 interactive_charts.py scatter_3d` | Üç değişkeni aynı anda gösterir |
| 10 | **KDE Plot** | `python3 interactive_charts.py kde_plot` | Yoğunluk tahminini gösterir |
| 11 | **Hexbin Plot** | `python3 interactive_charts.py hexbin_plot` | 2D yoğunluğu altıgenlerle gösterir |
| 12 | **Waterfall** | `python3 interactive_charts.py waterfall_chart` | Satış/gider/kar akışını gösterir |

**Ne Zaman Kullanılır?**
- Verinin istatistiksel özelliklerini incelemek istediğinizde
- Çok sayıda değişken arasındaki ilişkiyi görmek istediğinizde
- Yoğunluk ve dağılım analizleri yapmak istediğinizde

---

### 🎨 KÖŞELİ GRAFİKLER (6)
Özel visualisasyon tekniklerini kullanır.

| # | Grafik | Komut | Açıklama |
|---|--------|-------|----------|
| 13 | **Stacked Bar** | `python3 interactive_charts.py stacked_bar` | Kategorileri yığılı çubuklar şeklinde gösterir |
| 14 | **Grouped Bar** | `python3 interactive_charts.py grouped_bar` | Kategorileri yan yana çubuklar şeklinde gösterir |
| 15 | **Area Chart** | `python3 interactive_charts.py area_chart` | Zaman içinde değişim alanı şeklinde gösterir |
| 16 | **Density Contour** | `python3 interactive_charts.py density_contour` | Yoğunluk konturlarını gösterir |
| 17 | **Correlation** | `python3 interactive_charts.py correlation_matrix` | Değişkenler arasında korelasyon gösterir |
| 18 | **Swarm Plot** | `python3 interactive_charts.py swarm_plot` | Veri noktalarını birbirinden ayrı gösterir |

**Ne Zaman Kullanılır?**
- Kategorik verileri karşılaştırmak istediğinizde
- Değişkenler arasında korelasyon bulmak istediğinizde
- Detaylı kategorik analizler yapmak istediğinizde

---

### 📊 ÖZET GRAFİKLER (1)
Birden fazla grafiği bir arada sunar.

| # | Grafik | Komut | Açıklama |
|---|--------|-------|----------|
| 19 | **Dashboard** | `python3 interactive_charts.py dashboard` | 6 grafik bir arada |

---

## 💡 Kullanım Örnekleri

### Örnek 1: Satış Trendini Görmek
```bash
python3 interactive_charts.py line_chart
# Result: charts/T01_line_chart.png
```

### Örnek 2: Bölge Dağılımını Görmek
```bash
python3 interactive_charts.py pie_chart
# Result: charts/T05_pie_chart.png
```

### Örnek 3: Kategori-Bölge İlişkisini Görmek
```bash
python3 interactive_charts.py heatmap
# Result: charts/I01_heatmap.png
```

### Örnek 4: Korelasyon Analizi Yapmak
```bash
python3 interactive_charts.py correlation_matrix
# Result: charts/K05_correlation_matrix.png
```

### Örnek 5: Tüm Grafikleri Bir Defada Oluşturmak
```bash
python3 interactive_charts.py all
# Result: 19 grafik oluşturulur
```

### Örnek 6: Dashboard Görüntülemek
```bash
python3 interactive_charts.py dashboard
# Result: charts/O01_dashboard.png (hepsi bir arada)
```

---

## 📁 Dosya Yapısı

```
charts/
├── T01_line_chart.png          # Temel: Line Chart
├── T02_bar_chart.png           # Temel: Bar Chart
├── T03_histogram.png           # Temel: Histogram
├── T04_scatter_plot.png        # Temel: Scatter Plot
├── T05_pie_chart.png           # Temel: Pie Chart
├── T06_box_plot.png            # Temel: Box Plot
├── I01_heatmap.png             # İleri: Heatmap
├── I02_violin_plot.png         # İleri: Violin Plot
├── I03_3d_scatter.png          # İleri: 3D Scatter
├── I04_kde_plot.png            # İleri: KDE Plot
├── I05_hexbin_plot.png         # İleri: Hexbin Plot
├── I06_waterfall_chart.png     # İleri: Waterfall
├── K01_stacked_bar.png         # Köşeli: Stacked Bar
├── K02_grouped_bar.png         # Köşeli: Grouped Bar
├── K03_area_chart.png          # Köşeli: Area Chart
├── K04_density_contour.png     # Köşeli: Density Contour
├── K05_correlation_matrix.png  # Köşeli: Correlation
├── K06_swarm_plot.png          # Köşeli: Swarm Plot
└── O01_dashboard.png           # Özet: Dashboard
```

---

## 🛠️ Teknik Bilgiler

### Gerekli Kütüphaneler
```
pandas       - Veri işleme
matplotlib   - Temel grafik oluşturma
seaborn      - İleri görselleştirmeler
numpy        - Sayısal hesaplamalar
scipy        - Bilimsel hesaplamalar
```

### Grafik Özellikleri
- **Çözünürlük**: 300 DPI (yüksek kalite)
- **Format**: PNG
- **Boyut**: Grafik türüne göre değişir (10-16 inç)
- **Renkler**: Kolorblind dostu paletler

### Veri Özellikleri
- **Örneklem Sayısı**: 100 satır
- **Değişkenler**: Satış, Gider, Müşteri Sayısı, Ürün Kategorisi, Mağaza Bölgesi
- **Ürün Kategorileri**: Elektronik, Giyim, Yiyecek, Kitap
- **Mağaza Bölgeleri**: İstanbul, Ankara, İzmir, Bursa

---

## 🎓 Öğrenme İpuçları

### Başlangıç Seviyesi
1. `line_chart` ile temel trend analizi başlayın
2. `bar_chart` ile kategorik karşılaştırma yapın
3. `pie_chart` ile yüzdelik dağılımları görmek

### Orta Seviye
1. `scatter_plot` ile iki değişken arasındaki ilişkiyi inceleyin
2. `heatmap` ile kategorik ilişkileri analiz edin
3. `histogram` ve `kde_plot` ile dağılımları karşılaştırın

### İleri Seviye
1. `scatter_3d` ile çok boyutlu analizler yapın
2. `correlation_matrix` ile değişkenler arasında ilişkileri bulun
3. `waterfall_chart` ile finansal analiz yapın
4. `dashboard` ile genel özet oluşturun

---

## ❓ Sık Sorulan Sorular

**S: Yeni grafik türü nasıl eklerim?**
A: `interactive_charts.py` dosyasına yeni bir metod ekleyerek istediğiniz grafik türünü oluşturabilirsiniz.

**S: Grafikleri PDF olarak kaydedebilir miyim?**
A: Evet! `kaydet()` metodunda `'charts/{isim}.pdf'` yazarak PDF formatında kaydedebilirsiniz.

**S: Verimi kendi CSV dosyamla değiştirebilir miyim?**
A: Evet! `sales_data.csv` dosyasını değiştirerek script'i çalıştırabilirsiniz.

**S: Grafikleri web'de yayınlayabilir miyim?**
A: Evet! Plotly gibi interaktif kütüphanelerle dönüştürebilirsiniz.

---

## 📝 Not Defteri

Grafiklerin kullanımıyla ilgili not defteriniz:

```python
# Veri analizi adımları:
# 1. Veriyi yükle (CSV)
# 2. Temel grafikleri çiz (Line, Bar)
# 3. Dağılım analiz et (Histogram, KDE)
# 4. İlişkileri incele (Scatter, Heatmap)
# 5. Sonuçları dashboard'da sunarız
```

---

**Sorularınız veya önerileriniz mi var? Bana yazabilirsiniz!** 🚀

GitHub Copilot | Mart 2026

