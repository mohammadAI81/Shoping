from django.core.paginator import Paginator
from django.db.models import Q, Count
from django_unicorn.components import UnicornView

from ..models import Product, Color, Category, Brand
from ..variable import SHOW, SORT


class ListproductctegoryView(UnicornView):
    color, brand, page_obj = '', '', ''
    sorts = SORT
    shows = SHOW
    categories = Category.objects.none()
    brands = Brand.objects.none()
    colors = Color.objects.none()
    products = Product.objects.none()
    products_init = Product.objects.none()
    values = {'sort': SORT[0][0], 'show': SHOW[0]}

    def mount(self):
        """
        Return Init Product
        """
        self.categories = Category.objects.all()
        self.brands = Brand.objects.all()
        self.colors = Color.objects.all()
        self.products_init = Product.objects.select_related('category', 'color', 'brand')
        # Filter Of Category
        if self.request.GET:
            category_id = self.request.GET.get('category')
            if category_id != '0':
                self.products_init = self.products_init.filter(category_id=category_id)
        self.products = self.products_init
        self.sort_filter(sort=self.values.get('sort'))
        self.show_filter(self.values.get('show'))

        return self.products

    def product_filter(self):
        # Filter Of Color & Brand
        if self.color or self.brand:
            q_obj = Q()
            if self.color:
                q_obj &= Q(color_id=self.color)
            if self.brand:
                q_obj &= Q(brand_id=self.brand)
            self.products_init = self.products_init.filter(q_obj)
        self.products = self.products_init
        self.sorts = SORT
        self.shows = SHOW

    # Sort Product
    def sort_filter(self, sort):
        self.product_filter()
        self.products_init = self.products_init.order_by(sort)
        self.values['sort'] = sort
        self.products = self.products_init

    # Pagination Product
    def show_filter(self, show, page_num=1):
        self.product_filter()
        self.sort_filter(sort=self.values.get('sort'))
        if show == SHOW[-1]:
            self.products = self.products_init
            self.page_obj = None
        else:
            paginator = Paginator(self.products_init, show)
            page_obj = paginator.get_page(page_num)
            products = page_obj.object_list
            list_product_id = []
            for product in products:
                list_product_id.append(product.id)
            self.products = self.products_init.filter(id__in=list_product_id)

            self.page_obj = {
                'has_other_pages': page_obj.has_other_pages(),
                'has_previous': page_obj.has_previous(),
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'has_next': page_obj.has_next(),
                'number': page_obj.number,
                'page_range': list(paginator.page_range),
                'num_page': page_obj.paginator.num_pages
            }
        self.values['show'] = show

