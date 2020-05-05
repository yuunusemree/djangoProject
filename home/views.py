from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactFormu, ContactFormMessage
from note.models import Note, Category, Images


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Note.objects.all()[:4]
    category = Category.objects.all()
    randomnotes = Note.objects.all().order_by('?')[:3]
    lastnotes = Note.objects.all().order_by('-id')[:3]
    context = {'setting': setting,
               'category': category,
               'sliderdata': sliderdata,
               'randomnotes': randomnotes,
               'lastnotes': lastnotes,
               'page': 'home'
               }
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'hakkimizda.html', context)


def dersler(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all().order_by('parent_id')
    notes = Note.objects.all()
    context = {'setting': setting,
               'category': category,
               'notes': notes,
               }
    return render(request, 'dersler.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'referanslarimiz.html', context)


def iletisim(request):
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız alınmıştır. Teşekkürler.")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting,
               'form': form}
    return render(request, 'iletisim.html', context)


def category_notes(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    notes = Note.objects.filter(category_id=id)
    context = {'notes': notes,
               'category': category,
               'slug': slug,
               'categorydata': categorydata
               }
    return render(request, 'dersler.html', context)


def note_detail(request, id, slug):
    category = Category.objects.all()
    note = Note.objects.get(pk=id)
    images = Images.objects.filter(note_id=id)
    lastnotes = Note.objects.all().order_by('-id')[:3]
    context = {'note': note,
               'category': category,
               'slug': slug,
               'images': images,
               'lastnotes': lastnotes
               }
    return render(request, 'note_detail.html', context)


def note_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all
            query = form.cleaned_data['query']
            notes = Note.objects.filter(title__icontains=query)
            context = {'notes': notes,
                       'category': category
                       }
            return render(request, 'notes_search.html', context)
    return HttpResponseRedirect('/')