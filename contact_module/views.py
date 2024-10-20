from django.shortcuts import render, redirect
from django.views import View

from .forms import ContactUsModelForm
from .models import ContactUs
from site_module.models import SiteSetting

# Create your views here.
from django.urls import reverse


class ContactUsView(View):
    def get(self, request):
        contact_form = ContactUsModelForm()
        site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
        return render(request, 'contact_module/contact_us_page.html', {
            'contact_form': contact_form,
            'site_setting': site_setting
        })

    def post(self, request):
        contact_form = ContactUsModelForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect('home-page')

        return render(request, 'contact_module/contact_us_page.html', {
            'contact_form': contact_form
        })


def contact_us_page(request):
    if request.method == 'POST':
        contact_form = ContactUsModelForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect('home-page')
    else:
        contact_form = ContactUsModelForm()

    return render(request, 'contact_module/contact_us_page.html', {
        'contact_form': contact_form
    })
