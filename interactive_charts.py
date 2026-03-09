import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os
import sys

# Türkçe karakter desteği
plt.rcParams['figure.facecolor'] = '#f8f9fa'

# CSV dosyasını oku
df = pd.read_csv('sales_data.csv')
df['Kar'] = df['Satış'] - df['Gider']

class GrafikOlusturucu:
    def __init__(self):
        self.df = df
        os.makedirs('charts', exist_ok=True)

    def kaydet(self, fig, isim):
        """Grafiği kaydet"""
        dosya_adi = f'charts/{isim}.png'
        fig.savefig(dosya_adi, dpi=300, bbox_inches='tight')
        print(f"✅ {dosya_adi}")
        plt.close(fig)

    # ============ TEMEL GRAFİKLER (6) ============
    def line_chart(self):
        """Zaman serisine göre trend"""
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(self.df.index[:50], self.df['Satış'][:50], marker='o', label='Satış', linewidth=2, color='#2ecc71')
        ax.plot(self.df.index[:50], self.df['Gider'][:50], marker='s', label='Gider', linewidth=2, color='#e74c3c')
        ax.set_title('Satış ve Gider Trendi', fontsize=14, fontweight='bold')
        ax.set_xlabel('Veri Indeksi')
        ax.set_ylabel('Tutar')
        ax.legend()
        ax.grid(True, alpha=0.3)
        self.kaydet(fig, 'T01_line_chart')

    def bar_chart(self):
        """Kategori/bölge karşılaştırması"""
        fig, ax = plt.subplots(figsize=(10, 6))
        kategoriler = self.df.groupby('Ürün_Kategorisi')['Satış'].sum().sort_values(ascending=False)
        ax.bar(kategoriler.index, kategoriler.values, color='#3498db', edgecolor='black')
        ax.set_title('Ürün Kategorisine Göre Toplam Satış', fontsize=14, fontweight='bold')
        ax.set_ylabel('Satış (Tutar)')
        ax.tick_params(axis='x', rotation=45)
        self.kaydet(fig, 'T02_bar_chart')

    def histogram(self):
        """Değişken dağılımı"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(self.df['Satış'], bins=25, color='#9b59b6', edgecolor='black', alpha=0.7)
        ax.set_title('Satış Dağılımı', fontsize=14, fontweight='bold')
        ax.set_xlabel('Satış Miktarı')
        ax.set_ylabel('Frekans')
        ax.grid(True, alpha=0.3, axis='y')
        self.kaydet(fig, 'T03_histogram')

    def scatter_plot(self):
        """İki değişken ilişkisi"""
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(self.df['Müşteri_Sayısı'], self.df['Satış'],
                            c=self.df['Kar'], s=100, alpha=0.6, cmap='viridis', edgecolors='black')
        ax.set_title('Müşteri Sayısı vs Satış', fontsize=14, fontweight='bold')
        ax.set_xlabel('Müşteri Sayısı')
        ax.set_ylabel('Satış')
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Kar')
        self.kaydet(fig, 'T04_scatter_plot')

    def pie_chart(self):
        """Yüzdelik dağılım"""
        fig, ax = plt.subplots(figsize=(10, 8))
        bolge_satış = self.df.groupby('Mağaza_Bölgesi')['Satış'].sum()
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        wedges, texts, autotexts = ax.pie(bolge_satış.values, labels=bolge_satış.index,
                                           autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Bölgelere Göre Satış Dağılımı', fontsize=14, fontweight='bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        self.kaydet(fig, 'T05_pie_chart')

    def box_plot(self):
        """Dörtlü analiz"""
        fig, ax = plt.subplots(figsize=(10, 6))
        self.df.boxplot(column='Satış', by='Mağaza_Bölgesi', ax=ax)
        ax.set_title('Bölgelere Göre Satış Dağılımı', fontsize=14, fontweight='bold')
        ax.set_xlabel('Bölge')
        ax.set_ylabel('Satış')
        plt.suptitle('')
        self.kaydet(fig, 'T06_box_plot')

    # ============ İLERİ GRAFİKLER (6) ============
    def heatmap(self):
        """Kategorik ilişkiler"""
        fig, ax = plt.subplots(figsize=(10, 8))
        pivot_data = self.df.pivot_table(values='Satış', index='Ürün_Kategorisi',
                                        columns='Mağaza_Bölgesi', aggfunc='sum')
        sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlGnBu',
                   cbar_kws={'label': 'Satış'}, linewidths=1, ax=ax)
        ax.set_title('Kategori x Bolge Satislari', fontsize=14, fontweight='bold')
        self.kaydet(fig, 'I01_heatmap')

    def violin_plot(self):
        """Dağılım şekli"""
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.violinplot(data=self.df, x='Mağaza_Bölgesi', y='Satış', ax=ax, palette='Set2')
        sns.stripplot(data=self.df, x='Mağaza_Bölgesi', y='Satış',
                     color='black', alpha=0.3, size=4, ax=ax)
        ax.set_title('Bölgelere Göre Satış Dağılımı (Violin)', fontsize=14, fontweight='bold')
        self.kaydet(fig, 'I02_violin_plot')

    def scatter_3d(self):
        """Üç değişken analizi"""
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        colors_dict = {'Elektronik': '#e74c3c', 'Giyim': '#3498db', 'Yiyecek': '#2ecc71', 'Kitap': '#f39c12'}
        for kategori in self.df['Ürün_Kategorisi'].unique():
            mask = self.df['Ürün_Kategorisi'] == kategori
            ax.scatter(self.df[mask]['Müşteri_Sayısı'],
                      self.df[mask]['Gider'],
                      self.df[mask]['Satış'],
                      c=colors_dict.get(kategori, '#95a5a6'),
                      label=kategori, s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
        ax.set_xlabel('Müşteri Sayısı')
        ax.set_ylabel('Gider')
        ax.set_zlabel('Satış')
        ax.set_title('3D Satış Analizi', fontsize=14, fontweight='bold')
        ax.legend()
        self.kaydet(fig, 'I03_3d_scatter')

    def kde_plot(self):
        """Yoğunluk tahmini"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Yoğunluk Dağılımları (KDE)', fontsize=14, fontweight='bold')

        axes[0, 0].hist(self.df['Satış'], bins=20, alpha=0.5, color='#3498db', edgecolor='black')
        self.df['Satış'].plot(kind='kde', ax=axes[0, 0], color='#e74c3c', linewidth=2)
        axes[0, 0].set_title('Satış')

        axes[0, 1].hist(self.df['Gider'], bins=20, alpha=0.5, color='#2ecc71', edgecolor='black')
        self.df['Gider'].plot(kind='kde', ax=axes[0, 1], color='#e74c3c', linewidth=2)
        axes[0, 1].set_title('Gider')

        axes[1, 0].hist(self.df['Müşteri_Sayısı'], bins=20, alpha=0.5, color='#f39c12', edgecolor='black')
        self.df['Müşteri_Sayısı'].plot(kind='kde', ax=axes[1, 0], color='#e74c3c', linewidth=2)
        axes[1, 0].set_title('Müşteri Sayısı')

        axes[1, 1].hist(self.df['Kar'], bins=20, alpha=0.5, color='#9b59b6', edgecolor='black')
        self.df['Kar'].plot(kind='kde', ax=axes[1, 1], color='#e74c3c', linewidth=2)
        axes[1, 1].set_title('Kar')

        self.kaydet(fig, 'I04_kde_plot')

    def hexbin_plot(self):
        """2D yoğunluk"""
        fig, ax = plt.subplots(figsize=(10, 8))
        hexbin = ax.hexbin(self.df['Müşteri_Sayısı'], self.df['Satış'],
                          gridsize=15, cmap='YlOrRd', mincnt=1)
        ax.set_xlabel('Müşteri Sayısı')
        ax.set_ylabel('Satış')
        ax.set_title('Müşteri vs Satış (Hexbin Yoğunluk)', fontsize=14, fontweight='bold')
        plt.colorbar(hexbin, ax=ax, label='Frekans')
        self.kaydet(fig, 'I05_hexbin_plot')

    def waterfall_chart(self):
        """Satış/gider/kar akışı"""
        fig, ax = plt.subplots(figsize=(12, 6))
        bolge_satış = self.df.groupby('Mağaza_Bölgesi').agg({'Satış': 'sum', 'Gider': 'sum'})
        bolge_satış['Kar'] = bolge_satış['Satış'] - bolge_satış['Gider']
        x_pos = np.arange(len(bolge_satış.index))
        ax.bar(x_pos, bolge_satış['Satış'], label='Satış', color='#2ecc71', edgecolor='black', linewidth=1.5)
        ax.bar(x_pos, bolge_satış['Gider'], label='Gider', color='#e74c3c', edgecolor='black', linewidth=1.5, alpha=0.7)
        ax.plot(x_pos, bolge_satış['Kar'], marker='o', color='#9b59b6', linewidth=3, markersize=10, label='Kar')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(bolge_satış.index)
        ax.set_ylabel('Tutar')
        ax.set_title('Bölgelere Göre Satış, Gider ve Kar', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        self.kaydet(fig, 'I06_waterfall_chart')

    # ============ KÖŞELİ GRAFİKLER (6) ============
    def stacked_bar(self):
        """Yığılı çubuklar"""
        fig, ax = plt.subplots(figsize=(12, 6))
        stacked_data = self.df.pivot_table(values='Satış', index='Mağaza_Bölgesi',
                                          columns='Ürün_Kategorisi', aggfunc='sum')
        stacked_data.plot(kind='bar', stacked=True, ax=ax,
                         color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'],
                         edgecolor='black', linewidth=1.5)
        ax.set_title('Bölgelere Göre Kategori Satışları (Stacked)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Satış')
        ax.set_xlabel('Bölge')
        ax.legend(title='Kategori', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.tick_params(axis='x', rotation=45)
        self.kaydet(fig, 'K01_stacked_bar')

    def grouped_bar(self):
        """Gruplandırılmış çubuklar"""
        fig, ax = plt.subplots(figsize=(12, 6))
        grouped_data = self.df.groupby(['Mağaza_Bölgesi', 'Ürün_Kategorisi'])['Satış'].mean().unstack()
        x = np.arange(len(grouped_data.index))
        width = 0.2
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
        for i, col in enumerate(grouped_data.columns):
            offset = (i - 1.5) * width
            ax.bar(x + offset, grouped_data[col], width, label=col, color=colors[i], edgecolor='black')
        ax.set_xlabel('Mağaza Bölgesi')
        ax.set_ylabel('Ortalama Satış')
        ax.set_title('Bölgelere Göre Kategori Başına Ortalama Satış', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(grouped_data.index)
        ax.legend(title='Kategori')
        ax.grid(True, alpha=0.3, axis='y')
        self.kaydet(fig, 'K02_grouped_bar')

    def area_chart(self):
        """Alan grafiği"""
        fig, ax = plt.subplots(figsize=(12, 6))
        for bolge in self.df['Mağaza_Bölgesi'].unique():
            bolge_data = self.df[self.df['Mağaza_Bölgesi'] == bolge]['Satış'].reset_index(drop=True)
            ax.fill_between(range(len(bolge_data)), bolge_data, alpha=0.5, label=bolge)
        ax.set_title('Bölgelere Göre Satış Alan Grafiği', fontsize=14, fontweight='bold')
        ax.set_xlabel('Örnek Numarası')
        ax.set_ylabel('Satış')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        self.kaydet(fig, 'K03_area_chart')

    def density_contour(self):
        """Yoğunluk konturları"""
        fig, ax = plt.subplots(figsize=(10, 8))
        x = self.df['Müşteri_Sayısı']
        y = self.df['Satış']
        ax.hexbin(x, y, gridsize=15, cmap='viridis', mincnt=1, edgecolors='none')
        ax.set_xlabel('Müşteri Sayısı')
        ax.set_ylabel('Satış')
        ax.set_title('Yoğunluk Haritası - Müşteri vs Satış', fontsize=14, fontweight='bold')
        self.kaydet(fig, 'K04_density_contour')

    def correlation_matrix(self):
        """Korelasyon tablosu"""
        fig, ax = plt.subplots(figsize=(10, 8))
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.df[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, linewidths=2, cbar_kws={'label': 'Korelasyon'},
                   vmin=-1, vmax=1, ax=ax)
        ax.set_title('Sayısal Değişkenler Korelasyonu', fontsize=14, fontweight='bold')
        self.kaydet(fig, 'K05_correlation_matrix')

    def swarm_plot(self):
        """Veri noktaları çiçeği"""
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.swarmplot(data=self.df, x='Mağaza_Bölgesi', y='Satış',
                     hue='Ürün_Kategorisi', size=8, ax=ax, palette='Set2')
        ax.set_title('Bölgelere Göre Satış Dağılımı (Swarm)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Satış')
        ax.set_xlabel('Bölge')
        self.kaydet(fig, 'K06_swarm_plot')

    # ============ ÖZET GRAFİKLER (2) ============
    def dashboard(self):
        """Hepsi bir arada"""
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle('SATIŞ ANALİZ DASHBOARD', fontsize=18, fontweight='bold')
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        ax1 = fig.add_subplot(gs[0, :2])
        ax1.plot(self.df.index[:30], self.df['Satış'][:30], marker='o', label='Satış', linewidth=2, color='#2ecc71')
        ax1.plot(self.df.index[:30], self.df['Gider'][:30], marker='s', label='Gider', linewidth=2, color='#e74c3c')
        ax1.set_title('Satış & Gider Trendi', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2 = fig.add_subplot(gs[0, 2])
        bolge_satış = self.df.groupby('Mağaza_Bölgesi')['Satış'].sum()
        ax2.pie(bolge_satış.values, labels=bolge_satış.index, autopct='%1.0f%%',
               colors=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
        ax2.set_title('Bölge Dağılımı', fontweight='bold')

        ax3 = fig.add_subplot(gs[1, 0])
        kategoriler = self.df.groupby('Ürün_Kategorisi')['Satış'].sum().sort_values(ascending=False)
        ax3.bar(kategoriler.index, kategoriler.values, color='#3498db', edgecolor='black')
        ax3.set_title('Kategori Satışları', fontweight='bold')
        ax3.tick_params(axis='x', rotation=45)

        ax4 = fig.add_subplot(gs[1, 1])
        self.df.boxplot(column='Satış', by='Mağaza_Bölgesi', ax=ax4)
        ax4.set_title('Bölge Box Plot', fontweight='bold')
        plt.sca(ax4)
        plt.xticks(rotation=45)

        ax5 = fig.add_subplot(gs[1, 2])
        ax5.scatter(self.df['Müşteri_Sayısı'], self.df['Satış'],
                   c=self.df['Kar'], s=50, alpha=0.6, cmap='viridis')
        ax5.set_title('Müşteri vs Satış', fontweight='bold')
        ax5.set_xlabel('Müşteri')
        ax5.set_ylabel('Satış')

        ax6 = fig.add_subplot(gs[2, :])
        pivot_data = self.df.pivot_table(values='Satış', index='Ürün_Kategorisi',
                                        columns='Mağaza_Bölgesi', aggfunc='sum')
        sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlGnBu', ax=ax6,
                   cbar_kws={'label': 'Satış'}, linewidths=1)
        ax6.set_title('Kategori x Bölge Heatmap', fontweight='bold')

        self.kaydet(fig, 'O01_dashboard')

    def tum_grafikler(self):
        """Tüm grafikleri oluştur"""
        print("\n🔄 Tüm 20 grafik oluşturuluyor...\n")

        grafikler = [
            ("T01 - Line Chart", self.line_chart),
            ("T02 - Bar Chart", self.bar_chart),
            ("T03 - Histogram", self.histogram),
            ("T04 - Scatter Plot", self.scatter_plot),
            ("T05 - Pie Chart", self.pie_chart),
            ("T06 - Box Plot", self.box_plot),
            ("I01 - Heatmap", self.heatmap),
            ("I02 - Violin Plot", self.violin_plot),
            ("I03 - 3D Scatter", self.scatter_3d),
            ("I04 - KDE Plot", self.kde_plot),
            ("I05 - Hexbin Plot", self.hexbin_plot),
            ("I06 - Waterfall", self.waterfall_chart),
            ("K01 - Stacked Bar", self.stacked_bar),
            ("K02 - Grouped Bar", self.grouped_bar),
            ("K03 - Area Chart", self.area_chart),
            ("K04 - Density Contour", self.density_contour),
            ("K05 - Correlation", self.correlation_matrix),
            ("K06 - Swarm Plot", self.swarm_plot),
            ("O01 - Dashboard", self.dashboard),
        ]

        for i, (isim, fonksiyon) in enumerate(grafikler, 1):
            try:
                print(f"[{i:2d}/19] {isim:30s}", end=" ", flush=True)
                fonksiyon()
            except Exception as e:
                print(f"❌ Hata: {str(e)[:40]}")

        print("\n" + "="*70)
        print("🎉 TÜM GRAFIKLER BAŞARIYLA OLUŞTURULDU!")
        print("="*70 + "\n")

    def yardim(self):
        """Kullanım kılavuzu"""
        print("\n" + "="*70)
        print("📊 İNTERAKTİF GRAFIK OLUŞTURUCU")
        print("="*70)
        print("\nKullanım: python3 interactive_charts.py [grafik_adi]\n")
        print("🎯 TEMEL GRAFİKLER (6):")
        print("  line_chart      - Zaman serisine göre trend")
        print("  bar_chart       - Kategori/bölge karşılaştırması")
        print("  histogram       - Değişken dağılımı")
        print("  scatter_plot    - İki değişken ilişkisi")
        print("  pie_chart       - Yüzdelik dağılım")
        print("  box_plot        - Dörtlü analiz")
        print("\n📈 İLERİ GRAFİKLER (6):")
        print("  heatmap         - Kategorik ilişkiler")
        print("  violin_plot     - Dağılım şekli")
        print("  scatter_3d      - Üç değişken analizi")
        print("  kde_plot        - Yoğunluk tahmini")
        print("  hexbin_plot     - 2D yoğunluk")
        print("  waterfall_chart - Satış/gider/kar akışı")
        print("\n🎨 KÖŞELİ GRAFİKLER (6):")
        print("  stacked_bar     - Yığılı çubuklar")
        print("  grouped_bar     - Gruplandırılmış çubuklar")
        print("  area_chart      - Alan grafiği")
        print("  density_contour - Yoğunluk konturları")
        print("  correlation_matrix - Korelasyon tablosu")
        print("  swarm_plot      - Veri noktaları çiçeği")
        print("\n📊 ÖZET GRAFİKLER (2):")
        print("  dashboard       - Hepsi bir arada")
        print("  all             - Tüm 19 grafik")
        print("\n" + "="*70)
        print("Örnekler:")
        print("  python3 interactive_charts.py line_chart")
        print("  python3 interactive_charts.py pie_chart")
        print("  python3 interactive_charts.py all")
        print("="*70 + "\n")

# Ana Kod
if __name__ == "__main__":
    olusturucu = GrafikOlusturucu()

    if len(sys.argv) == 1 or sys.argv[1] in ['-h', '--help']:
        olusturucu.yardim()
    elif sys.argv[1] == 'all':
        olusturucu.tum_grafikler()
    elif hasattr(olusturucu, sys.argv[1]):
        try:
            getattr(olusturucu, sys.argv[1])()
            print(f"\n✅ {sys.argv[1]} grafiği başarıyla oluşturuldu!")
        except Exception as e:
            print(f"\n❌ Hata oluştu: {e}")
    else:
        print(f"\n❌ Bilinmeyen grafik: {sys.argv[1]}")
        olusturucu.yardim()

