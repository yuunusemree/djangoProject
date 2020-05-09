from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from home.models import Setting, UserProfile


def index(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'setting': setting,
               'profile': profile
               }
    return render(request, 'user_profile.html', context)
