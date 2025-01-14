import requests
from bs4 import BeautifulSoup
# from transformers import pipeline

# Web sitesinden haber metnini çekme fonksiyonu
def get_news_from_web(url):
    # Web sayfasına istek gönderme
    response = requests.get(url)

    # Sayfa başarılı şekilde alındıysa
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Sayfadaki haber metnini çekme (class, id gibi elementleri ihtiyaca göre düzenleyebilirsiniz)
        # Örneğin, <div class="news-content"> veya <article> gibi etiketlerden haber metnini çekebilirsiniz.
        # Burada, örnek olarak tüm <p> etiketleri üzerinden alıyoruz.
        paragraphs = soup.find_all('p')
        news_text = " ".join([para.get_text() for para in paragraphs])
        return news_text
    else:
        return None


# Web sitesinin URL'sini girin
news_url = "https://www.hurriyet.com.tr/gundem/cumhurbaskani-erdogan-36-yil-once-pkknin-ikiyaka-katliaminda-yasamini-kaybedenlerin-aileleriyle-gorustu-42658929"  # Değiştirmeniz gereken URL

# Web'den haber metnini al
news_text = get_news_from_web(news_url)
