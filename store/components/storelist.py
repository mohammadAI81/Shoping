from django_unicorn.components import UnicornView

from ..models import Product, Like


class StorelistView(UnicornView):
    is_like, num_likes = None, None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = Product.objects.get(id=self.component_kwargs['product_id'])

    def mount(self):
        self.is_like = self.product.likes.filter(person=self.request.user).exists()
        self.num_likes = self.product.likes.count()

    def like(self):
        Like.objects.create(product=self.product, person=self.request.user)
        self.num_likes += 1
        self.is_like = True

    def unlike(self):
        Like.objects.get(person=self.request.user, product=self.product ).delete()
        print('after delete Like')
        self.num_likes -= 1
        self.is_like = False



