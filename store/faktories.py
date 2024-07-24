import random
import factory
from faker import Faker
from factory.django import DjangoModelFactory

from . import models

faker = Faker()

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = models.Category
        
    name = factory.Faker(
        "sentence",
        nb_words=1,
        variable_nb_words=True
    )
    description = factory.Faker('paragraph', nb_sentences=1, variable_nb_sentences=False)


class BranFactory(DjangoModelFactory):
    class Meta:
        model = models.Brand
        
    name = factory.Faker(
        "sentence",
        nb_words=1,
        variable_nb_words=True
    )
    description = factory.Faker('paragraph', nb_sentences=1, variable_nb_sentences=False)


class ColorFactory(DjangoModelFactory):
    class Meta:
        model = models.Color
        
    name = factory.Faker('color')

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = models.Comment
        
    email = factory.Faker('email')
    published = factory.Faker('boolean')
    rating = factory.LazyFunction(lambda: random.choice(['1','2','3','4','5']))
    body = factory.Faker('paragraph', nb_sentences=1, variable_nb_sentences=False)
    
    
class ProductFactory(DjangoModelFactory):
    class Meta:
        model = models.Product
    

    name = factory.LazyAttribute(lambda x: ' '.join([x.capitalize() for x in faker.words(3)]))
    description = factory.Faker('paragraph', nb_sentences=1, variable_nb_sentences=False)
    price = factory.LazyFunction(lambda: random.randint(1, 1000) + (random.randint(1, 1000) / random.randint(1, 100)))
    inventory = factory.LazyFunction(lambda: random.randint(1, 1000))
    availability = factory.Faker('boolean')
    width = factory.LazyFunction(lambda: random.randint(1, 750))
    height = factory.LazyFunction(lambda: random.randint(1, 750))
    weight = factory.LazyFunction(lambda: random.randint(1, 750))
