from django.shortcuts import render
from habar.models import Habar, Bolim, Sponsor

def index(r):
    context = {
        'habar':Habar.objects.all(),
        'bolim':Bolim.objects.all(),  
        'sponsor':Sponsor.objects.all(),  
        'uzb': Habar.objects.filter(bolim__name="O'zbekiston").order_by('-date'),
        'jah': Habar.objects.filter(bolim__name="Jahon").order_by('-date'),
        'iqt': Habar.objects.filter(bolim__name="Iqtisodiyot").order_by('-date'),
        'spo': Habar.objects.filter(bolim__name="Sport").order_by('-date'),

    }
    return render(r, template_name='index.html', context=context)

def single_page(r):
    return render(r, template_name='single_page.html')

def contact(r):
    return render(r, template_name='contact.html')

def error(r):
    return render(r, template_name='404.html')