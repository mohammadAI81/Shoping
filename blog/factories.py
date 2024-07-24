import random
import factory
from datetime import datetime, timedelta
from factory.django import DjangoModelFactory
from faker import Faker

from .models import Comment, Blog

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment
    
    author = factory.Faker('name')    
    email = factory.Faker('email')
    description = factory.Faker('paragraph', nb_sentences=1, variable_nb_sentences=False)  
    

class BlogFactory(DjangoModelFactory):
    class Meta:
        model = Blog
    author = factory.Faker('name')  
    title = factory.Faker(
        "sentence",
        nb_words=2,
        variable_nb_words=True
    )
    description = factory.Faker('paragraph', nb_sentences=1, variable_nb_sentences=False)
    published = factory.Faker('boolean')
    
    