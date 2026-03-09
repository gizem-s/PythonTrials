import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec
from scipy import stats

# Stil ve font ayarları
sns.set_style("darkgrid")
plt.rcParams['figure.facecolor'] = '#f8f9fa'

# CSV dosyasını oku
df = pd.read_csv('sales_data.csv')

# ============ GRAFIK 1: Heatmap ============
fig1, ax1 = plt.subplots(figsize=(12, 8))

# Pivot table oluştur
pivot_data = df.pivot_table(
    values='Satış',
    index='Ürün_Kategorisi',
    columns='Mağaza_Bölgesi',
    aggfunc='sum'
)

# Heatmap çiz
sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlGnBu',
            cbar_kws={'label': 'Satış (₺)'}, linewidths=1, ax=ax1)
ax1.set_title('Ürün Kategorisine Göre Bölge Satış Heatmap', fontsize=14, fontweight='bold', pad=20)
ax1.set_xlabel('Mağaza Bölgesi', fontweight='bold')
ax1.set_ylabel('Ürün Kategorisi', fontweight='bold')
plt.tight_layout()
plt.savefig('charts/01_heatmap.png', dpi=300, bbox_inches='tight')
print("✅ Heatmap oluşturuldu: charts/01_heatmap.png")
plt.close()

# ============ GRAFIK 2: Violin Plot ============
fig2, ax2 = plt.subplots(figsize=(12, 7))

sns.violinplot(data=df, x='Mağaza_Bölgesi', y='Satış', palette='Set2', ax=ax2)
sns.stripplot(data=df, x='Mağaza_Bölgesi', y='Satış',
              color='black', alpha=0.3, size=4, ax=ax2)

ax2.set_title('Bölgelere Göre Satış Dağılımı (Violin Plot)', fontsize=14, fontweight='bold', pad=20)
ax2.set_xlabel('Mağaza Bölgesi', fontweight='bold')
ax2.set_ylabel('Satış (₺)', fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('charts/02_violin_plot.png', dpi=300, bbox_inches='tight')
print("✅ Violin Plot oluşturuldu: charts/02_violin_plot.png")
plt.close()

# ============ GRAFIK 3: 3D Scatter Plot ============
from mpl_toolkits.mplot3d import Axes3D

fig3 = plt.figure(figsize=(12, 8))
ax3 = fig3.add_subplot(111, projection='3d')

# Kategorilere göre renkler
colors = {'Elektronik': '#e74c3c', 'Giyim': '#3498db', 'Yiyecek': '#2ecc71', 'Kitap': '#f39c12'}
for kategori in df['Ürün_Kategorisi'].unique():
    mask = df['Ürün_Kategorisi'] == kategori
    ax3.scatter(df[mask]['Müşteri_Sayısı'],
               df[mask]['Gider'],
               df[mask]['Satış'],
               c=colors.get(kategori, '#95a5a6'),
               label=kategori,
               s=100,
               alpha=0.6,
               edgecolors='black',
               linewidth=0.5)

ax3.set_xlabel('Müşteri Sayısı', fontweight='bold')
ax3.set_ylabel('Gider (₺)', fontweight='bold')
ax3.set_zlabel('Satış (₺)', fontweight='bold')
ax3.set_title('3D Satış Analizi: Müşteri, Gider ve Satış', fontsize=14, fontweight='bold', pad=20)
ax3.legend(loc='upper left')
plt.tight_layout()
plt.savefig('charts/03_3d_scatter.png', dpi=300, bbox_inches='tight')
print("✅ 3D Scatter Plot oluşturuldu: charts/03_3d_scatter.png")
plt.close()

# ============ GRAFIK 4: KDE Plot (Kernel Density Estimation) ============
fig4, axes4 = plt.subplots(2, 2, figsize=(14, 10))
fig4.suptitle('Değişkenlerin Yoğunluk Dağılımı (KDE)', fontsize=16, fontweight='bold', y=1.00)

# Satış KDE
axes4[0, 0].hist(df['Satış'], bins=20, alpha=0.5, color='#3498db', edgecolor='black')
df['Satış'].plot(kind='kde', ax=axes4[0, 0], color='#e74c3c', linewidth=2, secondary_y=False)
axes4[0, 0].set_title('Satış Dağılımı', fontweight='bold')
axes4[0, 0].set_ylabel('Frekans')

# Gider KDE
axes4[0, 1].hist(df['Gider'], bins=20, alpha=0.5, color='#2ecc71', edgecolor='black')
df['Gider'].plot(kind='kde', ax=axes4[0, 1], color='#e74c3c', linewidth=2, secondary_y=False)
axes4[0, 1].set_title('Gider Dağılımı', fontweight='bold')
axes4[0, 1].set_ylabel('Frekans')

# Müşteri Sayısı KDE
axes4[1, 0].hist(df['Müşteri_Sayısı'], bins=20, alpha=0.5, color='#f39c12', edgecolor='black')
df['Müşteri_Sayısı'].plot(kind='kde', ax=axes4[1, 0], color='#e74c3c', linewidth=2, secondary_y=False)
axes4[1, 0].set_title('Müşteri Sayısı Dağılımı', fontweight='bold')
axes4[1, 0].set_ylabel('Frekans')

# Kar (Satış - Gider) KDE
df['Kar'] = df['Satış'] - df['Gider']
axes4[1, 1].hist(df['Kar'], bins=20, alpha=0.5, color='#9b59b6', edgecolor='black')
df['Kar'].plot(kind='kde', ax=axes4[1, 1], color='#e74c3c', linewidth=2, secondary_y=False)
axes4[1, 1].set_title('Kar Dağılımı', fontweight='bold')
axes4[1, 1].set_ylabel('Frekans')

plt.tight_layout()
plt.savefig('charts/04_kde_distributions.png', dpi=300, bbox_inches='tight')
print("✅ KDE Distributions oluşturuldu: charts/04_kde_distributions.png")
plt.close()

# ============ GRAFIK 5: Correlation Heatmap ============
fig5, ax5 = plt.subplots(figsize=(10, 8))

# Sayısal sütunları seç
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlation_matrix = df[numeric_cols].corr()

# Heatmap çiz
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, linewidths=2, cbar_kws={'label': 'Korelasyon'},
            vmin=-1, vmax=1, ax=ax5)
ax5.set_title('Sayısal Değişkenler Arasında Korelasyon', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('charts/05_correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("✅ Correlation Heatmap oluşturuldu: charts/05_correlation_heatmap.png")
plt.close()

# ============ GRAFIK 6: Stacked Bar Chart ============
fig6, ax6 = plt.subplots(figsize=(12, 7))

# Bölge ve kategori göre satış pivot
stacked_data = df.pivot_table(
    values='Satış',
    index='Mağaza_Bölgesi',
    columns='Ürün_Kategorisi',
    aggfunc='sum'
)

stacked_data.plot(kind='bar', stacked=True, ax=ax6,
                  color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'],
                  edgecolor='black', linewidth=1.5)
ax6.set_title('Bölgelere Göre Kategori Satışları (Stacked)', fontsize=14, fontweight='bold', pad=20)
ax6.set_xlabel('Mağaza Bölgesi', fontweight='bold')
ax6.set_ylabel('Satış (₺)', fontweight='bold')
ax6.legend(title='Ürün Kategorisi', bbox_to_anchor=(1.05, 1), loc='upper left')
ax6.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('charts/06_stacked_bar.png', dpi=300, bbox_inches='tight')
print("✅ Stacked Bar Chart oluşturuldu: charts/06_stacked_bar.png")
plt.close()

# ============ GRAFIK 7: Sunburst-like Multi-level Pie ============
fig7, axes7 = plt.subplots(1, 2, figsize=(16, 7))
fig7.suptitle('Multi-Level Analiz', fontsize=16, fontweight='bold')

# Bölge dağılımı
bolge_data = df.groupby('Mağaza_Bölgesi')['Satış'].sum()
colors1 = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
wedges1, texts1, autotexts1 = axes7[0].pie(bolge_data.values, labels=bolge_data.index,
                                            autopct='%1.1f%%', colors=colors1, startangle=90)
axes7[0].set_title('Bölgelere Göre Satış Dağılımı', fontweight='bold', fontsize=12)
for autotext in autotexts1:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

# Kategori dağılımı
kategori_data = df.groupby('Ürün_Kategorisi')['Satış'].sum()
colors2 = ['#9b59b6', '#1abc9c', '#e67e22', '#34495e']
wedges2, texts2, autotexts2 = axes7[1].pie(kategori_data.values, labels=kategori_data.index,
                                            autopct='%1.1f%%', colors=colors2, startangle=90)
axes7[1].set_title('Ürün Kategorisine Göre Satış Dağılımı', fontweight='bold', fontsize=12)
for autotext in autotexts2:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

plt.tight_layout()
plt.savefig('charts/07_multi_pie.png', dpi=300, bbox_inches='tight')
print("✅ Multi-Level Pie Charts oluşturuldu: charts/07_multi_pie.png")
plt.close()

# ============ GRAFIK 8: Hexbin Plot ============
fig8, ax8 = plt.subplots(figsize=(12, 8))

hexbin = ax8.hexbin(df['Müşteri_Sayısı'], df['Satış'], gridsize=15, cmap='YlOrRd', mincnt=1)
ax8.set_xlabel('Müşteri Sayısı', fontweight='bold')
ax8.set_ylabel('Satış (₺)', fontweight='bold')
ax8.set_title('Müşteri Sayısı vs Satış (Hexbin Yoğunluk)', fontsize=14, fontweight='bold', pad=20)
plt.colorbar(hexbin, ax=ax8, label='Frekans')
plt.tight_layout()
plt.savefig('charts/08_hexbin.png', dpi=300, bbox_inches='tight')
print("✅ Hexbin Plot oluşturuldu: charts/08_hexbin.png")
plt.close()

# ============ GRAFIK 9: Grouped Bar Chart ============
fig9, ax9 = plt.subplots(figsize=(14, 7))

# Bölge ve kategori göre ortalama satış
grouped_data = df.groupby(['Mağaza_Bölgesi', 'Ürün_Kategorisi'])['Satış'].mean().unstack()

x = np.arange(len(grouped_data.index))
width = 0.2
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']

for i, col in enumerate(grouped_data.columns):
    offset = (i - 1.5) * width
    ax9.bar(x + offset, grouped_data[col], width, label=col, color=colors[i], edgecolor='black')

ax9.set_xlabel('Mağaza Bölgesi', fontweight='bold')
ax9.set_ylabel('Ortalama Satış (₺)', fontweight='bold')
ax9.set_title('Bölgelere Göre Kategori Başına Ortalama Satış', fontsize=14, fontweight='bold', pad=20)
ax9.set_xticks(x)
ax9.set_xticklabels(grouped_data.index)
ax9.legend(title='Ürün Kategorisi')
ax9.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('charts/09_grouped_bar.png', dpi=300, bbox_inches='tight')
print("✅ Grouped Bar Chart oluşturuldu: charts/09_grouped_bar.png")
plt.close()

# ============ GRAFIK 10: Waterfall Chart ============
fig10, ax10 = plt.subplots(figsize=(12, 7))

# Bölgelere göre toplam satış ve kar
bolge_satış = df.groupby('Mağaza_Bölgesi').agg({'Satış': 'sum', 'Gider': 'sum'})
bolge_satış['Kar'] = bolge_satış['Satış'] - bolge_satış['Gider']

# Waterfall chart benzer görselleştirme
x_pos = np.arange(len(bolge_satış.index))
ax10.bar(x_pos, bolge_satış['Satış'], label='Satış', color='#2ecc71', edgecolor='black', linewidth=1.5)
ax10.bar(x_pos, bolge_satış['Gider'], bottom=0, label='Gider', color='#e74c3c', edgecolor='black', linewidth=1.5, alpha=0.7)

# Kar çizgisini ekle
ax10.plot(x_pos, bolge_satış['Kar'], marker='o', color='#9b59b6', linewidth=3, markersize=10, label='Kar')

ax10.set_xticks(x_pos)
ax10.set_xticklabels(bolge_satış.index)
ax10.set_xlabel('Mağaza Bölgesi', fontweight='bold')
ax10.set_ylabel('Tutar (₺)', fontweight='bold')
ax10.set_title('Bölgelere Göre Satış, Gider ve Kar Analizi', fontsize=14, fontweight='bold', pad=20)
ax10.legend()
ax10.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('charts/10_waterfall.png', dpi=300, bbox_inches='tight')
print("✅ Waterfall Chart oluşturuldu: charts/10_waterfall.png")
plt.close()

print("\n" + "="*60)
print("🎉 TÜM GRAFIKLER BAŞARIYLA OLUŞTURULDU!")
print("="*60)
print("\nOluşturulan Grafikler:")
print("  01. Heatmap - Kategori x Bölge Satış Analizi")
print("  02. Violin Plot - Bölgelere Göre Satış Dağılımı")
print("  03. 3D Scatter - Üç Değişkenli Analiz")
print("  04. KDE Distributions - Dağılım Analizi")
print("  05. Correlation Heatmap - Değişken İlişkileri")
print("  06. Stacked Bar - Kategori Satışları")
print("  07. Multi-Level Pie - Çoklu Dağılımlar")
print("  08. Hexbin Plot - Yoğunluk Haritası")
print("  09. Grouped Bar - Detaylı Karşılaştırma")
print("  10. Waterfall Chart - Satış/Gider/Kar Analizi")
print("="*60)

