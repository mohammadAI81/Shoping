import factory
from factory.django import DjangoModelFactory

from .models import Comment, Blog, Reply

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment
    
    author = factory.Faker('name')    
    email = factory.Faker('email')
    description = factory.Faker('paragraph', nb_sentences=6, variable_nb_sentences=False)  
    

class BlogFactory(DjangoModelFactory):
    class Meta:
        model = Blog
        
    author = factory.Faker('name')  
    title = factory.Faker("sentence", nb_words=2, variable_nb_words=True)
    description = factory.Faker('paragraph', nb_sentences=25, variable_nb_sentences=False)
    published = factory.Faker('boolean')
    
    
class ReplyFactory(DjangoModelFactory):
    class Meta:
        model = Reply
        
    author = factory.Faker('name')
    description = factory.Faker('paragraph', nb_sentences=25, variable_nb_sentences=False)
    
    