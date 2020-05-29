from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from home.models import Setting, UserProfile
from note.models import Category, Comment, Note, Images
from user.forms import UserUpdateForm, ProfileUpdateForm
from user.models import NoteForm, NoteImageForm


def index(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'setting': setting,
               'profile': profile
               }
    return render(request, 'user_profile.html', context)


def user_update(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Hesabınız güncellendi.")
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {'setting': setting,
                   'category': category,
                   'user_form': user_form,
                   'profile_form': profile_form
                   }
        return render(request, 'user_update.html', context)


def change_password(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Şifreniz güncellendi.")
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, "Aşağıdaki hatayı düzelterek tekrar deneyiniz.<br>" + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form, 'category': category, 'setting': setting,
        })


@login_required(login_url='/login')
def user_comments(request):
    current_user = request.user
    notes = Note.objects.all()
    setting = Setting.objects.get(pk=1)
    comments = Comment.objects.filter(user_id=current_user.id)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               'notes': notes,
               'comments': comments
               }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, "Yorumunuz silindi.")
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def usernotes(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    usernotes = Note.objects.filter(user_id=current_user.id)
    context = {'setting': setting,
               'category': category,
               'usernotes': usernotes
               }
    return render(request, 'user_notes.html', context)


@login_required(login_url='/login')
def addnote(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            catid = form.cleaned_data['category']
            data = Note()
            data.category_id = catid.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.detail = form.cleaned_data['detail']
            data.slug = form.cleaned_data['slug']
            data.status = 'False'
            data.user_id = current_user.id
            data.save()
            messages.success(request, "Not başarıyla eklendi")
            return HttpResponseRedirect('/user/usernotes')
        else:
            messages.warning(request, "Please correct the errors: " + str(form.errors))
            return HttpResponseRedirect('/user/addnote')
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        form = NoteForm()
        context = {'setting': setting,
                   'category': category,
                   'form': form
                   }
        return render(request, 'user_addnote.html', context)


@login_required(login_url='/login')
def editnote(request, id):
    note = Note.objects.get(id=id)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Not başarıyla güncellendi")
            return HttpResponseRedirect('/user/usernotes')
        else:
            messages.warning(request, "Please correct the errors: " + str(form.errors))
            return HttpResponseRedirect('/user/editnote' + str(id))
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        form = NoteForm(instance=note)
        context = {'setting': setting,
                   'category': category,
                   'form': form
                   }
        return render(request, 'user_addnote.html', context)


@login_required(login_url='/login')
def deletenote(request, id):
    current_user = request.user
    Note.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, "Not başarıyla silindi")
    return HttpResponseRedirect('/user/usernotes')


def imageaddnote(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = NoteImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.note_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, "Resim başarıyla eklendi")
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error : ' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        setting = Setting.objects.get(pk=1)
        note = Note.objects.get(id=id)
        images = Images.objects.filter(note_id=id)
        form = NoteImageForm()
        context = {'setting': setting,
                   'note': note,
                   'images': images,
                   'form': form
                   }
        return render(request, 'note_gallery.html', context)


