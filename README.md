# 📚 O‘quv Markazi Loyihasi

## 📌 Loyihaning qisqacha tavsifi

**📚 O‘quv Markazi Loyihasi** - bu Graphqlda ishlab chiqilgan mahsus datur. 

Ushbu loyiha o‘quv markazlari uchun talabalar, o‘qituvchilar va kurslarni boshqarish jarayonini avtomatlashtirishga mo‘ljallangan.

## ⚙️ Asosiy xususiyatlar

- **GraphQL** — Yuqori samaradorlikka ega ma’lumot olish va yuborish texnologiyasi. Moslashuvchan so‘rovlar, aniq ma’lumot olish va tarmoq yukini kamaytirish imkonini beradi.
- **Redis** — Xotirada ishlovchi tezkor ma’lumotlar bazasi. Kesh, navbat va xabar brokeri sifatida keng qo‘llanadi.
- **Celery** — Asinxron fon vazifalarini bajarish va periodik ishlarni rejalashtirish uchun kuchli Python kutubxonasi.
- **RabbitMQ** — Xabarlarni uzatish uchun ishonchli broker. Ko‘p komponentli tizimlarda ma’lumotlarni almashish jarayonini boshqaradi.
- **Docker** — Ilovani konteynerlash orqali turli muhitlarda bir xil ishlashini ta’minlaydi va deploy jarayonini osonlashtiradi.

## 🛠 Texnologiyalar

| Texnologiya | Tavsifi                                                |
|-------------|--------------------------------------------------------|
| Python 3.12 | Asosiy dasturlash tili                                 |
| Graphql     | Backend API yaratish freymvorki                        |
| PostgreSQL  | Ma’lumotlar bazasi                                     |
| Docker      | Konteynerizatsiya                                      |
| Redis       | Kesh va xabar brokeri                                  |
| Celery      | Fon vazifalarni asinxron bajarish va periodik ishlash  |
| RabbitMQ    | Xabarlarni uzatish uchun ishonchli broker              |

## 🛠️ O'rnatish va ishga tushirish

1. Repositoriyani klonlash

```bash
git clone https://github.com/XojaxonovPY/Training-center.git
cd Training-center
```

2. Virtual muhit yaratish va kutubxonalarni o'rnatish

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Docker yordamida ishga tushirish

```bash
docker-compose up --build
```

4. Ma'lumotlar bazasini migratsiya qilish

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Ilovani ishga tushirish

```bash
python manage.py runserver 0.0.0.0:8000
```

## 🔧 .env konfiguratsiyasi

Ilova ishlashi uchun `.env` faylida quyidagi parametrlarni sozlash kerak:

```env
DP_NAME=Your_db_name
DP_USER=Your_db_username
DP_PASSWORD=Your_db_password
DP_HOST=Your_db_host
DB_SERVER_HOST=Your_server_host
DP_PORT=Your_db_port
EMAIL=your_email
PASSWORD=your_password
REDIS_URL=redis://host:port/0
RABBIT_URL=amqp://guest:guest@host:port //
```

## Project Figmasi

[Figmani korish](https://www.figma.com/design/HCfpAZkN9J6wEDDyT7qabw/Untitled--Copy-?node-id=0-1&p=f)

## 📊 Ma’lumotlar bazasi modeli

[DrawSQL’da model sxemasini ko‘rish](https://drawsql.app/teams/gayrat-1/diagrams/oquv-markazi)

## 📄 Litsenziya

Loyiha MIT litsenziyasi asosida tarqatiladi.
