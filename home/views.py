import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, RegisterForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile
from note.models import Note, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Note.objects.filter(status=True)[:4]
    category = Category.objects.filter(status=True)
    randomnotes = Note.objects.filter(status=True).order_by('?')[:3]
    lastnotes = Note.objects.filter(status=True).order_by('-id')[:3]
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
    category = Category.objects.filter(status=True)
    notes = Note.objects.filter(status=True)
    context = {'setting': setting,
               'category': category,
               'notes': notes,
               }
    return render(request, 'dersler.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    notes = Note.objects.filter(status=True)
    context = {'setting': setting,
               'notes': notes
               }
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
    category = Category.objects.filter(status=True)
    categorydata = Category.objects.get(pk=id)
    notes = Note.objects.filter(category_id=id)
    setting = Setting.objects.get(pk=1)
    context = {'notes': notes,
               'category': category,
               'slug': slug,
               'categorydata': categorydata,
               'setting': setting
               }
    return render(request, 'dersler.html', context)


def note_detail(request, id, slug):
    category = Category.objects.filter(status=True)
    note = Note.objects.get(pk=id)
    images = Images.objects.filter(note_id=id)
    comments = Comment.objects.filter(note_id=id, status='True')
    lastnotes = Note.objects.all().order_by('-id')[:3]
    setting = Setting.objects.get(pk=1)
    context = {'note': note,
               'category': category,
               'slug': slug,
               'images': images,
               'comments': comments,
               'lastnotes': lastnotes,
               'setting': setting
               }
    return render(request, 'note_detail.html', context)


def note_search(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.filter(status=True)
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                notes = Note.objects.filter(title__icontains=query, status=True)
            else:
                notes = Note.objects.filter(title__icontains=query, category_id=catid, status=True)
            context = {'notes': notes,
                       'category': category,
                       'setting': setting
                       }
            return render(request, 'notes_search.html', context)
        else:
            return HttpResponse(str(form.errors))
    else:
        return HttpResponseRedirect('/')


def note_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        note = Note.objects.filter(title__icontains=q, status=True)
        results = []
        for rs in note:
            note_json = {}
            note_json = rs.title
            results.append(note_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Kullanıcı ya da şifrenizi kontrol ediniz.")
            return HttpResponseRedirect('/login')
    setting = Setting.objects.get(pk=1)
    category = Category.objects.filter(status=True)
    context = {'category': category,
               'setting': setting
               }
    return render(request, 'login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "pictures/users/user.png"
            data.save()
            return HttpResponseRedirect('/')

    form = RegisterForm()
    setting = Setting.objects.get(pk=1)
    category = Category.objects.filter(status=True)
    context = {'category': category,
               'setting': setting,
               'form': form
               }
    return render(request, 'register.html', context)