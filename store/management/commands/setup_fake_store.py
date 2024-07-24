from django.core.management.base import BaseCommand
from django.db import transaction

from faker import Faker
from datetime import datetime, timedelta
import random

from store.models import Brand, Category, Comment, Color, Product
from store.faktories import CategoryFactory, CommentFactory, ColorFactory, ProductFactory, BranFactory

faker = Faker()
list_of_model = [Product, Brand, Category, Comment, Color]

NUM_CATEGORY = 10
NUM_BRANC = 10
NUM_COLOR = 10
NUM_PRODUCT = 300

class Command(BaseCommand):
    help = 'Generates fake data'
    
    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Delete data old ...')
        models = list_of_model
        for m in models:
            m.objects.all().delete()
        
        self.stdout.write('Createing new data\n')
        
        # Category Data
        print(F'create {NUM_CATEGORY} categories... ', end='')
        all_categories = [CategoryFactory() for _ in range(NUM_CATEGORY)]
        print('DONE')
        
        # Brand Data
        print(F'create {NUM_BRANC} brands... ', end='')
        all_brands = [BranFactory() for _ in range(NUM_BRANC)]
        print('DONE')

        # Color Data
        print(F'create {NUM_COLOR} colors... ', end='')
        all_colors = [ColorFactory() for _ in range(NUM_COLOR)]
        print('DONE')
        
        # Product Data
        print(F'create {NUM_PRODUCT} products... ', end='')
        all_product = list()
        for _ in range(NUM_PRODUCT):
            product = ProductFactory(
                brand_id=random.choice(all_brands).id,
                category_id=random.choice(all_categories).id,
                color_id=random.choice(all_colors).id
                )
            product.datetime_created = faker.date_time_ad(start_datetime=datetime(2021, 1, 1), end_datetime=datetime(2024, 1, 1))
            all_product.append(product)
        print('DONE')
        
        
        # Comment Data
        print(F'Adding product comments... ', end='')
        for product in all_product:
            for _ in range(random.randint(1, 5)):
                comment = CommentFactory(product_id=product.id, author_id=1)
                comment.datetime_created = faker.date_time_ad(start_datetime=datetime(2021, 1, 1), end_datetime=datetime(2024, 1, 1))
        print('DONE')        
