import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Veri yükleme
df = pd.read_csv('sales_data.csv')
df['Kar'] = df['Satış'] - df['Gider']

print('📊 İstatistiksel Anlamlılık Grafikleri Oluşturuluyor...')

# ============ 1. T-Test Analizi ============
print('1. T-Test analizi...')
istanbul = df[df['Mağaza_Bölgesi'] == 'İstanbul']['Satış']
ankara = df[df['Mağaza_Bölgesi'] == 'Ankara']['Satış']

if len(istanbul) > 1 and len(ankara) > 1:
    t_stat, p_value = stats.ttest_ind(istanbul, ankara)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('📊 T-Test: İstatistiksel Anlamlılık Analizi', fontsize=14, fontweight='bold')

    # Box plot
    ax1.boxplot([istanbul, ankara], labels=['İstanbul', 'Ankara'])
    ax1.set_title(f'Bölge Karşılaştırması\np = {p_value:.4f}')
    ax1.set_ylabel('Satış Miktarı')

    if p_value < 0.05:
        ax1.text(1.5, max(istanbul.max(), ankara.max()) * 0.9,
                '*** p < 0.05\nİstatistiksel Anlamlı ***',
                ha='center', va='center', fontsize=10,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7))

    # Histogram karşılaştırması
    ax2.hist(istanbul, alpha=0.7, label='İstanbul', bins=15, color='#3498db', edgecolor='black')
    ax2.hist(ankara, alpha=0.7, label='Ankara', bins=15, color='#e74c3c', edgecolor='black')
    ax2.set_title('Dağılım Karşılaştırması')
    ax2.set_xlabel('Satış')
    ax2.set_ylabel('Frekans')
    ax2.legend()

    plt.tight_layout()
    plt.savefig('charts/S01_t_test_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ S01_t_test_analysis.png oluşturuldu')

# ============ 2. Güven Aralıkları ============
print('2. Güven aralıkları...')
bolge_stats = df.groupby('Mağaza_Bölgesi')['Satış'].agg(['mean', 'std', 'count'])
bolge_stats['se'] = bolge_stats['std'] / np.sqrt(bolge_stats['count'])
bolge_stats['ci_lower'] = bolge_stats['mean'] - 1.96 * bolge_stats['se']
bolge_stats['ci_upper'] = bolge_stats['mean'] + 1.96 * bolge_stats['se']

fig, ax = plt.subplots(figsize=(10, 6))
x_pos = np.arange(len(bolge_stats.index))
ax.bar(x_pos, bolge_stats['mean'], yerr=1.96*bolge_stats['se'],
      capsize=5, color='#3498db', edgecolor='black', alpha=0.7)
ax.set_title('📊 Güven Aralıkları: Bölge Ortalamaları (95% CI)')
ax.set_xticks(x_pos)
ax.set_xticklabels(bolge_stats.index)
ax.set_ylabel('Satış Ortalaması')
ax.grid(True, alpha=0.3, axis='y')

plt.savefig('charts/S02_confidence_intervals.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ S02_confidence_intervals.png oluşturuldu')

# ============ 3. p-Value Isı Haritası ============
print('3. p-Value ısı haritası...')
bolgeler = df['Mağaza_Bölgesi'].unique()
p_matrix = np.zeros((len(bolgeler), len(bolgeler)))

for i, bolge1 in enumerate(bolgeler):
    for j, bolge2 in enumerate(bolgeler):
        if i != j:
            data1 = df[df['Mağaza_Bölgesi'] == bolge1]['Satış']
            data2 = df[df['Mağaza_Bölgesi'] == bolge2]['Satış']
            _, p_val = stats.ttest_ind(data1, data2)
            p_matrix[i, j] = p_val
        else:
            p_matrix[i, j] = 1.0

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(p_matrix, cmap='RdYlGn_r', vmin=0, vmax=0.1)

# p-value'ları yaz
for i in range(len(bolgeler)):
    for j in range(len(bolgeler)):
        if i != j:
            color = 'white' if p_matrix[i, j] < 0.05 else 'black'
            ax.text(j, i, f'{p_matrix[i, j]:.3f}', ha='center', va='center',
                   color=color, fontweight='bold', fontsize=10)

ax.set_xticks(range(len(bolgeler)))
ax.set_yticks(range(len(bolgeler)))
ax.set_xticklabels(bolgeler, rotation=45)
ax.set_yticklabels(bolgeler)
ax.set_title('🔥 p-Value Isı Haritası\n(Kırmızı: p<0.05 = Anlamlı Fark)')

plt.colorbar(im, ax=ax, label='p-Value')
plt.tight_layout()
plt.savefig('charts/S03_p_value_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ S03_p_value_heatmap.png oluşturuldu')

# ============ 4. Regresyon Analizi ============
print('4. Regresyon analizi...')
X = df['Müşteri_Sayısı']
y = df['Satış']

# Lineer regresyon
slope, intercept, r_value, p_value_reg, std_err = stats.linregress(X, y)

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(X, y, alpha=0.6, color='#3498db', edgecolors='black', s=50)
ax.plot(X, slope*X + intercept, color='#e74c3c', linewidth=3,
       label=f'y = {slope:.2f}x + {intercept:.2f}\nR² = {r_value**2:.3f}, p = {p_value_reg:.4f}')

ax.set_title('📈 Regresyon Analizi: Müşteri Sayısı vs Satış')
ax.set_xlabel('Müşteri Sayısı')
ax.set_ylabel('Satış')
ax.legend()
ax.grid(True, alpha=0.3)

if p_value_reg < 0.05:
    ax.text(0.02, 0.98, '*** p < 0.05\nRegresyon anlamlı ***',
           transform=ax.transAxes, fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='green', alpha=0.7))

plt.savefig('charts/S04_regression_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ S04_regression_analysis.png oluşturuldu')

print('\n🎉 Tüm istatistiksel anlamlılık grafikleri başarıyla oluşturuldu!')
print('\n📊 Oluşturulan Grafikler:')
print('  S01_t_test_analysis.png      - T-Test analizi')
print('  S02_confidence_intervals.png - Güven aralıkları')
print('  S03_p_value_heatmap.png      - p-Value ısı haritası')
print('  S04_regression_analysis.png  - Regresyon analizi')
print('\n📁 Grafikler charts/ klasöründe kaydedildi!')
