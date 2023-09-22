from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Загружаем DATABASE_URL из .env файла
DATABASE_URL = config('DATABASE_URL')

# Создаем подключение к PostgreSQL
engine = create_engine(DATABASE_URL)

# Создаем сессию SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)