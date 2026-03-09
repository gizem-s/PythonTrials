import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import os

# Stil ayarları
plt.rcParams['figure.facecolor'] = '#f8f9fa'

# Veri yükleme
df = pd.read_csv('sales_data.csv')
df['Kar'] = df['Satış'] - df['Gider']

os.makedirs('charts', exist_ok=True)

# statsmodels kontrolü
try:
    import statsmodels.api as sm
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    HAS_STATSMODELS = True
    print("✅ statsmodels bulundu - gelişmiş istatistiksel analiz kullanılacak")
except ImportError:
    HAS_STATSMODELS = False
    print("⚠️  statsmodels bulunamadı - basit istatistiksel analiz kullanılacak")
    print("💡 Gelişmiş özellikler için: pip install statsmodels")

print("📊 İstatistiksel Grafikler Oluşturuluyor...\n")

# ============ S01: T-Test Analizi ============
print("1/6 - T-Test Analizi oluşturuluyor...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('T-Test Analizleri - İstatistiksel Anlamlılık', fontsize=16, fontweight='bold')

# Bölgelere göre satış karşılaştırması
istanbul = df[df['Mağaza_Bölgesi'] == 'İstanbul']['Satış']
ankara = df[df['Mağaza_Bölgesi'] == 'Ankara']['Satış']

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
elektronik = df[df['Ürün_Kategorisi'] == 'Elektronik']['Satış']
giyim = df[df['Ürün_Kategorisi'] == 'Giyim']['Satış']

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
plt.savefig('charts/S01_t_test_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ S01_t_test_analysis.png oluşturuldu")

# ============ S02: ANOVA Analizi ============
print("2/6 - ANOVA Analizi oluşturuluyor...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('ANOVA Analizi - Bölgeler Arası Karşılaştırma', fontsize=16, fontweight='bold')

# Bölgelere göre satış ANOVA
bolge_gruplari = [df[df['Mağaza_Bölgesi'] == bolge]['Satış']
                 for bolge in df['Mağaza_Bölgesi'].unique()]

f_stat, p_value = stats.f_oneway(*bolge_gruplari)

# Box plot
axes[0, 0].boxplot(bolge_gruplari, labels=df['Mağaza_Bölgesi'].unique())
axes[0, 0].set_title(f'Bölgelere Göre Satış ANOVA\nF={f_stat:.3f}, p={p_value:.4f}')
axes[0, 0].set_ylabel('Satış')
if p_value < 0.05:
    axes[0, 0].text(2, df['Satış'].max() * 0.9,
                   '*** İstatistiksel Olarak Anlamlı Fark ***',
                   ha='center', va='center', fontsize=10,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7))

# Tukey HSD post-hoc analizi
if HAS_STATSMODELS:
    tukey = pairwise_tukeyhsd(df['Satış'], df['Mağaza_Bölgesi'])
    tukey_text = "TUKEY HSD POST-HOC ANALİZİ\n\n" + str(tukey)
else:
    tukey_text = "TUKEY HSD ANALİZİ\n\n⚠️ statsmodels yüklü değil\nPost-hoc analiz yapılamadı"

# Tukey sonuçlarını görselleştir
axes[0, 1].axis('off')
axes[0, 1].text(0.05, 0.95, tukey_text, transform=axes[0, 1].transAxes,
               fontsize=8, verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))

# Kategorilere göre satış ANOVA
kategori_gruplari = [df[df['Ürün_Kategorisi'] == kat]['Satış']
                   for kat in df['Ürün_Kategorisi'].unique()]

f_stat2, p_value2 = stats.f_oneway(*kategori_gruplari)

axes[1, 0].boxplot(kategori_gruplari, labels=df['Ürün_Kategorisi'].unique())
axes[1, 0].set_title(f'Kategorilere Göre Satış ANOVA\nF={f_stat2:.3f}, p={p_value2:.4f}')
axes[1, 0].set_ylabel('Satış')
if p_value2 < 0.05:
    axes[1, 0].text(2, df['Satış'].max() * 0.9,
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
plt.savefig('charts/S02_anova_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ S02_anova_analysis.png oluşturuldu")

# ============ S03: Regresyon Analizi ============
print("3/6 - Regresyon Analizi oluşturuluyor...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Regresyon Analizi - Değişkenler Arası İlişkiler', fontsize=16, fontweight='bold')

# Müşteri sayısı vs Satış regresyonu
X = df['Müşteri_Sayısı']
y = df['Satış']

# Regresyon modeli
if HAS_STATSMODELS:
    X_with_const = sm.add_constant(X)
    model = sm.OLS(y, X_with_const).fit()

    # Scatter plot ve regresyon çizgisi
    slope, intercept, r_value, p_value_reg, std_err = stats.linregress(X, y)
    axes[0, 0].scatter(X, y, alpha=0.6, color='#3498db', edgecolors='black')
    axes[0, 0].plot(X, slope*X + intercept, color='#e74c3c', linewidth=3,
                   label=f'y = {slope:.2f}x + {intercept:.2f}')
    axes[0, 0].set_title(f'Müşteri Sayısı vs Satış Regresyonu\nR² = {r_value**2:.3f}, p = {p_value_reg:.4f}')
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
else:
    # Basit lineer regresyon (scipy ile)
    slope, intercept, r_value, p_value_reg, std_err = stats.linregress(X, y)

    axes[0, 0].scatter(X, y, alpha=0.6, color='#3498db', edgecolors='black')
    axes[0, 0].plot(X, slope*X + intercept, color='#e74c3c', linewidth=3,
                   label=f'y = {slope:.2f}x + {intercept:.2f}')
    axes[0, 0].set_title(f'Müşteri Sayısı vs Satış Regresyonu\nR² = {r_value**2:.3f}, p = {p_value_reg:.4f}')
    axes[0, 0].set_xlabel('Müşteri Sayısı')
    axes[0, 0].set_ylabel('Satış')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Basit residual plot
    y_pred = slope*X + intercept
    residuals = y - y_pred
    axes[0, 1].scatter(y_pred, residuals, alpha=0.6, color='#9b59b6', edgecolors='black')
    axes[0, 1].axhline(y=0, color='red', linestyle='--', linewidth=2)
    axes[0, 1].set_title('Residual Plot (Artık Değerler)')
    axes[0, 1].set_xlabel('Tahmin Edilen Değerler')
    axes[0, 1].set_ylabel('Artık Değerler')
    axes[0, 1].grid(True, alpha=0.3)

    # Normal Q-Q plot (scipy ile)
    import scipy.stats as stats
    (osm, osr), (slope_qq, intercept_qq, r_qq) = stats.probplot(residuals, dist="norm")
    axes[1, 0].plot(osm, osr, 'o', alpha=0.6, color='#9b59b6')
    axes[1, 0].plot(osm, slope_qq*osm + intercept_qq, 'r-', linewidth=2)
    axes[1, 0].set_title('Q-Q Plot (Normalite Testi)')
    axes[1, 0].set_xlabel('Teorik Quantiller')
    axes[1, 0].set_ylabel('Örnek Quantiller')

    stats_text = f"""
    BASİT REGRESYON ANALİZİ SONUÇLARI

    Model: Satış = β₀ + β₁×Müşteri_Sayısı

    Katsayılar:
    • β₀ (Sabit): {intercept:.2f}
    • β₁ (Eğim): {slope:.2f}

    Model Kalitesi:
    • R² (Açıklanan Varyans): {r_value**2:.3f}
    • p-değeri: {p_value_reg:.4f}

    Not: statsmodels yüklü değil,
    gelişmiş istatistikler kullanılamadı.
    Temel regresyon analizi yapıldı.
    """

axes[1, 1].axis('off')
axes[1, 1].text(0.05, 0.95, stats_text, transform=axes[1, 1].transAxes,
               fontsize=9, verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))

plt.tight_layout()
plt.savefig('charts/S03_regression_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ S03_regression_analysis.png oluşturuldu")

# ============ S04: Güven Aralıkları ============
print("4/6 - Güven Aralıkları oluşturuluyor...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Güven Aralıkları ve Tahmin Belirsizliği', fontsize=16, fontweight='bold')

# Bölgelere göre ortalama satış ve güven aralıkları
bolge_stats = df.groupby('Mağaza_Bölgesi')['Satış'].agg(['mean', 'std', 'count'])
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
kat_stats = df.groupby('Ürün_Kategorisi')['Satış'].agg(['mean', 'std', 'count'])
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

# Bootstrap güven aralıkları
np.random.seed(42)
bootstrap_means = []
for _ in range(1000):
    sample = np.random.choice(df['Satış'], size=len(df), replace=True)
    bootstrap_means.append(np.mean(sample))

bootstrap_ci = np.percentile(bootstrap_means, [2.5, 97.5])
observed_mean = np.mean(df['Satış'])

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
plt.savefig('charts/S04_confidence_intervals.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ S04_confidence_intervals.png oluşturuldu")

# ============ S05: p-Value Isı Haritası ============
print("5/6 - p-Value Isı Haritası oluşturuluyor...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('p-Value Isı Haritası - İstatistiksel Anlamlılık Matrisi', fontsize=16, fontweight='bold')

# Bölgeler arası p-value matrisi
bolgeler = df['Mağaza_Bölgesi'].unique()
p_matrix = np.zeros((len(bolgeler), len(bolgeler)))

for i, bolge1 in enumerate(bolgeler):
    for j, bolge2 in enumerate(bolgeler):
        if i != j:
            data1 = df[df['Mağaza_Bölgesi'] == bolge1]['Satış']
            data2 = df[df['Mağaza_Bölgesi'] == bolge2]['Satış']
            _, p_value = stats.ttest_ind(data1, data2)
            p_matrix[i, j] = p_value
        else:
            p_matrix[i, j] = 1.0

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
kategoriler = df['Ürün_Kategorisi'].unique()
p_matrix2 = np.zeros((len(kategoriler), len(kategoriler)))

for i, kat1 in enumerate(kategoriler):
    for j, kat2 in enumerate(kategoriler):
        if i != j:
            data1 = df[df['Ürün_Kategorisi'] == kat1]['Satış']
            data2 = df[df['Ürün_Kategorisi'] == kat2]['Satış']
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

Matrıs Açıklaması:
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
plt.savefig('charts/S05_p_value_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ S05_p_value_heatmap.png oluşturuldu")

# ============ S06: İstatistiksel Karşılaştırma ============
print("6/6 - İstatistiksel Karşılaştırma oluşturuluyor...")
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('İstatistiksel Karşılaştırma Grafikleri', fontsize=16, fontweight='bold')

# 1. Effect size gösterimi (Cohen's d)
istanbul = df[df['Mağaza_Bölgesi'] == 'İstanbul']['Satış']
ankara = df[df['Mağaza_Bölgesi'] == 'Ankara']['Satış']

mean_diff = istanbul.mean() - ankara.mean()
pooled_std = np.sqrt((istanbul.std()**2 + ankara.std()**2) / 2)
cohens_d = mean_diff / pooled_std

# Effect size bar plot
groups = ['İstanbul', 'Ankara']
means = [istanbul.mean(), ankara.mean()]
errors = [istanbul.std()/np.sqrt(len(istanbul)), ankara.std()/np.sqrt(len(ankara))]

bars = axes[0, 0].bar(groups, means, yerr=errors, capsize=5,
                      color=['#3498db', '#e74c3c'], alpha=0.7, edgecolor='black')
axes[0, 0].set_title(f'Grup Karşılaştırması\nCohen\'s d = {cohens_d:.3f}')
axes[0, 0].set_ylabel('Satış Ortalaması')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Effect size yorumu
if abs(cohens_d) < 0.2:
    effect_text = "Çok Küçük Etki"
    effect_color = 'gray'
elif abs(cohens_d) < 0.5:
    effect_text = "Küçük Etki"
    effect_color = 'blue'
elif abs(cohens_d) < 0.8:
    effect_text = "Orta Etki"
    effect_color = 'orange'
else:
    effect_text = "Büyük Etki"
    effect_color = 'red'

axes[0, 0].text(1, max(means) + max(errors) * 1.2, effect_text,
               ha='center', va='bottom', fontsize=10,
               bbox=dict(boxstyle='round,pad=0.3', facecolor=effect_color, alpha=0.7))

# 2. Power analysis gösterimi
if HAS_STATSMODELS:
    from statsmodels.stats.power import TTestIndPower

    effect_sizes = np.linspace(0.1, 1.0, 50)
    sample_sizes = np.linspace(10, 200, 50)

    power_analysis = TTestIndPower()
    power_matrix = np.zeros((len(sample_sizes), len(effect_sizes)))

    for i, n in enumerate(sample_sizes):
        for j, es in enumerate(effect_sizes):
            power_matrix[i, j] = power_analysis.power(es, n, 0.05, alternative='two-sided')

    im = axes[0, 1].imshow(power_matrix, aspect='auto', origin='lower',
                           extent=[effect_sizes.min(), effect_sizes.max(),
                                  sample_sizes.min(), sample_sizes.max()],
                           cmap='viridis')
    axes[0, 1].set_xlabel('Effect Size (Cohen\'s d)')
    axes[0, 1].set_ylabel('Örneklem Büyüklüğü')
    axes[0, 1].set_title('Power Analysis Heatmap')
    plt.colorbar(im, ax=axes[0, 1], label='Power (1-β)')
else:
    # Basit power gösterimi
    effect_sizes = [0.2, 0.5, 0.8]
    sample_sizes = [30, 50, 100, 200]

    # Basit power hesaplama (yaklaşık)
    power_matrix = np.zeros((len(sample_sizes), len(effect_sizes)))
    for i, n in enumerate(sample_sizes):
        for j, es in enumerate(effect_sizes):
            # Basit formül: power ≈ 1 - Φ(1.96 - es * sqrt(n/2))
            z_score = 1.96 - es * np.sqrt(n / 2)
            power_matrix[i, j] = 1 - stats.norm.cdf(z_score)

    im = axes[0, 1].imshow(power_matrix, aspect='auto', origin='lower',
                           extent=[0.2, 0.8, 30, 200], cmap='viridis')
    axes[0, 1].set_xlabel('Effect Size (Cohen\'s d)')
    axes[0, 1].set_ylabel('Örneklem Büyüklüğü')
    axes[0, 1].set_title('Power Analysis Heatmap\n(Basit Yaklaşım)')
    plt.colorbar(im, ax=axes[0, 1], label='Power (1-β)')

# 3. Normallik testleri
normality_tests = {}
for bolge in df['Mağaza_Bölgesi'].unique():
    data = df[df['Mağaza_Bölgesi'] == bolge]['Satış']
    _, p_shapiro = stats.shapiro(data)
    normality_tests[bolge] = p_shapiro

bolge_names = list(normality_tests.keys())
p_values = list(normality_tests.values())

bars2 = axes[0, 2].bar(bolge_names, p_values, color='#9b59b6', alpha=0.7, edgecolor='black')
axes[0, 2].axhline(y=0.05, color='red', linestyle='--', linewidth=2, label='α = 0.05')
axes[0, 2].set_title('Normallik Testi (Shapiro-Wilk)\np > 0.05 ise normal dağılım')
axes[0, 2].set_ylabel('p-Value')
axes[0, 2].set_ylim(0, 1)
axes[0, 2].legend()

# p-value'ları barların üzerine yaz
for bar, p_val in zip(bars2, p_values):
    axes[0, 2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                   f'{p_val:.3f}', ha='center', va='bottom', fontweight='bold')

# 4. Varyans homojenliği testi
levene_groups = [df[df['Mağaza_Bölgesi'] == bolge]['Satış']
                for bolge in df['Mağaza_Bölgesi'].unique()]
_, p_levene = stats.levene(*levene_groups)

axes[1, 0].axis('off')
levene_text = f"""
VARYANS HOMOJENLİĞİ TESTİ

Levene Testi:
• p-değeri: {p_levene:.4f}
• Sonuç: {'Homojen' if p_levene > 0.05 else 'Heterojen'}

Normallik Testleri:
{chr(10).join([f'• {bolge}: p = {p_val:.3f} ({"Normal" if p_val > 0.05 else "Normal Değil"})'
              for bolge, p_val in normality_tests.items()])}

Effect Size (Cohen's d):
• Değer: {cohens_d:.3f}
• Yorum: {effect_text}

Not: İstatistiksel testler için
normallik ve varyans homojenliği
önemli varsayımlardır.
"""
axes[1, 0].text(0.05, 0.95, levene_text, transform=axes[1, 0].transAxes,
               fontsize=9, verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral', alpha=0.8))

# 5. Korelasyon güven aralıkları
corr_data = []
for _ in range(1000):
    sample = df.sample(n=len(df), replace=True)
    corr_data.append(sample['Müşteri_Sayısı'].corr(sample['Satış']))

corr_ci = np.percentile(corr_data, [2.5, 97.5])
observed_corr = df['Müşteri_Sayısı'].corr(df['Satış'])

axes[1, 1].hist(corr_data, bins=30, alpha=0.7, color='#f39c12', edgecolor='black')
axes[1, 1].axvline(observed_corr, color='red', linewidth=2,
                  label=f'Gözlenen: {observed_corr:.3f}')
axes[1, 1].axvline(corr_ci[0], color='green', linestyle='--', linewidth=2,
                  label=f'CI Alt: {corr_ci[0]:.3f}')
axes[1, 1].axvline(corr_ci[1], color='green', linestyle='--', linewidth=2,
                  label=f'CI Üst: {corr_ci[1]:.3f}')
axes[1, 1].set_title('Korelasyon Güven Aralıkları\n(Müşteri vs Satış)')
axes[1, 1].set_xlabel('Bootstrap Korelasyonları')
axes[1, 1].set_ylabel('Frekans')
axes[1, 1].legend()

# 6. İstatistiksel anlamlılık özeti
axes[1, 2].axis('off')
summary_stats = f"""
İSTATİSTİKSEL ANALİZ ÖZETİ

Temel İstatistikler:
• Toplam Gözlem: {len(df)}
• Benzersiz Bölge: {df['Mağaza_Bölgesi'].nunique()}
• Benzersiz Kategori: {df['Ürün_Kategorisi'].nunique()}

Dağılım Özellikleri:
• Satış Ortalama: {df['Satış'].mean():.0f}
• Satış Std: {df['Satış'].std():.0f}
• Satış Min-Max: {df['Satış'].min():.0f} - {self.df['Satış'].max():.0f}

Test Sonuçları:
• Normallik: {sum(1 for p in normality_tests.values() if p > 0.05)}/{len(normality_tests)} grup normal
• Varyans Homojenliği: {'Evet' if p_levene > 0.05 else 'Hayır'}
• Effect Size: {abs(cohens_d):.2f} ({effect_text})

Öneriler:
• p > 0.05 ise parametric testler
• p ≤ 0.05 ise non-parametric testler
• Çoklu karşılaştırma için düzeltme
"""
axes[1, 2].text(0.05, 0.95, summary_stats, transform=axes[1, 2].transAxes,
               fontsize=8, verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))

plt.tight_layout()
plt.savefig('charts/S06_statistical_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ S06_statistical_comparison.png oluşturuldu")

print("\n" + "="*60)
print("🎉 TÜM İSTATİSTİKSEL GRAFİKLER BAŞARIYLA OLUŞTURULDU!")
print("="*60)
print("\n📊 Oluşturulan İstatistiksel Grafikler:")
print("  S01 - T-Test Analizi")
print("  S02 - ANOVA Analizi")
print("  S03 - Regresyon Analizi")
print("  S04 - Güven Aralıkları")
print("  S05 - p-Value Isı Haritası")
print("  S06 - İstatistiksel Karşılaştırma")
print("="*60)
