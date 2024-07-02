from django_unicorn.components import UnicornView

from ..models import Product, Like


class StorelistView(UnicornView):
    is_like, num_likes = None, None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id = self.component_kwargs['product_id']

    def mount(self):

        product = Product.objects.get(id=self.product_id)
        self.is_like = product.likes.filter(person=self.request.user).exists()
        self.num_likes = product.likes.count()

    def like(self):
        print('like is work')
        product = Product.objects.get(id=self.product_id)
        Like.objects.create(product=product, person=self.request.user)
        self.num_likes += 1
        self.is_like = True

    def unlike(self):
        print('unlike is work')
        Like.objects.get(person=self.request.user).delete()
        self.num_likes -= 1
        self.is_like = False



