from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем базовый класс для моделей
Base = declarative_base()

# Класс Connect для работы с базой данных
class Connect:
    @staticmethod
    def create_connection():
        # Строка подключения к базе данных PostgreSQL
        engine = create_engine("postgresql://postgres:1234@localhost:5432/my_database")
        # Создание таблиц в базе данных, если они еще не существуют
        Base.metadata.create_all(engine)
        # Создание фабрики сессий
        Session = sessionmaker(bind=engine)
        # Создание сессии
        session = Session()
        return session

# Определение модели User
class User(Base):
    __tablename__ = 'users'  # Название таблицы в базе данных
    
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор пользователя
    full_name = Column(String(100), nullable=False)  # Полное имя пользователя
    email = Column(String(100), unique=True, nullable=False)  # Email пользователя (должен быть уникальным)
    phone_number = Column(String(15), nullable=False)  # Номер телефона пользователя
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")  # Дата создания записи

# Функции для работы с пользователями
def add_user(full_name, email, phone_number):
    # Функция для добавления нового пользователя
    session = Connect.create_connection()  # Создаем сессию
    new_user = User(full_name=full_name, email=email, phone_number=phone_number)  # Создаем нового пользователя
    session.add(new_user)  # Добавляем пользователя в сессию
    session.commit()  # Сохраняем изменения в базе данных
    session.close()  # Закрываем сессию

def edit_user(user_id, full_name, email, phone_number):
    # Функция для редактирования существующего пользователя
    session = Connect.create_connection()  # Создаем сессию
    user = session.query(User).filter(User.id == user_id).first()  # Находим пользователя по ID
    if user:  # Если пользователь найден
        user.full_name = full_name  # Обновляем полное имя
        user.email = email  # Обновляем email
        user.phone_number = phone_number  # Обновляем номер телефона
        session.commit()  # Сохраняем изменения
    session.close()  # Закрываем сессию

def delete_user(user_id):
    # Функция для удаления пользователя
    session = Connect.create_connection()  # Создаем сессию
    user = session.query(User).filter(User.id == user_id).first()  # Находим пользователя по ID
    if user:  # Если пользователь найден
        session.delete(user)  # Удаляем пользователя из сессии
        session.commit()  # Сохраняем изменения
    session.close()  # Закрываем сессию