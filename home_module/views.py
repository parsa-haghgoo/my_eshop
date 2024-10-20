from django.shortcuts import render
from django.db.models import Count
from django.views.generic.base import TemplateView
from site_module.models import SiteSetting, FooterLinkBox, Slider
from product_module.models import Product


def group_list(custom_list, size=4):
    grouped_list = []
    for i in range(0, len(custom_list), size):
        grouped_list.append(custom_list[i:i + size])
    return grouped_list


class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        most_visit_products = Product.objects.filter(is_active=True, is_delete=False).annotate(visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        multi_sell_product = Product.objects.filter(is_active=True, is_delete=False, is_mulltiselling=True)[:12]
        context['latest_products'] = group_list(latest_products)
        context['most_visit_products'] = group_list(most_visit_products)
        context['multi_sell_product'] = group_list(multi_sell_product)
        return context


def site_header_component(request):

    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    for item in footer_link_boxes:
        item.footerlink_set
    context = {
        'site_setting': setting,
        'footer_link_boxes': footer_link_boxes
    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context
