# Bassly — Система бронювання квитків на музичні концерти

Bassly — це вебплатформа для перегляду музичних подій, бронювання та купівлі квитків.  
Система дозволяє організаторам створювати концерти, а користувачам — купувати квитки онлайн.

---

## Основні функції

- Перегляд доступних концертів
- Перегляд деталей події (артист, дата, локація)
- Перегляд доступних квитків
- Бронювання квитків
- Створення та оплата замовлень
- Авторизація користувачів
- Базові адміністративні операції (через Django Admin)

---

## Використані технології

### **Backend**
- Django (Python)
- Django ORM
- SQLite (або інша СКБД)

**TODO:**  

- `TODO: додати інші фреймворки/бібліотеки`

---

## API документація

API описано у форматі **OpenAPI 3.0** та доступне у файлі:

- /docs/api/openapi.yaml

Для перегляду у Swagger:

1. Перейти до https://editor.swagger.io  
2. Вставити вміст файлу `openapi.yaml`
3. Переглянути структуру методів (`Auth`, `Events`, `Tickets`, `Orders`)

- /docs/api/swagger_screenshot.png

---

## Архітектура

Архітектурні рішення оформлені у форматі ADR (Architecture Decision Records):

- docs/adr/0001-architecture-style.md

---

Також доступні діаграми:

- `docs/architecture_diagram.png`
- `docs/domain/context_map.png`

**Основний стиль:** моноліт (з можливістю еволюції до модульного моноліту або мікросервісів).

---

## Моделі (домени)

Проєкт використовує такі основні сутності:

- **User** (роль, логін, email)
- **Event** (концерт)
- **Ticket** (квиток із статусом)
- **Order** (замовлення)

Всі доменні концепти описані в:

- docs/domain/entities.md
- docs/domain/glossary.md
- docs/domain/analysis.md

---

## Локальний запуск

### 1. Створити віртуальне середовище

- python -m venv venv
- source venv/bin/activate # Linux/Mac
- venv\Scripts\activate # Windows

### 2. Встановити залежності

- pip install -r requirements.txt

### 3. Виконати міграції

- python manage.py migrate

### 4. Запустити сервер

- python manage.py runserver

---

## Зворотній зв’язок

Проєкт створений у навчальних цілях.  
У разі питань можеш звертатися через Issues у GitHub.

---

## Docker

- docker build -t bassly .
- docker compose up -d
- docker compose exec web python manage.py makemigrations
- docker compose exec web python manage.py migrate
- docker compose build
- docker compose up -d
- docker compose down (якщо зробили все що потрібно)