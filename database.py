import sqlite3
import bcrypt

# Функция для хеширования пароля
def hash_password(plain_text_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed_password
# Создаем или подключаемся к базе данных
conn = sqlite3.connect('airmasters.db')
cursor = conn.cursor()

# Создание таблиц
cursor.executescript('''
-- Таблица марок автомобилей
CREATE TABLE IF NOT EXISTS CarBrand (
    carBrandId INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Таблица моделей автомобилей
CREATE TABLE IF NOT EXISTS CarModel (
    carModelId INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    carBrandId INTEGER NOT NULL,
    FOREIGN KEY (carBrandId) REFERENCES CarBrand(carBrandId)
);

-- Таблица категорий товаров
CREATE TABLE IF NOT EXISTS Category (
    categoryId INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Таблица товаров
CREATE TABLE IF NOT EXISTS Product (
    productId INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    stockQuantity INTEGER NOT NULL,
    carModelId INTEGER,
    categoryId INTEGER NOT NULL,
    FOREIGN KEY (carModelId) REFERENCES CarModel(carModelId),
    FOREIGN KEY (categoryId) REFERENCES Category(categoryId)
);

-- Таблица фотографий товаров
CREATE TABLE IF NOT EXISTS ProductPhoto (
    photoId INTEGER PRIMARY KEY,
    productId INTEGER NOT NULL,
    photoUrl TEXT NOT NULL,
    FOREIGN KEY (productId) REFERENCES Product(productId)
);

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS User (
    userId INTEGER PRIMARY KEY,
    fName TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    role INTEGER NOT NULL CHECK (role IN (1, 2)),
    login TEXT NOT NULL,
    password TEXT NOT NULL
);

-- Таблица корзины
CREATE TABLE IF NOT EXISTS Cart (
    cartId INTEGER PRIMARY KEY,
    userId INTEGER NOT NULL,
    productId INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (userId) REFERENCES User(userId),
    FOREIGN KEY (productId) REFERENCES Product(productId)
);

-- Таблица избранного
CREATE TABLE IF NOT EXISTS Favorite (
    favoriteId INTEGER PRIMARY KEY,
    userId INTEGER NOT NULL,
    productId INTEGER NOT NULL,
    FOREIGN KEY (userId) REFERENCES User(userId),
    FOREIGN KEY (productId) REFERENCES Product(productId)
);
''')

# Вставка данных
# Марки автомобилей
car_brands = [(1, 'BMW'), (2, 'Chevrolet')]
cursor.executemany('INSERT INTO CarBrand (carBrandId, name) VALUES (?, ?) ON CONFLICT(carBrandId) DO NOTHING', car_brands)

# Модели автомобилей
car_models = [
    (1, '3 Series', 1), (2, '5 Series', 1), (3, 'X5', 1),
    (4, 'Camaro', 2), (5, 'Corvette', 2), (6, 'Tahoe', 2)
]
cursor.executemany('INSERT INTO CarModel (carModelId, name, carBrandId) VALUES (?, ?, ?) ON CONFLICT(carModelId) DO NOTHING', car_models)

# Категории товаров
categories = [
    (1, 'Пневмоподвеска Комфорт'), (2, 'Пневмоподвеска Занижение'), (3, 'Комплекты цифрового управления'),
    (4, 'Коммерческий транспорт, минивэны'), (5, 'Внедорожники и пикапы'), (6, 'Ремонт систем пневмоподвески'),
    (7, 'Пневмоподвеска на ВАЗ (Lada), ГАЗ'), (8, 'Управление пневмоподвеской'), (9, 'Пневмоподушки'),
    (10, 'Компрессоры'), (11, 'Ресиверы'), (12, 'Комплектующие'),
    (13, 'Пневмоцилиндры Air Cups для винтовых стоек'), (14, 'Подкачка шин и надувного оборудования'), (15, 'Пневмогудок')
]
cursor.executemany('INSERT INTO Category (categoryId, name) VALUES (?, ?) ON CONFLICT(categoryId) DO NOTHING', categories)

# Товары
products = [
    (1, 'Пневмоподвеска для BMW 3 Series', 'Высококачественная пневмоподвеска.', 1200.00, 10, 1, 1),
    (2, 'Пневмоподвеска для BMW 5 Series', 'Комфортная подвеска.', 1300.00, 8, 2, 1),
    (3, 'Пневмоподвеска для BMW X5', 'Идеальное решение для внедорожников.', 1500.00, 5, 3, 1),
    (4, 'Пневмоподвеска для Chevrolet Camaro', 'Отличное качество.', 1400.00, 7, 4, 2),
    (5, 'Пневмоподвеска для Chevrolet Corvette', 'Для спортивных автомобилей.', 1600.00, 6, 5, 2),
    (6, 'Пневмоподвеска для Chevrolet Tahoe', 'Надежность и комфорт.', 1700.00, 4, 6, 5),
    (7, 'Пневмогудок 1', 'Универсальный пневмогудок.', 200.00, 15, None, 15),
    (8, 'Пневмогудок 2', 'Компактный пневмогудок.', 250.00, 20, None, 15)
]
cursor.executemany('INSERT INTO Product (productId, name, description, price, stockQuantity, carModelId, categoryId) VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(productId) DO NOTHING', products)

# Фотографии товаров
product_photos = [
    (1, 1, 'https://airmasters.ru/upload/resize_cache/iblock/b4b/mazda%20rx7%20%D0%98%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%20WhatsApp%202024-02-15%20%D0%B2%2013.27.53_732cff5c_thumb_640_300_water__proportions_.jpg'), (2, 1, 'https://airmasters.ru/upload/resize_cache/iblock/e56/75536_v0_1395864190-770x433_thumb_640_300_water__proportions_.jpg'), (3, 1, 'https://airmasters.ru/upload/resize_cache/iblock/9d5/air-lift-performance-z3-111-1170x658_thumb_0_600_water_.jpg'),
    (4, 2, 'https://airmasters.ru/upload/resize_cache/iblock/276/75673_v0_1408645957-770x433_thumb_640_300_water__proportions_.jpg'), (5, 3, 'https://airmasters.ru/upload/resize_cache/iblock/d38/pnevmopodveska_2.comfort_2_thumb_640_300_water__proportions_.JPG'),
    (6, 4, 'https://airmasters.ru/upload/resize_cache/iblock/f1b/ShtucB_thumb_640_300_water__proportions_.JPG'), (7, 5, 'https://airmasters.ru/upload/resize_cache/iblock/083/komplekt_podkachki_koles_s_bistrorazemom_2_thumb_640_300_water__proportions_.jpg'),
    (8, 6, 'https://airmasters.ru/upload/resize_cache/iblock/df8/x5.jpg.pagespeed.ic.7mlkKMoM9d_thumb_640_300_water__proportions_.jpg'), (9, 7, 'https://airmasters.ru/upload/resize_cache/iblock/eb0/data-komplekty-8gauge-powerkit1-84881-std-800x500_thumb_640_300_water__proportions_.jpg'), (10, 8, 'https://airmasters.ru/upload/resize_cache/iblock/193/UN_46129__34549.1407965160.1280.1280_thumb_640_300_water__proportions_.jpg')
]
cursor.executemany('INSERT INTO ProductPhoto (photoId, productId, photoUrl) VALUES (?, ?, ?) ON CONFLICT(photoId) DO NOTHING', product_photos)

# Пользователи
users = [
    (1, 'Админ', '+971500000001', 'admin@airmasters.com', 1, 'admin', hash_password('adminpass')),
    (2, 'Иван', '+971500000002', 'ivan@airmasters.com', 2, 'ivan_user', hash_password('password123'))
]

for user in users:
    cursor.execute(
        'INSERT INTO User (userId, fName, phone, email, role, login, password) VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(userId) DO NOTHING',
        (user[0], user[1], user[2], user[3], user[4], user[5], user[6])
    )

# Корзина
cart = [
    (1, 2, 1, 2),  # Иван купил 2 товара ID 1
    (2, 2, 2, 1)   # Иван купил 1 товар ID 2
]
cursor.executemany('INSERT INTO Cart (cartId, userId, productId, quantity) VALUES (?, ?, ?, ?) ON CONFLICT(cartId) DO NOTHING', cart)

# Избранное
favorites = [
    (1, 2, 1),  # Иван добавил товар ID 1 в избранное
    (2, 2, 2)   # Иван добавил товар ID 2 в избранное
]
cursor.executemany('INSERT INTO Favorite (favoriteId, userId, productId) VALUES (?, ?, ?) ON CONFLICT(favoriteId) DO NOTHING', favorites)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных успешно создана и заполнена с хешированием паролей!")
