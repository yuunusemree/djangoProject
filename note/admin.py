from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from note.models import Category, Note, Images, Comment


# Register your models here.

class NoteImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_notes_count', 'related_notes_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Note,
                'category',
                'notes_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Note,
                 'category',
                 'notes_count',
                 cumulative=False)
        return qs

    def related_notes_count(self, instance):
        return instance.notes_count
    related_notes_count.short_description = 'Related notes (for this specific category)'

    def related_notes_cumulative_count(self, instance):
        return instance.notes_cumulative_count
    related_notes_cumulative_count.short_description = 'Related notes (in tree)'


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'status']
    list_filter = ['status', 'category']
    inlines = [NoteImageInline]
    readonly_fields = ('image_tag', 'user')
    prepopulated_fields = {'slug': ('title',)}


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'note', 'image_tag']
    readonly_fields = ('note', 'title', 'image', 'image_tag')


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'note', 'user', 'status']
    list_filter = ['status']
    readonly_fields = ('note', 'user', 'subject', 'comment', 'rate', 'ip')


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Note, NoteAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment, CommentAdmin)
