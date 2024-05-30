# Bu Projenin Amacı Nedir?

Bu projenin temel amacı kullanıcıların kayıt olup, hem kendi İHA'larını ve özelliklerini
tanımlayıp hemde başka kullanıcıların tanımladığı İHA'larını kiralayabilmesini sağlamaktır.

Kullanıcılar tek bir profil ile hem İHA kiralayabilir hemde kendi İHA'larının
kiralanmasını yönetebilmektedir.

## Teknik Özellikleri Nelerdir?

### Kullanılan Teknolojiler

#### -Python

#### -Django

#### -Django Rest Framework

#### -Postgresql

#### -Docker

#### -HTML/CSS (Bootstrap)

#### -Javascript

#### -Jquery ve Ajax

#### -Datatables

### Sistem Yapısı

- Proje temel olarak server-side render şeklinde yazılmıştır fakat detayların listelenmesi, verilerin silinmesi ve
  güncellenmesi gib bazı noktalar Django Rest Framework ile yapılmıştır.
- Ön yüzü HTML/CSS olarak yazılmıştır. Ek olarak Bootstrap kullanılmıştır. Ön yüzden Back-end tarafına API erişimi Ajax
  ile sağlanmıştır.
- Veritabanı olarak Postgresql kullanılmıştır.

## Nasıl Çalıştırılır?

### Docker

- İlgili sunucuya docker yüklenmelidir.
- Örnek olarak verilen 'env.docker.exp' dosyasının içeriği doldurulup .env olarak kayıt edilmelidir.
- .env dosyası oluşturulduktan sonra proje dizininde ```docker-compose up --build``` komutu çalıştırılıp sunucu ayağa kaldırılabilir.

### Standart

- İlgili sunucuda Python3.9 veya daha üst bir sürümü olmalıdır.
- İstenildiği takdirde sanal bir Python ortamı oluşturulabilir. Bunun için ilgili dizinin içinde ```python3 -m venv <sanal_ortam_adi>``` komutu çalıştırılıp sonrasında bu ortam aktif edilmelidir. 
- Gerekli paketlerin yüklenmesi için ```pip3 install -r requirements.txt``` çalıştırılmalıdır.
- Örnek olarak verilen 'env.standart.exp' dosyasının içeriği doldurulup .env olarak kayıt edilmelidir.
- Tablolar oluşması için ```python3 manage.py migrate``` komutu çalıştırılmalıdır.
- Sunucuyu ayağa kaldırmak için ```python3 manage.py runserver``` komutu çalıştırılmalıdır.


## Kullanım

### Test

- Testleri çalıştırmak için şu komut dosya dizininde çalıştırılmalıdır: ```python3 manage.py test ```

### Kayıt & Giriş

- Proje ayağa kalktığı zaman ```<url>/``` adresine gittiğimiz zaman giriş yapmamışsak bizi giriş sayfasına
  yönlendiriyor.
- Giriş sayfasında 'Kayıt Ol' butonu ile sisteme kayıt olabiliriz.
- Kayıt için doldurmamız gereken Email, Parola, İsim gibi alanları doldurduktan sonra kayıt olma işlemini
  tamamlayabiliriz. Daha sonra bizi tekrar giriş yapabileceğimiz sayfaya yönlendiriyor.
- Giriş yapıldıktan sonra bizi ana sayfaya yönlendiriyor. Eğer giriş yapmadan bir sayfaya erişmek istediysek oraya yönlendirme yapıyor.
- Ana sayfaya yönlenirsek burada bazı istatistikler karşımıza çıkıyor.

### Profil Yönetimi

- Üst alandaki isim ve soyismin bulunduğu kısımda Profil butonuna bastığımızda profilimizi yönettiğimiz alan açılıyor.
- Profil yönetim sayfasından, kayıt olurken girdiğimiz bilgileri güncelleyebiliriz.

### İHA'ların Yönetimi

- Sağ taraftaki menüde "İHA'larım" sekmesine bastığımız zaman bize ait olan İHA'ların listesini görebiliriz.
- İHA'larım sayfasının sağ üst tarafında mevcut İHA'larımızı ekleyebiliriz
- İHA ekleme kısmının yanında Filtre butonu bulunmaktadır. Burada eklediğimiz İHA'lar içinde detaylı filtreme yapabiliriz.
- Ayrıca İHA'ların listelendiği tablo içindede tabloda bulunan 'Ara' kısmından arama yapabiliriz.
- Tablo kolonlarının üzerine bastığımızda ise büyükten küçüğe veya küçükten büyüğe sıralama yapabiliriz.
- Tabloda eklediğimiz İHA'ların en sol kısmındaki aksiyonlar kısmından ise eklediğimiz İHA'ların detayını, silme işlemini, güncelleme işlemini ve kiralama detay işlemlerini yapabiliriz.
- Kiralama detay sayfasına gittiğimiz zaman başka kullanıcıların o İHA için oluşturduğu kiralama talepleri gözükmektedir.
- Kiralama detay sayfasına varsayılan olarak sadece cevaplanmamış talepleri gösterir burada sağ yukarıdaki filtrede bu filtreyi görebiliriz. Eğer tüm detayları görmek istersek filtre kısmından görmek istediğimiz dataları filtreyebiliriz.
- Kiralama detay sayfasındaki tabloda aksiyon altında o kullanıcının talebini onaylayabilir veya reddebiliriz. 


### Kiralık İHA'ların Yönetimi

- Sağ taraftaki menüde "Tüm İlanlar" sekmesine bastığımız zaman sistemde kayıtlı kiralayabileceğimiz tüm İHA'lar listenir.
- Tüm ilanlar sayfasında sağ yukarıda Filtre kısmından buradaki ilanları detaylıca filtreyebiliriz veya tabloda Ara kısmından da arama yapabiliriz.
- İHA'ların detay ve kiralama butonları aksiyonlar kolonunun altındadır.
- Kiralamak istediğimiz iha için aksiyon altındaki butona basıp Kiralama Talebi oluştur butonuna basıyoruz. Açılan menüde hangi tarihler arasında kiralama yapacağımızı seçip talep oluşturuyoruz.
- Eğer girdiğimiz tarihlerde İHA kiralanmış ise sistem bize uyarı veriyor ve başka bir tarih seçmemizi istiyor. İHA o tarihte müsait ise talep İHA'nın sahibine gidiyor.


### Kiralanan İHA'ların Yönetimi

- Sağ taraftaki menüde "Kiralamalarım" sekmesine bastığımız zaman sistemde kiraladığımız & kiralamak için talep ettiğimiz İHA'ları ve kiralama detaylarını görebiliriz.
- Kiralamalarım sayfasında sağ yukarıdaki Filtre kısmında detaylı filtreleme yapabiliriz veya tablodaki Ara alanından da direkt arama yapabiliriz.
- Kiralamalarım sayfasındaki tabloda seçilen İHA, başlangıç tarihi, bitiş tarihi, kiralama durumunu görebiliriz.
- Kiralama durumu mevcut talebin durumunu gösterir. Yani talep onaylanmış mı bekliyor mu gibi bilgiyi bize göstermektedir.
- Aksiyon alanındaki butonlar ile onay bekleme aşamasındaki taleplerimizi güncelleyebiliriz veya talebimizi iptal edebiliriz.