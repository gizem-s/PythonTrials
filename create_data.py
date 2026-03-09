import pandas as pd
import numpy as np

# Random seed ile tutarlı veriler oluştur
np.random.seed(42)

# Random veriler oluştur
n_samples = 100
data = {
    'Ay': np.tile(['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
                   'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'], 9)[:n_samples],
    'Satış': np.random.randint(5000, 50000, n_samples),
    'Gider': np.random.randint(2000, 20000, n_samples),
    'Müşteri_Sayısı': np.random.randint(50, 500, n_samples),
    'Ürün_Kategorisi': np.random.choice(['Elektronik', 'Giyim', 'Yiyecek', 'Kitap'], n_samples),
    'Mağaza_Bölgesi': np.random.choice(['İstanbul', 'Ankara', 'İzmir', 'Bursa'], n_samples)
}

# DataFrame oluştur
df = pd.DataFrame(data)

# CSV dosyasına kaydet
df.to_csv('sales_data.csv', index=False, encoding='utf-8')
print("✅ sales_data.csv dosyası başarıyla oluşturuldu!")
print(f"\nVeriler:\n{df.head(10)}")

