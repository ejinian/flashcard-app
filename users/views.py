from django.shortcuts import render
from flash.models import Flashcard
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            flashcards = Flashcard.objects.all()
            context = {
                'flashcards_json': flashcards
            }
            return render(request, 'flash/card_admin.html', context)
        else:
            messages.error(request, f'Error signing up')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
