import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Pandas'ın veri görünümü için ayarları yapıyoruz, tüm sütunları göstermek için.
pd.set_option('display.max_columns', None)
# Görünüm genişliğini 1000 piksel yaparak verilerin tamamını görmek için.
pd.set_option('display.width', 1000)

# Titanic veri setini yükleyip, sadece 'Sex', 'Age', 'Fare' sütunlarını alıyoruz.
X = pd.read_csv(r"C:\Users\etopa\Downloads\titanic.csv")[['Sex', 'Age', 'Fare']]
# 'Survived' sütunu hedef değişken (etiket) olarak alınır.
y = pd.read_csv(r"C:\Users\etopa\Downloads\titanic.csv")['Survived']

# Kategorik 'Sex' sütununu sayısal verilere çeviriyoruz:
# 'female' değerini 0, 'male' değerini ise 1 ile eşliyoruz.
X['Sex'] = X['Sex'].map({'female': 0, 'male': 1})

# Kategorik veriyi sayısal hale getirmek önemlidir çünkü makine öğrenimi algoritmaları genellikle
# sayısal verilerle çalışır. Kategorik veriler bu algoritmalar için anlamlı değildir.
# Bu yüzden kategorik veriyi sayısal verilere dönüştürmek, modelin doğru şekilde öğrenmesini sağlar.

# Veriyi eğitim ve test setlerine ayırıyoruz (%80 eğitim, %20 test).
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Veriyi ölçeklendiriyoruz (min-max normalizasyonu uyguluyoruz).
# MinMaxScaler veriyi [0, 1] aralığına çeker.
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)  # Eğitim verisi üzerinde fit ve transform işlemi yapılır.
X_test = scaler.transform(X_test)  # Test verisi yalnızca transform edilir.

# Ölçekleme, verilerin farklı aralıklara sahip olmasından dolayı modelin daha doğru öğrenmesini sağlar.
# Özellikle sinir ağları gibi algoritmalar, giriş verilerinin benzer ölçeklerde olmasını gerektirir.
# Ölçekleme işlemi, büyük aralıklardaki verilerin modelin daha yavaş öğrenmesine neden olmasını engeller.

# Yapay Sinir Ağı (ANN) modelini oluşturuyoruz.
ann_model = tf.keras.Sequential([
    # İlk gizli katman: 10 nöron, 'relu' aktivasyon fonksiyonu kullanıyoruz.
    tf.keras.layers.Dense(10, activation='relu', input_shape=(3,)),  # 3 giriş özelliği var (Sex, Age, Fare)
    # Çıkış katmanı: Tek bir nöron, tahmin edeceğimiz değer (hayatta kalma durumu)
    tf.keras.layers.Dense(1)  # Çıkış katmanı
])

# Alternatif modelde daha fazla gizli katman ekliyoruz:
ann_model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(3,)),  # 1. gizli katman
    tf.keras.layers.Dense(10, activation='relu'),  # 2. gizli katman
    tf.keras.layers.Dense(10, activation='relu'),  # 3. gizli katman
    tf.keras.layers.Dense(1)  # Çıkış katmanı
])

# Aktivasyon fonksiyonu açıklaması:
# 'relu' (Rectified Linear Unit) negatif değerleri sıfır yapar, pozitifleri ise olduğu gibi geçirir.
# Bu, modelin öğrenme sürecini daha verimli hale getirir.

# Nöron sayısını seçmek için kesin bir yöntem yoktur. Ancak katman sayısı arttıkça,
# nöron sayısını azaltmak genellikle daha iyi sonuçlar verir, çünkü model nihayetinde tek bir çıkışa ulaşır.

# Modeli derliyoruz: 'adam' optimizasyon algoritması ve 'mse' kayıp fonksiyonu seçiyoruz.
ann_model.compile(optimizer='adam', loss='mse', metrics=['mae'])
# optimizer='adam': Modelin hata payını en aza indirmeye çalışacak algoritma.
# loss='mse': Modelin hatalarını ölçmek için 'Mean Squared Error' (MSE) kullanıyoruz.
# metrics=['mae']: Modelin performansını izlemek için 'Mean Absolute Error' (MAE) kullanıyoruz.
# Kaybın ve MAE'nin küçük olması modelin daha iyi öğrenmiş olduğunu gösterir.

# Modeli eğitiyoruz. Verileri 50 kez modelden geçiriyoruz (epochs), 16'lık gruplar halinde (batch_size).
ann_model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=1)
# epochs=50: Eğitim sürecinde veriler 50 kez modelleniyor.
# batch_size=16: Model verileri 16'lık gruplar halinde işler, bu da eğitim sürecini hızlandırır.

# Modeli test verisi ile değerlendiriyoruz.
loss, mae = ann_model.evaluate(X_test, y_test)
# Test verisi üzerinde kayıp ve MAE hesaplanır.
print(f"ANN Test Loss: {loss:.4f}, Test MAE: {mae:.4f}")
# Modelin test kaybı ve MAE değeri yazdırılır.
