from django.contrib import admin
from note.models import Category, Note


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status']
    list_filter = ['status', 'category']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Note, NoteAdmin)