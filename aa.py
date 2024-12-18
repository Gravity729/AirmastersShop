import sqlite3
import bcrypt


# Создаем или подключаемся к базе данных
conn = sqlite3.connect('airmasters.db')
cursor = conn.cursor()


# Избранное
favorites = [
    (1, 2, 1),  # Иван добавил товар ID 1 в избранное
    (2, 2, 2)   # Иван добавил товар ID 2 в избранное
]
cursor.executemany('INSERT INTO Favorite (favoriteId, userId, productId) VALUES (?, ?, ?) ON CONFLICT(favoriteId) DO NOTHING', favorites)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("товары добавлены")