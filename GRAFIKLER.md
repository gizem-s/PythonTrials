# 📊 Gelişmiş Veri Analiz Grafikleri

Bu dosya, `advanced_charts.py` tarafından oluşturulan grafikleri açıklar.

## Grafikler

### 1️⃣ Heatmap (`01_heatmap.png`)
- **Açıklama**: Ürün kategorileri ile mağaza bölgeleri arasında satış ilişkisini gösteren ısı haritası
- **Kullanım**: Hangi bölgede hangi ürün kategorisinin daha iyi satış yaptığını anlamak
- **Renk Kodu**: Açık renkler az satış, koyu renkler fazla satış

### 2️⃣ Violin Plot (`02_violin_plot.png`)
- **Açıklama**: Bölgelere göre satış dağılımını gösteren ayakkabı şeklindeki grafik
- **Kullanım**: Satışların dağılımının şeklini ve merkezini görmek
- **Siyah Noktalar**: Bireysel veri noktaları

### 3️⃣ 3D Scatter Plot (`03_3d_scatter.png`)
- **Açıklama**: Müşteri sayısı, gider ve satış olmak üzere üç değişkeni aynı anda gösteren grafik
- **Kullanım**: Üç değişken arasındaki ilişkiyi görselleştirmek
- **Renkler**: Farklı ürün kategorilerini temsil eder

### 4️⃣ KDE Distributions (`04_kde_distributions.png`)
- **Açıklama**: Satış, gider, müşteri sayısı ve kar değişkenlerinin yoğunluk dağılımı
- **Kullanım**: Verinin nasıl dağıldığını ve en sık hangi değerlerin bulunduğunu görmek
- **Histogram + Eğri**: Frekans ve yoğunluk bilgisini bir arada sunar

### 5️⃣ Correlation Heatmap (`05_correlation_heatmap.png`)
- **Açıklama**: Sayısal değişkenler arasındaki korelasyon katsayılarını gösteren ısı haritası
- **Kullanım**: Değişkenler arasında güçlü/zayıf ilişkileri bulmak
- **Renk Kodu**: Kırmızı pozitif korelasyon, mavi negatif korelasyon

### 6️⃣ Stacked Bar Chart (`06_stacked_bar.png`)
- **Açıklama**: Bölgelere göre ürün kategorilerinin yığılı çubuk grafiği
- **Kullanım**: Bölgelerde kategori satışlarının oranını görmek
- **Yığılmış Formatı**: Hem total hem de dağılımı anlamak için kullanılır

### 7️⃣ Multi-Level Pie Charts (`07_multi_pie.png`)
- **Açıklama**: İki ayrı pasta grafiği - bölge dağılımı ve kategori dağılımı
- **Kullanım**: Satışların yüzdelik dağılımını görmek
- **Yüzdeler**: Her dilimin oranını yüzdeyle gösterir

### 8️⃣ Hexbin Plot (`08_hexbin.png`)
- **Açıklama**: Müşteri sayısı vs satış ilişkisini altıgen yoğunluk haritası ile gösteren grafik
- **Kullanım**: İki değişken arasında yoğunluk ilişkisini görmek
- **Renk Kodu**: Koyu renkler yüksek frekans, açık renkler düşük frekans

### 9️⃣ Grouped Bar Chart (`09_grouped_bar.png`)
- **Açıklama**: Bölgelere göre kategori başına ortalama satış (yan yana çubuklar)
- **Kullanım**: Kategoriler arasında karşılaştırma yapmak
- **Detaylı Analiz**: Her bölge-kategori kombinasyonun ortalamasını görmek

### 🔟 Waterfall Chart (`10_waterfall.png`)
- **Açıklama**: Bölgelere göre satış, gider ve kar değişimini gösteren grafik
- **Kullanım**: Satış ve maliyetlerin kar üzerine etkisini anlamak
- **Mor Çizgi**: Kar trendini gösterir

## Grafikleri Oluşturma

Tüm grafikleri oluşturmak için:

```bash
python3 advanced_charts.py
```

Grafikler `charts/` klasöründe `.png` formatında kaydedilir.

## Gerekli Kütüphaneler

- pandas
- matplotlib
- seaborn
- numpy
- scipy

Kurulum:
```bash
pip install pandas matplotlib seaborn numpy scipy
```

## Veri Kaynağı

Grafikler `sales_data.csv` dosyasından okur. Bu dosyayı oluşturmak için:

```bash
python3 create_data.py
```

---

**Not**: Bu grafikler eğitim ve deneme amaçlıdır ve random veri kullanır.

