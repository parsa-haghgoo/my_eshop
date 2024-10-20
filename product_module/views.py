from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .forms import SearchForm

from site_module.models import SiteSetting
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery, ProductComment
from django.http import HttpRequest


def group_list(custom_list, size=4):
    grouped_list = []
    for i in range(0, len(custom_list), size):
        grouped_list.append(custom_list[i:i + size])
    return grouped_list


def get_client_ip(request: HttpRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    form_class = SearchForm
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 6

    def get_queryset(self):
        query = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            query = Product.objects.filter(title__contains=form.cleaned_data['title'])
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the search form to the context
        context['search_form'] = SearchForm(self.request.GET)
        return context


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_queryset(self):
        query = super(ProductDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product: Product = kwargs.get('object')
        loaded_product = self.object
        context['comments'] = ProductComment.objects.filter(product_id=product.id).order_by(
            '-create_date')
        request = self.request
        context['related_products'] = group_list(
            list(Product.objects.filter(brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12]), 3)
        context['product_galleries_group'] = group_list(
            list(ProductGallery.objects.filter(product_id=loaded_product.id).all()), 3)
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()

        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        return context


def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/components/product_brands_component.html', context)


def add_product_comment(request: HttpRequest):
    if request.user.is_authenticated:
        product_id = request.GET.get('product_id')
        product_comment = request.GET.get('product_comment')
        print(product_id, product_comment)
        new_comment = ProductComment(product_id=product_id, text=product_comment, user_id=request.user.id)
        new_comment.save()

    return HttpResponse('response')


def product_site_layout(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting
    }
    return render(request, 'product_module/base/layout.html', context)
