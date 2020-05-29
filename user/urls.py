from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('usernotes/', views.usernotes, name='usernotes'),
    path('addnote/', views.addnote, name='addnote'),
    path('editnote/<int:id>', views.editnote, name='editnote'),
    path('deletenote/<int:id>', views.deletenote, name='deletenote'),
    path('imageaddnote/<int:id>', views.imageaddnote, name='imageaddnote')
    # ex: /home/5/
    # path('<int:question_id>/', views.detail, name='detail'),
]