from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    tasks = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Note
        fields = ['content', 'tasks']