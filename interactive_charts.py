import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

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
        print("\n🔄 Tüm 25 grafik oluşturuluyor...\n")

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
            ("S01 - T-Test Analysis", self.t_test_analysis),
            ("S02 - ANOVA Analysis", self.anova_analysis),
            ("S03 - Regression Analysis", self.regression_analysis),
            ("S04 - Confidence Intervals", self.confidence_intervals),
            ("S05 - p-Value Heatmap", self.p_value_heatmap),
            ("S06 - Statistical Comparison", self.statistical_comparison),
            ("O01 - Dashboard", self.dashboard),
        ]

        for i, (isim, fonksiyon) in enumerate(grafikler, 1):
            try:
                print(f"[{i:2d}/25] {isim:30s}", end=" ", flush=True)
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
        print("\n📊 İSTATİSTİKSEL GRAFİKLER (6):")
        print("  t_test_analysis - T-test karşılaştırmaları")
        print("  anova_analysis  - ANOVA çoklu karşılaştırma")
        print("  regression_analysis - Regresyon analizi")
        print("  confidence_intervals - Güven aralıkları")
        print("  p_value_heatmap - p-value ısı haritası")
        print("  statistical_comparison - İstatistiksel karşılaştırma")
        print("\n📊 ÖZET GRAFİKLER (2):")
        print("  dashboard       - Hepsi bir arada")
        print("  all             - Tüm 25 grafik")
        print("\n" + "="*70)
        print("Örnekler:")
        print("  python3 interactive_charts.py line_chart")
        print("  python3 interactive_charts.py t_test_analysis")
        print("  python3 interactive_charts.py all")
        print("="*70 + "\n")

    # ============ İSTATİSTİKSEL GRAFİKLER (6) ============
    def t_test_analysis(self):
        """T-test analizi - İki grup karşılaştırması"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('T-Test Analizleri - İstatistiksel Anlamlılık', fontsize=16, fontweight='bold')

        # Bölgelere göre satış karşılaştırması
        istanbul = self.df[self.df['Mağaza_Bölgesi'] == 'İstanbul']['Satış']
        ankara = self.df[self.df['Mağaza_Bölgesi'] == 'Ankara']['Satış']

        t_stat, p_value = stats.ttest_ind(istanbul, ankara)

        # Box plot
        axes[0, 0].boxplot([istanbul, ankara], labels=['İstanbul', 'Ankara'])
        axes[0, 0].set_title(f'İstanbul vs Ankara Satış Karşılaştırması\np-value: {p_value:.4f}')
        axes[0, 0].set_ylabel('Satış')
        if p_value < 0.05:
            axes[0, 0].text(1.5, max(istanbul.max(), ankara.max()) * 0.9,
                           '*** İstatistiksel Olarak Anlamlı ***',
                           ha='center', va='center', fontsize=10,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7))

        # Histogram karşılaştırması
        axes[0, 1].hist(istanbul, alpha=0.7, label='İstanbul', bins=15, color='#3498db')
        axes[0, 1].hist(ankara, alpha=0.7, label='Ankara', bins=15, color='#e74c3c')
        axes[0, 1].set_title('Dağılım Karşılaştırması')
        axes[0, 1].legend()
        axes[0, 1].set_xlabel('Satış')
        axes[0, 1].set_ylabel('Frekans')

        # Kategorilere göre satış karşılaştırması
        elektronik = self.df[self.df['Ürün_Kategorisi'] == 'Elektronik']['Satış']
        giyim = self.df[self.df['Ürün_Kategorisi'] == 'Giyim']['Satış']

        t_stat2, p_value2 = stats.ttest_ind(elektronik, giyim)

        axes[1, 0].boxplot([elektronik, giyim], labels=['Elektronik', 'Giyim'])
        axes[1, 0].set_title(f'Elektronik vs Giyim Satış Karşılaştırması\np-value: {p_value2:.4f}')
        axes[1, 0].set_ylabel('Satış')
        if p_value2 < 0.05:
            axes[1, 0].text(1.5, max(elektronik.max(), giyim.max()) * 0.9,
                           '*** İstatistiksel Olarak Anlamlı ***',
                           ha='center', va='center', fontsize=10,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7))

        # İstatistik özeti
        axes[1, 1].axis('off')
        summary_text = f"""
        İSTATİSTİKSEL ANALİZ SONUÇLARI
        
        İstanbul vs Ankara:
        • t-değeri: {t_stat:.3f}
        • p-değeri: {p_value:.4f}
        • Anlamlılık: {'Evet' if p_value < 0.05 else 'Hayır'}
        
        Elektronik vs Giyim:
        • t-değeri: {t_stat2:.3f}
        • p-değeri: {p_value2:.4f}
        • Anlamlılık: {'Evet' if p_value2 < 0.05 else 'Hayır'}
        
        Not: p < 0.05 ise gruplar arası
        fark istatistiksel olarak anlamlıdır.
        """
        axes[1, 1].text(0.1, 0.8, summary_text, transform=axes[1, 1].transAxes,
                       fontsize=10, verticalalignment='top', fontfamily='monospace')

        plt.tight_layout()
        self.kaydet(fig, 'S01_t_test_analysis')

    def anova_analysis(self):
        """ANOVA analizi - Çoklu grup karşılaştırması"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('ANOVA Analizi - Bölgeler Arası Karşılaştırma', fontsize=16, fontweight='bold')

        # Bölgelere göre satış ANOVA
        bolge_gruplari = [self.df[self.df['Mağaza_Bölgesi'] == bolge]['Satış']
                         for bolge in self.df['Mağaza_Bölgesi'].unique()]

        f_stat, p_value = stats.f_oneway(*bolge_gruplari)

        # Box plot
        axes[0, 0].boxplot(bolge_gruplari, labels=self.df['Mağaza_Bölgesi'].unique())
        axes[0, 0].set_title(f'Bölgelere Göre Satış ANOVA\nF={f_stat:.3f}, p={p_value:.4f}')
        axes[0, 0].set_ylabel('Satış')
        if p_value < 0.05:
            axes[0, 0].text(2, self.df['Satış'].max() * 0.9,
                           '*** İstatistiksel Olarak Anlamlı Fark ***',
                           ha='center', va='center', fontsize=10,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7))

        # Tukey HSD post-hoc analizi
        tukey = pairwise_tukeyhsd(self.df['Satış'], self.df['Mağaza_Bölgesi'])

        # Tukey sonuçlarını görselleştir
        axes[0, 1].axis('off')
        tukey_text = "TUKEY HSD POST-HOC ANALİZİ\n\n"
        tukey_text += str(tukey)
        axes[0, 1].text(0.05, 0.95, tukey_text, transform=axes[0, 1].transAxes,
                       fontsize=8, verticalalignment='top', fontfamily='monospace',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))

        # Kategorilere göre satış ANOVA
        kategori_gruplari = [self.df[self.df['Ürün_Kategorisi'] == kat]['Satış']
                           for kat in self.df['Ürün_Kategorisi'].unique()]

        f_stat2, p_value2 = stats.f_oneway(*kategori_gruplari)

        axes[1, 0].boxplot(kategori_gruplari, labels=self.df['Ürün_Kategorisi'].unique())
        axes[1, 0].set_title(f'Kategorilere Göre Satış ANOVA\nF={f_stat2:.3f}, p={p_value2:.4f}')
        axes[1, 0].set_ylabel('Satış')
        if p_value2 < 0.05:
            axes[1, 0].text(2, self.df['Satış'].max() * 0.9,
                           '*** İstatistiksel Olarak Anlamlı Fark ***',
                           ha='center', va='center', fontsize=10,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7))

        # İstatistik özeti
        axes[1, 1].axis('off')
        summary_text = f"""
        ANOVA ANALİZ SONUÇLARI
        
        Bölgeler Arası:
        • F-değeri: {f_stat:.3f}
        • p-değeri: {p_value:.4f}
        • Anlamlılık: {'Evet' if p_value < 0.05 else 'Hayır'}
        
        Kategoriler Arası:
        • F-değeri: {f_stat2:.3f}
        • p-değeri: {p_value2:.4f}
        • Anlamlılık: {'Evet' if p_value2 < 0.05 else 'Hayır'}
        
        Not: p < 0.05 ise gruplar arası
        en az bir fark istatistiksel olarak
        anlamlıdır.
        """
        axes[1, 1].text(0.1, 0.8, summary_text, transform=axes[1, 1].transAxes,
                       fontsize=10, verticalalignment='top', fontfamily='monospace')

        plt.tight_layout()
        self.kaydet(fig, 'S02_anova_analysis')

    def regression_analysis(self):
        """Regresyon analizi - İlişki ve tahmin"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Regresyon Analizi - Değişkenler Arası İlişkiler', fontsize=16, fontweight='bold')

        # Müşteri sayısı vs Satış regresyonu
        X = self.df['Müşteri_Sayısı']
        y = self.df['Satış']

        # Regresyon modeli
        X_with_const = sm.add_constant(X)
        model = sm.OLS(y, X_with_const).fit()

        # Scatter plot ve regresyon çizgisi
        axes[0, 0].scatter(X, y, alpha=0.6, color='#3498db', edgecolors='black')
        axes[0, 0].plot(X, model.predict(X_with_const), color='#e74c3c', linewidth=3,
                       label=f'y = {model.params[1]:.2f}x + {model.params[0]:.2f}')
        axes[0, 0].set_title(f'Müşteri Sayısı vs Satış Regresyonu\nR² = {model.rsquared:.3f}, p = {model.f_pvalue:.4f}')
        axes[0, 0].set_xlabel('Müşteri Sayısı')
        axes[0, 0].set_ylabel('Satış')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        # Güven aralıkları
        pred = model.get_prediction(X_with_const)
        pred_df = pred.summary_frame()
        axes[0, 0].fill_between(X, pred_df['mean_ci_lower'], pred_df['mean_ci_upper'],
                               color='#e74c3c', alpha=0.2, label='95% Güven Aralığı')

        # Residual plot
        residuals = model.resid
        axes[0, 1].scatter(model.fittedvalues, residuals, alpha=0.6, color='#9b59b6', edgecolors='black')
        axes[0, 1].axhline(y=0, color='red', linestyle='--', linewidth=2)
        axes[0, 1].set_title('Residual Plot (Artık Değerler)')
        axes[0, 1].set_xlabel('Tahmin Edilen Değerler')
        axes[0, 1].set_ylabel('Artık Değerler')
        axes[0, 1].grid(True, alpha=0.3)

        # Q-Q plot
        sm.qqplot(residuals, line='45', ax=axes[1, 0])
        axes[1, 0].set_title('Q-Q Plot (Normalite Testi)')

        # Regresyon istatistikleri
        axes[1, 1].axis('off')
        stats_text = f"""
        REGRESYON ANALİZİ SONUÇLARI
        
        Model: Satış = β₀ + β₁×Müşteri_Sayısı
        
        Katsayılar:
        • β₀ (Sabit): {model.params[0]:.2f}
        • β₁ (Eğim): {model.params[1]:.2f}
        
        Model Kalitesi:
        • R² (Açıklanan Varyans): {model.rsquared:.3f}
        • Düzeltilmiş R²: {model.rsquared_adj:.3f}
        • F-istatistiği: {model.fvalue:.2f}
        • p-değeri: {model.f_pvalue:.4f}
        
        Katsayı Testleri:
        • Sabit p-değeri: {model.pvalues[0]:.4f}
        • Eğim p-değeri: {model.pvalues[1]:.4f}
        
        Not: p < 0.05 ise katsayılar
        istatistiksel olarak anlamlıdır.
        """
        axes[1, 1].text(0.05, 0.95, stats_text, transform=axes[1, 1].transAxes,
                       fontsize=9, verticalalignment='top', fontfamily='monospace',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))

        plt.tight_layout()
        self.kaydet(fig, 'S03_regression_analysis')

    def confidence_intervals(self):
        """Güven aralıkları - Tahmin belirsizliği"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Güven Aralıkları ve Tahmin Belirsizliği', fontsize=16, fontweight='bold')

        # Bölgelere göre ortalama satış ve güven aralıkları
        bolge_stats = self.df.groupby('Mağaza_Bölgesi')['Satış'].agg(['mean', 'std', 'count'])
        bolge_stats['se'] = bolge_stats['std'] / np.sqrt(bolge_stats['count'])
        bolge_stats['ci_lower'] = bolge_stats['mean'] - 1.96 * bolge_stats['se']
        bolge_stats['ci_upper'] = bolge_stats['mean'] + 1.96 * bolge_stats['se']

        # Güven aralıkları bar plot
        x_pos = np.arange(len(bolge_stats.index))
        axes[0, 0].bar(x_pos, bolge_stats['mean'], yerr=1.96*bolge_stats['se'],
                      capsize=5, color='#3498db', edgecolor='black', alpha=0.7)
        axes[0, 0].set_title('Bölgelere Göre Satış Ortalamaları\n(95% Güven Aralıkları)')
        axes[0, 0].set_xticks(x_pos)
        axes[0, 0].set_xticklabels(bolge_stats.index)
        axes[0, 0].set_ylabel('Satış Ortalaması')
        axes[0, 0].grid(True, alpha=0.3, axis='y')

        # Kategorilere göre güven aralıkları
        kat_stats = self.df.groupby('Ürün_Kategorisi')['Satış'].agg(['mean', 'std', 'count'])
        kat_stats['se'] = kat_stats['std'] / np.sqrt(kat_stats['count'])
        kat_stats['ci_lower'] = kat_stats['mean'] - 1.96 * kat_stats['se']
        kat_stats['ci_upper'] = kat_stats['mean'] + 1.96 * kat_stats['se']

        x_pos2 = np.arange(len(kat_stats.index))
        axes[0, 1].bar(x_pos2, kat_stats['mean'], yerr=1.96*kat_stats['se'],
                      capsize=5, color='#e74c3c', edgecolor='black', alpha=0.7)
        axes[0, 1].set_title('Kategorilere Göre Satış Ortalamaları\n(95% Güven Aralıkları)')
        axes[0, 1].set_xticks(x_pos2)
        axes[0, 1].set_xticklabels(kat_stats.index, rotation=45)
        axes[0, 1].set_ylabel('Satış Ortalaması')
        axes[0, 1].grid(True, alpha=0.3, axis='y')

        # Bootstrap güven aralıkları örneği
        np.random.seed(42)
        bootstrap_means = []
        for _ in range(1000):
            sample = np.random.choice(self.df['Satış'], size=len(self.df), replace=True)
            bootstrap_means.append(np.mean(sample))

        bootstrap_ci = np.percentile(bootstrap_means, [2.5, 97.5])
        observed_mean = np.mean(self.df['Satış'])

        axes[1, 0].hist(bootstrap_means, bins=30, alpha=0.7, color='#9b59b6', edgecolor='black')
        axes[1, 0].axvline(observed_mean, color='red', linewidth=2, label=f'Gözlenen: {observed_mean:.0f}')
        axes[1, 0].axvline(bootstrap_ci[0], color='green', linestyle='--', linewidth=2,
                          label=f'CI Alt: {bootstrap_ci[0]:.0f}')
        axes[1, 0].axvline(bootstrap_ci[1], color='green', linestyle='--', linewidth=2,
                          label=f'CI Üst: {bootstrap_ci[1]:.0f}')
        axes[1, 0].set_title('Bootstrap Güven Aralıkları - Genel Satış Ortalaması')
        axes[1, 0].set_xlabel('Bootstrap Ortalamaları')
        axes[1, 0].set_ylabel('Frekans')
        axes[1, 0].legend()

        # Güven aralıkları karşılaştırması
        axes[1, 1].axis('off')
        ci_text = f"""
        GÜVEN ARALIKLARI ANALİZİ
        
        Bölge Bazlı Güven Aralıkları:
        {bolge_stats[['mean', 'ci_lower', 'ci_upper']].round(0).to_string()}
        
        Kategori Bazlı Güven Aralıkları:
        {kat_stats[['mean', 'ci_lower', 'ci_upper']].round(0).to_string()}
        
        Bootstrap CI (Genel Ortalama):
        • Gözlenen: {observed_mean:.0f}
        • 95% CI: [{bootstrap_ci[0]:.0f}, {bootstrap_ci[1]:.0f}]
        
        Not: Güven aralıkları tahmin
        belirsizliğini gösterir. Aralıklar
        çakışmıyorsa gruplar arası fark
        istatistiksel olarak anlamlıdır.
        """
        axes[1, 1].text(0.05, 0.95, ci_text, transform=axes[1, 1].transAxes,
                       fontsize=8, verticalalignment='top', fontfamily='monospace',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))

        plt.tight_layout()
        self.kaydet(fig, 'S04_confidence_intervals')

    def p_value_heatmap(self):
        """p-value ısı haritası - Çoklu karşılaştırmalar"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('p-Value Isı Haritası - İstatistiksel Anlamlılık Matrisi', fontsize=16, fontweight='bold')

        # Bölgeler arası p-value matrisi
        bolgeler = self.df['Mağaza_Bölgesi'].unique()
        p_matrix = np.zeros((len(bolgeler), len(bolgeler)))

        for i, bolge1 in enumerate(bolgeler):
            for j, bolge2 in enumerate(bolgeler):
                if i != j:
                    data1 = self.df[self.df['Mağaza_Bölgesi'] == bolge1]['Satış']
                    data2 = self.df[self.df['Mağaza_Bölgesi'] == bolge2]['Satış']
                    _, p_value = stats.ttest_ind(data1, data2)
                    p_matrix[i, j] = p_value
                else:
                    p_matrix[i, j] = 1.0  # Kendi kendine karşılaştırma

        # p-value ısı haritası
        im1 = axes[0, 0].imshow(p_matrix, cmap='RdYlGn_r', vmin=0, vmax=0.1)
        axes[0, 0].set_xticks(range(len(bolgeler)))
        axes[0, 0].set_yticks(range(len(bolgeler)))
        axes[0, 0].set_xticklabels(bolgeler, rotation=45)
        axes[0, 0].set_yticklabels(bolgeler)
        axes[0, 0].set_title('Bölgeler Arası p-Value Matrisi')

        # p-value'ları yaz
        for i in range(len(bolgeler)):
            for j in range(len(bolgeler)):
                if i != j:
                    color = 'white' if p_matrix[i, j] < 0.05 else 'black'
                    axes[0, 0].text(j, i, f'{p_matrix[i, j]:.3f}', ha='center', va='center',
                                   color=color, fontweight='bold', fontsize=8)

        plt.colorbar(im1, ax=axes[0, 0], label='p-Value')

        # Kategoriler arası p-value matrisi
        kategoriler = self.df['Ürün_Kategorisi'].unique()
        p_matrix2 = np.zeros((len(kategoriler), len(kategoriler)))

        for i, kat1 in enumerate(kategoriler):
            for j, kat2 in enumerate(kategoriler):
                if i != j:
                    data1 = self.df[self.df['Ürün_Kategorisi'] == kat1]['Satış']
                    data2 = self.df[self.df['Ürün_Kategorisi'] == kat2]['Satış']
                    _, p_value = stats.ttest_ind(data1, data2)
                    p_matrix2[i, j] = p_value
                else:
                    p_matrix2[i, j] = 1.0

        im2 = axes[0, 1].imshow(p_matrix2, cmap='RdYlGn_r', vmin=0, vmax=0.1)
        axes[0, 1].set_xticks(range(len(kategoriler)))
        axes[0, 1].set_yticks(range(len(kategoriler)))
        axes[0, 1].set_xticklabels(kategoriler, rotation=45)
        axes[0, 1].set_yticklabels(kategoriler)
        axes[0, 1].set_title('Kategoriler Arası p-Value Matrisi')

        for i in range(len(kategoriler)):
            for j in range(len(kategoriler)):
                if i != j:
                    color = 'white' if p_matrix2[i, j] < 0.05 else 'black'
                    axes[0, 1].text(j, i, f'{p_matrix2[i, j]:.3f}', ha='center', va='center',
                                   color=color, fontweight='bold', fontsize=8)

        plt.colorbar(im2, ax=axes[0, 1], label='p-Value')

        # Anlamlılık seviyeleri gösterimi
        axes[1, 0].axis('off')
        significance_text = """
        p-VALUE ANLAMLILIK SEVIYELERİ
        
        🔴 p < 0.001 : Çok Yüksek Anlamlılık
        🟠 p < 0.01  : Yüksek Anlamlılık  
        🟡 p < 0.05  : Orta Anlamlılık
        🟢 p ≥ 0.05  : Anlamlı Değil
        
        Isı Haritası Renk Kodu:
        • Kırmızı (p ≈ 0): Çok Anlamlı Fark
        • Sarı (p ≈ 0.05): Sınırda Anlamlılık
        • Yeşil (p > 0.05): Anlamlı Fark Yok
        
        Matris Açıklaması:
        • Köşegen: Her zaman 1.0 (kendi kendine)
        • Diğer hücreler: Grup karşılaştırmaları
        • p < 0.05 ise gruplar farklıdır
        """
        axes[1, 0].text(0.05, 0.95, significance_text, transform=axes[1, 0].transAxes,
                       fontsize=10, verticalalignment='top', fontfamily='monospace',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcyan', alpha=0.8))

        # İstatistiksel test özeti
        axes[1, 1].axis('off')
        summary_text = f"""
        İSTATİSTİKSEL TEST ÖZETİ
        
        Bölgeler Arası Karşılaştırmalar:
        • Toplam Test: {len(bolgeler)*(len(bolgeler)-1)//2}
        • Anlamlı Fark: {np.sum(p_matrix < 0.05) - len(bolgeler)} adet
        • Anlamlılık Oranı: {(np.sum(p_matrix < 0.05) - len(bolgeler))/(len(bolgeler)*(len(bolgeler)-1)//2)*100:.1f}%
        
        Kategoriler Arası Karşılaştırmalar:
        • Toplam Test: {len(kategoriler)*(len(kategoriler)-1)//2}
        • Anlamlı Fark: {np.sum(p_matrix2 < 0.05) - len(kategoriler)} adet
        • Anlamlılık Oranı: {(np.sum(p_matrix2 < 0.05) - len(kategoriler))/(len(kategoriler)*(len(kategoriler)-1)//2)*100:.1f}%
        
        Not: Çoklu karşılaştırmalarda
        Type I hata riski artar.
        Bonferroni düzeltmesi önerilir.
        """
        axes[1, 1].text(0.05, 0.95, summary_text, transform=axes[1, 1].transAxes,
                       fontsize=9, verticalalignment='top', fontfamily='monospace',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightpink', alpha=0.8))

        plt.tight_layout()
        self.kaydet(fig, 'S05_p_value_heatmap')

    def statistical_significance_demo(self):
        """İstatistiksel anlamlılık demo grafiği"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('📊 İstatistiksel Anlamlılık Gösterimi', fontsize=16, fontweight='bold')

        # T-Test örneği
        istanbul = self.df[self.df['Mağaza_Bölgesi'] == 'İstanbul']['Satış']
        ankara = self.df[self.df['Mağaza_Bölgesi'] == 'Ankara']['Satış']

        from scipy import stats
        t_stat, p_value = stats.ttest_ind(istanbul, ankara)

        # Box plot
        axes[0, 0].boxplot([istanbul, ankara], labels=['İstanbul', 'Ankara'])
        axes[0, 0].set_title(f'T-Test Karşılaştırması\np-value: {p_value:.4f}')
        axes[0, 0].set_ylabel('Satış')

        if p_value < 0.05:
            axes[0, 0].text(1.5, max(istanbul.max(), ankara.max()) * 0.9,
                           '*** İstatistiksel Olarak Anlamlı ***',
                           ha='center', va='center', fontsize=10,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7))

        # Güven aralıkları
        bolge_stats = self.df.groupby('Mağaza_Bölgesi')['Satış'].agg(['mean', 'std', 'count'])
        bolge_stats['se'] = bolge_stats['std'] / np.sqrt(bolge_stats['count'])
        bolge_stats['ci_lower'] = bolge_stats['mean'] - 1.96 * bolge_stats['se']
        bolge_stats['ci_upper'] = bolge_stats['mean'] + 1.96 * bolge_stats['se']

        x_pos = np.arange(len(bolge_stats.index))
        axes[0, 1].bar(x_pos, bolge_stats['mean'], yerr=1.96*bolge_stats['se'],
                      capsize=5, color='#3498db', edgecolor='black', alpha=0.7)
        axes[0, 1].set_title('Güven Aralıkları (95% CI)')
        axes[0, 1].set_xticks(x_pos)
        axes[0, 1].set_xticklabels(bolge_stats.index)
        axes[0, 1].set_ylabel('Satış Ortalaması')

        # p-value ısı haritası
        bolgeler = self.df['Mağaza_Bölgesi'].unique()
        p_matrix = np.zeros((len(bolgeler), len(bolgeler)))

        for i, bolge1 in enumerate(bolgeler):
            for j, bolge2 in enumerate(bolgeler):
                if i != j:
                    data1 = self.df[self.df['Mağaza_Bölgesi'] == bolge1]['Satış']
                    data2 = self.df[self.df['Mağaza_Bölgesi'] == bolge2]['Satış']
                    _, p_val = stats.ttest_ind(data1, data2)
                    p_matrix[i, j] = p_val
                else:
                    p_matrix[i, j] = 1.0

        im = axes[1, 0].imshow(p_matrix, cmap='RdYlGn_r', vmin=0, vmax=0.1)
        axes[1, 0].set_xticks(range(len(bolgeler)))
        axes[1, 0].set_yticks(range(len(bolgeler)))
        axes[1, 0].set_xticklabels(bolgeler, rotation=45)
        axes[1, 0].set_yticklabels(bolgeler)
        axes[1, 0].set_title('p-Value Isı Haritası')

        # p-value'ları yaz
        for i in range(len(bolgeler)):
            for j in range(len(bolgeler)):
                if i != j:
                    color = 'white' if p_matrix[i, j] < 0.05 else 'black'
                    axes[1, 0].text(j, i, f'{p_matrix[i, j]:.3f}', ha='center', va='center',
                                   color=color, fontweight='bold', fontsize=8)

        plt.colorbar(im, ax=axes[1, 0], label='p-Value')

        # İstatistik özeti
        axes[1, 1].axis('off')
        summary_text = f"""
        İSTATİSTİKSEL ANALİZ ÖZETİ
        
        📈 T-Test Sonucu:
        • t-değeri: {t_stat:.3f}
        • p-değeri: {p_value:.4f}
        • Anlamlılık: {'Evet (p<0.05)' if p_value < 0.05 else 'Hayır (p≥0.05)'}
        
        🎯 Güven Aralıkları:
        • 95% CI kullanıldı
        • Çakışmayan aralıklar = anlamlı fark
        
        🔥 p-Value Isı Haritası:
        • Kırmızı: p < 0.05 (anlamlı)
        • Yeşil: p ≥ 0.05 (anlamlı değil)
        
        💡 İpuçları:
        • p < 0.05: İstatistiksel anlamlılık
        • Güven aralıkları çakışmazsa: Fark var
        • Effect size: Pratik önem derecesi
        """
        axes[1, 1].text(0.05, 0.95, summary_text, transform=axes[1, 1].transAxes,
                       fontsize=9, verticalalignment='top', fontfamily='monospace',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))

        plt.tight_layout()
        self.kaydet(fig, 'S01_statistical_significance_demo')

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

