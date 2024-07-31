from django.core.management import BaseCommand
from django.db import transaction

from datetime import datetime, timedelta
import random
import factory
from faker import Faker

from blog.models import Comment, Blog
from blog.factories import CommentFactory, BlogFactory, ReplyFactory

list_of_model = [Comment, Blog]

NUM_BLOG = 400
faker = Faker()

class Command(BaseCommand):
    help = 'Generate date of blog'
    
    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Delete data\n')
        models = list_of_model
        for m in models:
            m.objects.all().delete()
            
        self.stdout.write('Create data ...')
        
        # Blog data
        print(f"Adding {NUM_BLOG} blogs ... ", end='')
        blogs = list()
        for _ in range(NUM_BLOG):
            blog = BlogFactory()
            blog.datetime_created = faker.date_time_ad(start_datetime=datetime(2021, 1, 1), end_datetime=datetime(2024, 1, 1))
            blog.datetime_modified = blog.datetime_created + timedelta(hours=random.randint(1, 5000))
            blogs.append(blog)
        print('DONE')

        # Comment data
        print("Adding blogs comment ... ", end='')
        comments = list()
        for blog in blogs:
            for _ in range(random.randint(1, 4)):
                comment = CommentFactory(blog_id=blog.id)
                comment.datetime_created = faker.date_time_ad(start_datetime=datetime(2021, 1, 1), end_datetime=datetime(2024, 1, 1))
                comment.datetime_modified = comment.datetime_created + timedelta(hours=random.randint(1, 5000))
                comments.append(comment)
        print('DONE')
        
        # Reply data
        print('Adding comment reply data ...', end=" ")
        for comment in comments:
            for _ in range(random.randint(1, 3)):
                ReplyFactory(comment_id=comment.id)
        print('DONE')
                