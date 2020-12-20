import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dmfriends.settings")
django.setup()

from product.models import Product, ProductImage

CSV_PATH_PRODUCTS = '/home/lyla0427/바탕화면/product_images.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    for row in data_reader:
        if row[3] != '':
            product_ins= Product.objects.only('id').get(name=row[2])
            ProductImage.objects.create(image_url=row[3], product=product_ins)
        else:
            pass