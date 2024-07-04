from django.core.paginator import Paginator
from django.db.models import Q, Count
from django_unicorn.components import UnicornView

from ..models import Product, Color, Category, Brand
from ..variable import SHOW, SORT


class ListproductctegoryView(UnicornView):
    color, brand = '', ''
    sorts = SORT
    shows = SHOW
    categories = Category.objects.none()
    brands = Brand.objects.none()
    colors = Color.objects.none()
    products = Product.objects.none()
    values = {'sort': 'name', 'show': 'All'}

    def mount(self):
        # For Filter
        # if sort := request_get.get('sort'):
        #     products = products.order_by(sort)
        #
        # category = request_get.get('category')
        # brand = request_get.get('brand')
        # color = request_get.get('color')
        # if category or brand or color:
        #     q_objects = Q()
        #     if category:
        #         q_objects |= Q(category__name=category)
        #     if brand:
        #         q_objects &= Q(brand__name=brand)
        #     if color:
        #         q_objects &= Q(color__name=color)
        #     products = products.filter(q_objects)
        #
        # context = {'products': products, 'num': request_get.get('page_num')}

        # Pagination
        # page_num = request_get.get('page')
        # if context['num'] is None:
        #     context['num'] = request_get.get('num')
        # if page_num or context['num']:
        #     if context['num'] != 'All':
        #         paginator = Paginator(products, context['num'])
        #         products = paginator.get_page(page_num)
        #         context['page_obj'] = products
        self.categories = Category.objects.all()
        self.brands = Brand.objects.all()
        self.colors = Color.objects.all()
        self.products = Product.objects.select_related('category', 'color', 'brand').order_by(self.values.get('sort'))
        # Filter Of Category
        if self.request.GET:
            category_id = self.request.GET.get('category')
            if category_id != '0':
                self.products = self.products.filter(category_id=category_id)
        
    def product_filter(self):
        # Filter Of Color & Brand
        if self.color or self.brand:
            q_obj = Q()
            if self.color:
                q_obj &= Q(color_id=self.color)
            if self.brand:
                q_obj &= Q(brand_id=self.brand)
            self.products = self.products.filter(q_obj)
        self.sorts = SORT
        self.shows = SHOW
        
    def sort_filter(self, sort):
        self.products = self.products.order_by(sort)
        self.values['sort'] = sort



