#######################################
#######################################
############## A/B TESTI ##############
#######################################
#######################################

######################################################
# Parametrik testler icin varsayimlar
######################################################
# Normallik - shapiro
# Varyans homojenligi - levene


######################################################
# Grup karsilastirmasi parametrik & non-parametrik testler
######################################################

# Parametrik & iki grup ise 't testi' - ttest_ind
# Parametrik & iki+ grup ise 'Anova' - f_oneway

# Parametrik degil & iki grup ise 'Mann–Whitney U test' - mannwhitneyu
# Parametrik degil & iki+ grup ise 'Kruskal Wallis' - kruskal


######################################################
# Degiskenler arasinda iliski parametrik & non-parametrik testler
######################################################

# Parametrik test 'Pearson korelasyon analizi' - pearsonr
# Parametrik degil & nominal veri 'Chi-Square (Ki-Kare)' - chi2_contingency
# Parametrik degil & ordinal veri 'Chi-Square (Ki-Kare)' - spearmanr



######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# İki grup ortalaması arasında istatistiksel karşılaştırma yapmak için AB Testi veya Bağımsız İki Örneklem T Testi kullanılır. Süreç genellikle şu adımları içerir:


### Varsayım Kontrolü ###
# Normallik Varsayımı: Her iki grubun dağılımının normal olup olmadığını kontrol ederiz. Bunu Shapiro-Wilk testi ile yapabiliriz.
# Varyans Homojenliği: Levene testi  kullanarak, iki grubun varyanslarının homojen olup olmadığını test ederiz.


### Hipotezin Uygulanması ###
# Varsayımlar Sağlanıyorsa: Normallik ve varyans homojenliği varsayımı sağlanıyorsa, bağımsız iki örneklem t testi (parametrik test) uygulanır.
# Varsayımlar Sağlanmıyorsa: Eğer normallik varsayımı sağlanmıyorsa, Mann-Whitney U testi (non-parametrik test) kullanılır. Varyans homojenliği sağlanmıyorsa, t testi fonksiyonuna 'equal_var=False' argümanı girilerek Welch'in t testi uygulanır.

### Notlar ###
# Eğer normallik varsayımı sağlanmıyorsa, direkt olarak Mann-Whitney U testine geçilir.
# Yalnizca varyans homojenliği sağlanmıyorsa, bağımsız iki örneklem t testinin 'equal_var' parametresi 'False' olarak ayarlanır.


#############################################################################################################################
# Uygulama 1: Sigara İçen ve İçmeyen Müşterilerin Ortalama Hesap Tutarları Arasındaki Farkın İstatistiksel Olarak İncelenmesi
#############################################################################################################################

### İş problemi ###
# Lokanta sahibi, işletmesini daha verimli hale getirmek amacıyla bir gözlemde bulunmuştur:
# Sigara içilen bölümdeki masalarda ödenen ortalama hesap, sigara içilmeyen bölüme göre daha yüksek gibi görünmektedir.
# İşletmeyi ikiye ayırarak sigara içen ve içmeyen müşterileri farklı alanlarda ağırlamaya başlamıştır.
# Ancak bu gözlemin gerçekten bir eğilim mi yoksa rastlantısal bir durum mu olduğundan emin olmak istemektedir.
# Sigara içilen bölümü genişletmek ciddi bir yatırım gerektirecektir; özellikle havalandırma sistemlerinin güçlendirilmesi gibi
# ek masrafları da beraberinde getirecektir. Bu nedenle, lokanta sahibi öncelikle bu farkın istatistiksel olarak anlamlı olup
# olmadığını araştırmaya karar verir. Bu amaçla yapılan istatistiksel testler, ödenen ortalama hesap tutarları arasındaki
# farkın tesadüfen oluşup oluşmadığını anlamak için kullanılacaktır. Eğer fark istatistiksel olarak anlamlıysa,
# sigara içilen alanı genişletmek için gereken yatırımı yapmaya daha rahat karar verebilecektir.


########################################
# Ilgili kutuphaneleri yukleme
########################################

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, f_oneway, mannwhitneyu, kruskal, pearsonr, chi2_contingency, spearmanr

########################################
# AŞAMA 1: Veriyi Python ortamında okuma
########################################

df = pd.read_excel('veri/lokanta.xlsx')

##############################################################################
# AŞAMA 2: Hedef grupların (sigara içen vs. içmeyen) ortalamasını bakma
##############################################################################

df.groupby('Sigara_icen').agg({'Toplam_hesap': 'mean'})

############################
# AŞAMA 3: Parametrik mi Parametrik değil mi (Varsayım Kontrolü)
############################

# Normallik Varsayımı
# Varyans Homojenliği

############################
# AŞAMA 3.1 : Normallik Varsayımı (shapiro)
############################

# H0: Normal Dagilim Varsayimi saglanmaktadir.
# H1: Normal Dagilim Varsayimi saglanmamaktadir.

p_value_no_smoke = shapiro(df.loc[df['Sigara_icen'] == 'Hayır', 'Toplam_hesap']).pvalue
p_value_smoke = shapiro(df.loc[df['Sigara_icen'] == 'Evet', 'Toplam_hesap']).pvalue

print(f"Shapiro Testi (Sigara içmeyenler): p-değeri = {p_value_no_smoke}")
print(f"Shapiro Testi (Sigara içenler): p-değeri = {p_value_smoke}")

# Eger p-degeri 0.05'ten kucukse, H0 ret

############################
# AŞAMA 3.2 : Varyans Homojenliği Varsayımı (levene)
############################

# H0: Gruplarin varyansi homojendir.
# H1: Gruplarin varyansi homojen degildir.

levene_p_value = levene(df.loc[df['Sigara_icen'] == 'Hayır', 'Toplam_hesap'],
                        df.loc[df['Sigara_icen'] == 'Evet', 'Toplam_hesap']).pvalue
print(f"Levene Testi: p-değeri = {levene_p_value}")

# Eger p-degeri 0.05'ten kucukse H0 ret

############################
# AŞAMA 4 : Nihai Test
############################

# H0: Sigara icen ve icmeyen musterilerin odedigi ortalama hesap miktarlari
# arasinda istatisksel olarak anlamli bir fark yoktur.
# H1: Sigara icen ve icmeyen musterilerin odedigi ortalama hesap miktarlari
# arasinda istatisksel olarak anlamli bir fark vardir.

t_test_result = ttest_ind(df.loc[df['Sigara_icen'] == 'Hayır', 'Toplam_hesap'],
                          df.loc[df['Sigara_icen'] == 'Evet', 'Toplam_hesap'],
                          equal_var=True)
print(f"T Testi: p-değeri = {t_test_result.pvalue}")


################################################################################################################
# Normallik varsayimi saglanamasaydi, Asama 3.2 ve Asama 4'un yerine asagidaki testin kullanilmasi gerekecekti
################################################################################################################

mannwhitneyu(df.loc[df['Sigara_icen']== 'Hayır', 'Toplam_hesap'],
       df.loc[df['Sigara_icen']== 'Evet', 'Toplam_hesap'])


### Ek notlar





from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, f_oneway
from scipy.stats import mannwhitneyu, kruskal, pearsonr, chi2_contingency, spearmanr

# 1. ttest_1samp (Tek Örneklem T Testi)
# Parametrik: Evet.
# Açıklama: Verilerin normal dağıldığı varsayılır. Bir örneklemin ortalamasının belirli bir değerden
# anlamlı şekilde farklı olup olmadığını test eder.

# 2. shapiro (Shapiro-Wilk Testi)
# Parametrik: Hayır.
# Açıklama: Bu test, bir veri kümesinin normal dağılıma uygun olup olmadığını test eder.
# Dağılımın normalliğini kontrol eden non-parametrik bir testtir.

# 3. levene (Levene Testi)
# Parametrik: Hayır.
# Açıklama: İki veya daha fazla grubun varyanslarının eşit olup olmadığını test eder.
# Verilerin normal dağılım varsayımı gerektirmeyen bir varyans homojenliği testidir.

# 4. ttest_ind (Bağımsız İki Örneklem T Testi)
# Parametrik: Evet.
# Açıklama: İki bağımsız grubun ortalamalarını karşılaştırır. Verilerin normal dağıldığı ve
# gruplar arası varyansların eşit olduğu varsayılır.

# 5. f_oneway (ANOVA)
# Parametrik: Evet.
# Açıklama: İkiden fazla grubun ortalamalarını karşılaştırır. Normal dağılım ve
# varyansların eşitliği varsayımına dayanır.

# 6. mannwhitneyu (Mann-Whitney U Testi)
# Parametrik: Hayır.
# Açıklama: İki bağımsız grubun sıralarını karşılaştırır. Verilerin normal dağılıma uymadığı durumlarda
# t-testi yerine kullanılabilen bir non-parametrik testtir.

# 7. kruskal (Kruskal-Wallis Testi)
# Parametrik: Hayır.
# Açıklama: İkiden fazla bağımsız grubun sıralarını karşılaştırır. ANOVA’nın non-parametrik versiyonu olarak
# kullanılır ve verilerin sıralı olduğu varsayılır.

# 8. pearsonr (Pearson Korelasyon Katsayısı)
# Parametrik: Evet.
# Açıklama: İki sürekli değişken arasındaki doğrusal ilişkiyi ölçer. Verilerin normal dağılım gösterdiği varsayılır.

# 9. chi2_contingency (Ki-Kare Testi)
# Parametrik: Hayır.
# Açıklama: Kategorik veriler arasındaki ilişkiyi test eder. Nominal veriler için kullanılan bir bağımsızlık testidir.

# 10. spearmanr (Spearman Korelasyon Katsayısı)
# Parametrik: Hayır.
# Açıklama: İki sıralı değişken arasındaki ilişkiyi ölçer. Pearson korelasyonunun non-parametrik versiyonudur
# ve verilerin sıralı olduğu varsayılır.

# Not: Parametrik testler genellikle verilerin normal dağılım varsayımı altında çalışır ve daha güçlü sonuçlar sağlar.
# Non-parametrik testler ise dağılım varsayımı gerektirmez ve özellikle verilerin normal dağılmadığı veya
# sıralı olduğu durumlarda tercih edilir.