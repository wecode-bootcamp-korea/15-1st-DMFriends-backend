import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dmfriends.settings")
django.setup()

from product.models import Category, Subcategory, Product

CSV_PATH_PRODUCTS = '/home/lyla0427/바탕화면/products_전체 제품 데이터.csv'

# a1 = Category(name="리빙")
# a2 = Category(name="잡화")
# a3 = Category(name="의류")

# Category.objects.bulk_create([a1, a2, a3])

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    # for row in data_reader:
    #     if row[1] != '':
    #         category_ins = Category.objects.only('id').get(name=row[0])
    #         Subcategory.objects.create(name=row[1], category=category_ins)
    #     else:
    #         pass

    for row in data_reader:
        if row[4] != '':
            category_ins    = Category.objects.only('id').get(name=row[0])
            subcategory_ins = Subcategory.objects.only('id').get(name=row[1])
            Product.objects.create(name=row[4], price=row[5], star_rating=row[6], created_at=row[9], category=category_ins, subcategory=subcategory_ins, image_url=row[10])

        else:
            pass
