"""Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.

Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.

Задача 3: Определите модель продукта Product со следующими типами колонок:
id: числовой идентификатор
name: строка (макс. 100 символов)
price: числовое значение с фиксированной точностью
in_stock: логическое значение

Задача 4: Определите связанную модель категории Category со следующими типами колонок:
id: числовой идентификатор
name: строка (макс. 100 символов)
description: строка (макс. 255 символов)

Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id."""


from sqlalchemy import create_engine, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship
from decimal import Decimal

engine = create_engine(
    "mysql+mysqlconnector://ich1:ich1_password_ilovedbs@ich-edit.edu.itcareerhub.de/sql_alchemy_test",  # user, pass, база
    echo=True,
    pool_size=5,    # постоянные соединения
    max_overflow=10 # временные при пике
)

class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)



class Product(Base):
    __tablename__ = "product"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=False)

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products") # Не совсем понимаю, как лучше, с или без Mapped в случае создания relationship


class Category(Base):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category") # Тут тоже самое, хотя более понятно из-за того, что мы передаем список
    # !!! если не затруднит, объясните в комментариях к этому дз, заранее спасибо!!!

Base.metadata.create_all(engine)