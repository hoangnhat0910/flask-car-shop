from shop import db, app
from shop.products.models import Addproduct, Brand, Category
from shop.products.routes import index_product
from faker import Faker
import random
import os

fake = Faker()

# with app.app_context():
    # deleted = Addproduct.query.filter_by(is_fake=True).delete()
    # db.session.commit()
    # print(f"🗑️ Đã xoá {deleted} sản phẩm giả.")

def create_fake_products(n=50):
    with app.app_context():
        brands = Brand.query.all()
        categories = Category.query.all()
        IMAGE_FOLDER = 'shop/static/images'
        IMAGE_LIST = os.listdir(IMAGE_FOLDER)

        if not brands or not categories:
            print("⚠️ Vui lòng thêm brand và category trước khi tạo dữ liệu giả.")
            return

        for _ in range(n):
            brand = random.choice(brands)
            category = random.choice(categories)

            product = Addproduct(
                name=fake.unique.word().capitalize() + ' ' + fake.word().capitalize(),
                price=round(random.uniform(5000, 200000), 2),
                discount=random.randint(0, 30),
                stock=random.randint(10, 200),
                colors=','.join(fake.words(nb=4)),
                desc=fake.paragraph(nb_sentences=5),
                category_id=category.id,
                brand_id=brand.id,
                image_1=random.choice(IMAGE_LIST),
                image_2=random.choice(IMAGE_LIST),
                image_3=random.choice(IMAGE_LIST),
                # is_fake=True
            )

            db.session.add(product)
            db.session.flush()  # Để có ID ngay khi thêm

            # Index vào Elasticsearch
            index_product(product)

        db.session.commit()
        print(f"✅ Đã tạo và index {n} sản phẩm giả thành công.")

if __name__ == '__main__':
    create_fake_products(50)
