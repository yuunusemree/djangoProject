from django.contrib import admin
from note.models import Category, Note, Images

# Register your models here.

class NoteImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'status']
    list_filter = ['status', 'category']
    inlines = [NoteImageInline]
    readonly_fields = ('image_tag',)


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'note', 'image_tag']
    readonly_fields = ('image_tag',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Images, ImagesAdmin)
