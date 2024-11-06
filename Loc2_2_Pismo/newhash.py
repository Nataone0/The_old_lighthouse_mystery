import hashlib

# Данные для хэширования
data = "Пример данных для хэширования"

# Создаем объект хэширования, используя алгоритм SHA-256
hash_object = hashlib.sha256()

# Преобразуем строку в байты и добавляем её в объект хэширования
hash_object.update(data.encode('utf-8'))

# Получаем хэш-значение в шестнадцатеричном формате
hash_hex = hash_object.hexdigest()

print(f"Хэш данных: {hash_hex}")

from faker import Faker

# Инициализация объекта Faker
fake = Faker('ru_RU')  # Используем локаль для русскоязычных данных

# Пример исходных данных пользователей
users = [
    {"name": "Иван Иванов", "email": "ivan@example.com"},
    {"name": "Мария Петрова", "email": "maria@example.com"},
    {"name": "Анна Смирнова", "email": "anna@example.com"}
]


def anonymize_data(data):
    anonymized_users = []

    # Проходим по каждому пользователю
    for user in data:
        # Генерируем фейковое имя и email
        fake_name = fake.name()
        fake_email = fake.email()

        # Добавляем анонимизированные данные в новый список
        anonymized_users.append({
            "name": fake_name,
            "email": fake_email
        })

    return anonymized_users


# Анонимизация данных
anonymized_users = anonymize_data(users)

# Вывод анонимизированных данных
for anonymized_user in anonymized_users:
    print(f"Анонимизированное имя: {anonymized_user['name']}")
    print(f"Анонимизированный email: {anonymized_user['email']}")
    print("-" * 40)
