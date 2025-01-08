from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем базовый класс для моделей
Base = declarative_base()

# Класс Connect для работы с базой данных
class Connect:
    @staticmethod
    def create_connection():
        # Строка подключения к базе данных PostgreSQL (замените на вашу строку подключения)
        engine = create_engine("postgresql://postgres:1234@localhost:5432/my_database") #убрать пароль 
        # Создание таблиц в базе данных, если они еще не существуют
        Base.metadata.create_all(engine)
        # Создание фабрики сессий
        Session = sessionmaker(bind=engine)
        # Создание сессии
        session = Session()
        return session

# Определение модели User
class User(Base):
    __tablename__ = 'users' #название таблицы
    
    id = Column(Integer, primary_key=True) #название как в бд
    full_name = Column(String(100), nullable=False) #название как в бд
    email = Column(String(100), unique=True, nullable=False) #название как в бд
    phone_number = Column(String(15), nullable=False) #название как в бд
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP") #название как в бд
