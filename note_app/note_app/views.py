from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import NoteForm
from .models import Note
from django.shortcuts import render, redirect
from .models import Task
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

def ma_vue(request):
    return render(request, 'ma_vue.html')
@login_required
def create_note(request):
    return render(request, 'create_note.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            for key, task_content in request.POST.items():
                if key.startswith('task-') and task_content:  # Ignore les tâches vides
                    Task.objects.create(note=note, content=task_content)
            return redirect('view_notes')
    else:
        form = NoteForm()

    return render(request, 'create_note.html', {'form': form})

def view_notes(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'view_notes.html', {'notes': notes})

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            for key, task_content in request.POST.items():
                if key.startswith('task-'):
                    task_id = key.split('-')[1]
                    if task_content:  # if task content is not empty, create or update the task
                        Task.objects.update_or_create(id=task_id, defaults={'content': task_content, 'note': note})
                elif key.startswith('task-delete-'):
                    task_id = key.split('-')[2]
                    if task_content == 'true':  # if task is marked for deletion, delete the task
                        Task.objects.filter(id=task_id).delete()
            return redirect('view_notes')
    else:
        form = NoteForm(instance=note)
    return render(request, 'edit_note.html', {'form': form, 'note': note})


def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('view_notes')

def toggle_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'completed': task.completed})

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return HttpResponseRedirect(reverse('view_notes'))