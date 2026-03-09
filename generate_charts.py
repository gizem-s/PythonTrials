import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Türkçe karakter desteği
plt.rcParams['font.family'] = 'Helvetica'

# CSV dosyasını oku
df = pd.read_csv('sales_data.csv')

# Stil ayarla
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

# Şekil oluştur (2x3 grid = 6 grafik)
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Satış Analizi Grafikleri', fontsize=18, fontweight='bold', y=1.00)

# 1. Satış ve Gider Trendi (Line Chart)
ax1 = axes[0, 0]
ax1.plot(df.index[:30], df['Satış'][:30], marker='o', label='Satış', linewidth=2, color='#2ecc71')
ax1.plot(df.index[:30], df['Gider'][:30], marker='s', label='Gider', linewidth=2, color='#e74c3c')
ax1.set_title('Satış ve Gider Trendi', fontweight='bold')
ax1.set_xlabel('Örnek Numarası')
ax1.set_ylabel('Tutar (₺)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Ürün Kategorisine Göre Satış (Bar Chart)
ax2 = axes[0, 1]
kategori_satış = df.groupby('Ürün_Kategorisi')['Satış'].sum().sort_values(ascending=False)
bars = ax2.bar(kategori_satış.index, kategori_satış.values, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
ax2.set_title('Ürün Kategorisine Göre Toplam Satış', fontweight='bold')
ax2.set_ylabel('Satış (₺)')
ax2.tick_params(axis='x', rotation=45)
# Değerleri göster
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'₺{int(height):,}', ha='center', va='bottom')

# 3. Satış Dağılımı (Histogram)
ax3 = axes[0, 2]
ax3.hist(df['Satış'], bins=20, color='#9b59b6', edgecolor='black', alpha=0.7)
ax3.set_title('Satış Dağılımı', fontweight='bold')
ax3.set_xlabel('Satış Miktarı (₺)')
ax3.set_ylabel('Frekans')
ax3.grid(True, alpha=0.3, axis='y')

# 4. Müşteri Sayısı ve Satış Ilişkisi (Scatter Plot)
ax4 = axes[1, 0]
scatter = ax4.scatter(df['Müşteri_Sayısı'], df['Satış'], c=df['Gider'],
                     s=100, alpha=0.6, cmap='viridis', edgecolors='black')
ax4.set_title('Müşteri Sayısı ve Satış İlişkisi', fontweight='bold')
ax4.set_xlabel('Müşteri Sayısı')
ax4.set_ylabel('Satış (₺)')
cbar = plt.colorbar(scatter, ax=ax4)
cbar.set_label('Gider (₺)')
ax4.grid(True, alpha=0.3)

# 5. Bölgeye Göre Satış (Pie Chart)
ax5 = axes[1, 1]
bolge_satış = df.groupby('Mağaza_Bölgesi')['Satış'].sum()
colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
wedges, texts, autotexts = ax5.pie(bolge_satış.values, labels=bolge_satış.index, autopct='%1.1f%%',
                                     colors=colors, startangle=90, textprops={'fontsize': 10})
ax5.set_title('Bölgelere Göre Satış Dağılımı', fontweight='bold')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# 6. Bölgeye Göre Ortalama Satış (Box Plot)
ax6 = axes[1, 2]
df.boxplot(column='Satış', by='Mağaza_Bölgesi', ax=ax6)
ax6.set_title('Bölgelere Göre Satış Dağılımı (Box Plot)', fontweight='bold')
ax6.set_xlabel('Bölge')
ax6.set_ylabel('Satış (₺)')
plt.sca(ax6)
plt.xticks(rotation=45)

# Genel ayarlar
plt.tight_layout()

# Grafikleri kaydet ve göster
plt.savefig('sales_charts.png', dpi=300, bbox_inches='tight')
print("✅ Grafikler başarıyla oluşturuldu ve 'sales_charts.png' olarak kaydedildi!")

plt.show()

# İstatistik bilgisi yazdır
print("\n" + "="*50)
print("VERİ İSTATİSTİKLERİ")
print("="*50)
print(f"\nSatış Özeti:\n{df['Satış'].describe()}")
print(f"\nGider Özeti:\n{df['Gider'].describe()}")
print(f"\nMüşteri Sayısı Özeti:\n{df['Müşteri_Sayısı'].describe()}")
print("\n" + "="*50)

