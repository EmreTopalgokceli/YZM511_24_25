# https://esenler.bel.tr/wp-content/uploads/2021/04/Omer-Seyfettin-Secme-Hikayeler-icler.pdf

# Gerekli Kütüphaneler
# pip install wordcloud nltk matplotlib stanza

# """
# Aşağıdaki kütüphaneler kullanılarak metin analizi ve görselleştirme işlemleri yapılacaktır:
#
# 1. 'wordcloud': Kelime bulutları (word clouds) oluşturmak için kullanılır. Bu kütüphane sayesinde,
#    metindeki kelimelerin sıklığına bağlı olarak kelime görselleştirmeleri oluşturabilirsiniz.
#
# 2. 'nltk': Doğal dil işleme (Natural Language Processing - NLP) görevlerinde sıkça kullanılan bir araçtır.
#    Stopwords, tokenizasyon, ve diğer metin işleme işlemleri için idealdir.
#
# 3. 'matplotlib': Veri görselleştirme için kullanılan bir grafik kütüphanesidir. Kelime bulutunu çizmek için
#    bu kütüphaneyi kullanacağız.
#
# 4. 'stanza': Stanford NLP tarafından geliştirilen ve çeşitli doğal dil işleme işlemlerini gerçekleştiren
#    güçlü bir araçtır. Bu projede, kelimelerin köklerini bulmak (lemmatizasyon) için kullanılacaktır.
# """

# Gerekli modülleri import ediyoruz
import re  # Düzenli ifadelerle metin işleme için
import stanza  # Kelime kökü bulma (lemmatization) ve metin analizi için
from nltk.corpus import stopwords  # Durdurma kelimeleri (stopwords) için
import nltk  # NLP araçları için
from wordcloud import WordCloud  # Kelime bulutu oluşturma için
import matplotlib.pyplot as plt  # Görselleştirme işlemleri için

# Gerekli indirmeleri gerçekleştiriyoruz
nltk.download("stopwords")  # NLTK'nin durdurma kelimeleri listesini indiriyoruz.
stanza.download("tr")  # Stanza'nın Türkçe dil modelini indiriyoruz.

# 1. METİN DOSYASINI OKUMA
# """
# Bu bölümde, metin bir dosyadan okunur. 'with open' yapısı, dosya işlemlerinin güvenli bir şekilde yapılmasını sağlar.
# Dosya işlemi tamamlandığında dosya otomatik olarak kapatılır.
#
# - r"C:\Users\Admin\Desktop\Omer Seyfettin.txt": Metin dosyasının tam yolu. (Bu yolu kendi dosya konumunuza göre
#   değiştirmelisiniz.)
# - encoding="utf-8": Dosya Türkçe karakterler içerdiğinden, bu karakterlerin doğru şekilde okunmasını sağlamak için
#   UTF-8 kullanılır.
# """
file_path = r"C:\Users\Admin\Desktop\Omer Seyfettin.txt"
with open(file_path, "r", encoding="utf-8") as dosya:
    ham_metin = dosya.read()

# Ham metnin ilk 500 karakterini yazdırarak doğru okunduğunu kontrol ediyoruz
print("Ham Metin Örneği:\n")
print(ham_metin[:500])


# 2. METİN TEMİZLEME
# """
# Metin temizleme işlemleri:
# - Küçük harfe çevirme: Büyük-küçük harf farklılıklarını önlemek için tüm harfler küçültülür.
# - Noktalama işaretlerini kaldırma: Düzenli ifadeler (regex) kullanılarak noktalama işaretleri metinden çıkarılır.
# - Stopwords çıkarma: Sık kullanılan ancak metin analizi için önemli olmayan durdurma kelimeleri temizlenir.
#
# """
# Küçük harfe çevirme
metin = ham_metin.lower()

# Noktalama işaretlerini temizleme
# 're.sub' düzenli ifadelerle eşleşen karakterleri boş string ile değiştirir.
# Asagidaki kod harfler, rakamlar, alt çizgi ve boşluk dışındaki tüm karakterleri veya rakamları hedef alarak bunları kaldırır.
metin = re.sub(r'[^\w\s]|\d', '', metin)
# r'[^\wÇçĞğİıÖöŞşÜü\s]': Harfler, rakamlar ve Türkçe karakterler dışındaki tüm karakterler seçilir.
# metin = re.sub(r'[^\wÇçĞğİıÖöŞşÜü\s]', '', metin)

# Stopwords çıkarma
# NLTK'nin Türkçe stopwords listesini alıyoruz
stopwords_listesi = set(stopwords.words("turkish"))
stopwords_listesi.add('o') # Ekleyebiliriz
# Ya da bir liste halinde ekleyebilirz.
ekstra_stopwords = ["var", "bir", "kimi", "nra", "ve", "bu", "şu", "o", "ile", "de", "da", "çok", "az", "mi", "ne", "kadar"]
stopwords_listesi.update(ekstra_stopwords)
# stopwords_listesi.remove('emre') # Cikartabiliriz

# 3. TOKENIZE ETME
# Metni boşluklara göre kelimelere ayırıyoruz (tokenizasyon).
kelimeler = metin.split()  # Tokenizasyon

# Stopwords olmayan kelimeleri seçmek için liste oluşturma
temiz_kelimeler = [i for i in kelimeler if i not in stopwords_listesi]
# i for i in kelimeler: kelimeler listesindeki her bir kelimeyi (i) döngüyle iterasyon yapar.

# Temizlenmiş metni tekrar birlestiriyoruz. Stopwords'lerden kurtulmak icin tokenize etmistik.
temiz_metin = " ".join(temiz_kelimeler)


# 4. LEMMATIZASYON (KOK BULMA)
nlp = stanza.Pipeline("tr")  # Türkçe modeli başlatir
# Bu model, metin analizinde Türkçe dil bilgisi kurallarını kullanır ve kelimelerin köklerini (lemma) bulmamıza yardımcı olur.
# Örneğin, "koşuyorum" kelimesini "koşmak" köküne dönüştürür.

# Stanza ile işlem yapma
doc = nlp(temiz_metin)

# Lemma (kök) sonuçlarını çıkarma
print("\nKelime ve Kök Halleri:\n")
for i in doc.sentences:
# 'doc.sentences' Stanza'nın analiz ettiği cümlelerin bir listesidir.
    for kelime in i.words:
# Her kelimenin orijinal hali (kelime.text) ve lemmatize edilmiş kökü (kelime.lemma) yazdırılır.
        print(f"Kelime: {kelime.text}, Kök: {kelime.lemma}")



### GORSELLESTIRME ####

from wordcloud import WordCloud
import matplotlib
matplotlib.use("TkAgg")  # Grafik arayüzü için uygun backend kullanımı, sizde gerekmeyebilir
import matplotlib.pyplot as plt


# 1. Temizlenmiş Kelimeleri Birleştir
# Önceki işlemde elde edilen kök halleriyle metni birleştiriyoruz
temiz_metin = " ".join([kelime.lemma for i in doc.sentences for kelime in i.words])

# 2. WordCloud Oluşturma
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(temiz_metin)


# 3. WordCloud Görselleştirme
plt.figure(figsize=(10, 5))  # Grafik boyutunu ayarlıyoruz
# plt.imshow(wordcloud, interpolation="bilinear")  # Kelime bulutunu gösteriyoruz
plt.imshow(wordcloud)
plt.axis("off")  # Eksenleri kapatıyoruz
# plt.title("Kelime Bulutu", fontsize=16) # Isterseniz baslik atayabilirsiniz.
plt.show()

# wordcloud.to_file("wordcloud_output.png") # Eger gorseli yazdiramazsaniz bu kod ile calisma klasorunuze kaydedebilirsiniz.
