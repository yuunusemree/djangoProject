from django.contrib import admin
from note.models import Category, Note, Images

# Register your models here.

class NoteImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status']
    list_filter = ['status', 'category']
    inlines = [NoteImageInline]


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'note', 'title']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Images, ImagesAdmin)
