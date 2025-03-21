from django.shortcuts import render, redirect
from habar.models import Habar, Bolim, Sponsor, Contact
import datetime
from habar.forms import ContactForm
from django.contrib import messages

def get_date():
    return datetime.datetime.today()

def get_category():
    return Bolim.objects.all()

def index(r):
    context = {
        'habar':Habar.objects.all().order_by('-date'),
        'habar2':Habar.objects.all().order_by('-view'),
        'bolim':Bolim.objects.all(),  
        'sponsor':Sponsor.objects.all(),  
        'uzb': Habar.objects.filter(bolim__name="O'zbekiston").order_by('-date'),
        'jah': Habar.objects.filter(bolim__name="Jahon").order_by('-date'),
        'iqt': Habar.objects.filter(bolim__name="Iqtisodiyot").order_by('-date'),
        'spo': Habar.objects.filter(bolim__name="Sport").order_by('-date'),
        'date': get_date(),

    }
    return render(r, template_name='index.html', context=context)

def about(r):
    context = {
        'habar2':Habar.objects.all().order_by('-view'),
        'habar':Habar.objects.all().order_by('-date'),
        'bolim':Bolim.objects.all(),  
        'sponsor':Sponsor.objects.all(),
        'date': get_date(),

    }
    return render(r, template_name='404.html', context=context)


def detail(request, pk):
    habar0 = Habar.objects.get(pk=pk)
    habarlar = Habar.objects.filter(bolim=habar0.bolim).exclude(id=habar0.id).order_by('-date')
    popular_news = Habar.objects.all().exclude(id=habar0.id).order_by('-view')
    sponsor = Sponsor.objects.all()
    habar0.view += 1
    habar0.save()
    context = {
        'ctg': get_category(),
        'habar0': habar0,
        'habarlar': habarlar[:3],
        'popular_news': popular_news[:6],
        'date': get_date(),
        'sponsor': sponsor,
        'habar':Habar.objects.all().order_by('-date'),
        'bolim':Bolim.objects.all(),
    }
    return render(request, 'single_page.html', context)

def contact(r):
    context = {
        'habar2':Habar.objects.all().order_by('-view'),
        'habar':Habar.objects.all().order_by('-date'),
        'bolim':Bolim.objects.all(),  
        'sponsor':Sponsor.objects.all(),
        'date': get_date(),

    }
    return render(r, template_name='contact.html', context=context)

def contact(request):
    habar = Habar.objects.all().order_by('-date')
    habar2 = Habar.objects.all().order_by('-view')
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message shuu ketti..")
            return redirect('contact')

    else:
        form = ContactForm()
    context = {
        'bolim': get_category(),
        'habar': habar,
        'habar2': habar2[:6],
        'date': get_date(),
        'form': form,
    }
    return render(request, 'contact.html', context)

def category_detail(request, pk):
    bolim0 = Bolim.objects.get(id=pk)
    habarlar = Habar.objects.filter(bolim=bolim0.id ).order_by('-date')
    habar = Habar.objects.order_by('-date')
    print( bolim0.name)
    context = {
        'bolim': get_category(),
        'habarlar': habarlar,
        'date': get_date(),
        'bolim0': bolim0,
        'habar':habar,
    }
    return render(request, 'category.html', context)