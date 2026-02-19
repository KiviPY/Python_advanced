"""Задача 1: Наполнение данными
Добавьте в базу данных следующие категории и продукты
Добавление категорий: Добавьте в таблицу categories следующие категории:

    Название: "Электроника", Описание: "Гаджеты и устройства."
    Название: "Книги", Описание: "Печатные книги и электронные книги."
    Название: "Одежда", Описание: "Одежда для мужчин и женщин."

    Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись, что каждый продукт связан с соответствующей категорией:
    Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
    Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
    Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
    Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
    Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда


"""
from decimal import Decimal

from sqlalchemy import create_engine, select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from hw_3 import Base, Product, Category

from config import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10
)

Session = sessionmaker(bind=engine)


categories_data = [
    {"name": "Электроника", "description": "Гаджеты и устройства."},
    {"name": "Книги", "description": "Печатные книги и электронные книги."},
    {"name": "Одежда", "description": "Одежда для мужчин и женщин."},
]


products_data = [
    {"name":  "Смартфон", "price": 299.99, "in_stock": True, "category_name": "Электроника"},
    {"name":  "Ноутбук", "price": 499.99, "in_stock": True, "category_name": "Электроника"},
    {"name":  "Научно-фантастический роман", "price": 15.99, "in_stock": True, "category_name": "Книги"},
    {"name":  "Джинсы", "price": 40.50, "in_stock": True, "category_name": "Одежда"},
    {"name":  "Футболка", "price": 20.00, "in_stock": True, "category_name": "Одежда"}
]

with (Session() as session):

    categories = [Category(**data) for data in categories_data]
    session.add_all(categories)
    try:
        session.commit()
    except IntegrityError:
        session.rollback() # Если уже существуют, то откатывает до session.commit()
        print("Категории уже существуют")


    categories_dict = {category.name: category for category in session.execute(select(Category)).scalars()} # делает {"Электроника": Category.id=1, "Книги": Category.id=2, "Одежда": Category.id=3>}
    for data in products_data:
        category = categories_dict[data["category_name"]]
        # data["category_name"] → "Электроника". categories_dict["Электроника"] Получаем: Category.id=1 name="Электроника"

        product = Product(name=data["name"],
                          price=Decimal(data["price"]),
                          in_stock=data["in_stock"],
                          category=category) # или можно category_id=category.id, результат будет тот же

        session.add(product)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        print("Какой-то или какие-то продукты уже существуют")


        """Задача 2: Чтение данных
        Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с ней продукты, включая их названия и цены."""

        categories = session.execute(select(Category)).scalars().all()
        for category in categories:
            print(f"\nКатегория: {category.name}")
            for product in category.products:
                print(f"{product.name}: {product.price}")


        """Задача 3: Обновление данных
        Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99."""

        phone = session.execute(select(Product).where(Product.name == "Смартфон")).scalar()

        if phone:
            phone.price = Decimal("349.99")
            session.commit()
            print("Цена обновлена")


        """Задача 4: Агрегация и группировка
        Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории."""

        stmt_4 = select(Category.name, func.count(Product.id).label("product_count")).join(Product).group_by(Category.id) # или Category.name
        result_4 = session.execute(stmt_4).all()

        for category in result_4:
            print(f"{category.name}: {category.product_count}")
        "============================================================"
        for name, count in result_4:
            print(f"{name}: {count}")


        """Задача 5: Группировка с фильтрацией
        Отфильтруйте и выведите только те категории, в которых более одного продукта."""

        stmt_5 = select(Category.name, func.count(Product.id).label("product_count")).join(Product).group_by(Category.id).having(func.count(Product.id) > 1)
        result_5 = session.execute(stmt_5).all()

        for category in result_5:
            print(f"{category.name}: {category.product_count}")

