from ckeditor.widgets import CKEditorWidget
from django.db import models
from django.forms import ModelForm, Select, TextInput, FileInput

from note.models import Note, Category, Images


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['category', 'title', 'keywords', 'description', 'image', 'detail', 'slug']
        widgets = {
            'category': Select(attrs={'class': 'comment_input', 'placeholder': 'category'}, choices=Category.objects.all()),
            'title': TextInput(attrs={'class': 'comment_input', 'placeholder': 'title'}),
            'keywords': TextInput(attrs={'class': 'comment_input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'comment_input', 'placeholder': 'description'}),
            'image': FileInput(attrs={'class': 'fileinput', 'placeholder': 'image'}),
            'detail': CKEditorWidget(),
            'slug': TextInput(attrs={'class': 'comment_input', 'placeholder': 'slug'}),
        }


class NoteImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'image']