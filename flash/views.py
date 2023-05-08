from django.shortcuts import render, redirect
from .models import Flashcard
from django.core import serializers
from django.http import JsonResponse
from datetime import datetime, timezone

timespan = {
    '0': 0,
    '1': 5,
    '2': 25,
    '3': 120,
    '4': 600,
    '5': 3600,
    '6': 18000,
    '7': 86400,
    '8': 432000,
    '9': 2160000,
    '10': 10520000,
    '11': 99999999
}

def updateTimes(user):
    # this function allows for synchronization of time_cooldown between the db and frontend
    # creates the illusion that the timer of each flashcard is ticking on the backend
    flashcards = Flashcard.objects.filter(user_id=user)
    # keeping all time in UTC
    current_time = datetime.now(timezone.utc)
    print(f'Current time: {current_time}')
    for flashcard in flashcards:
        time_passed = current_time - flashcard.last_bin_change
        print('time_passed: ' + str(time_passed))
        cooldown_in_seconds = timespan[flashcard.current_bin] - time_passed.total_seconds()
        if cooldown_in_seconds < 0:
            cooldown_in_seconds = 0
        flashcard.time_cooldown = cooldown_in_seconds
        flashcard.save()
    return


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    updateTimes(request.user)
    if request.method == 'POST':
        flashcard_id = request.POST['id']
        correct = request.POST['correct']
        current_bin = request.POST['current_bin']
        flashcard = Flashcard.objects.get(id=flashcard_id)
        if correct == 'true': # ajax sending strings
            nextBin = str(int(current_bin) + 1)
            if flashcard.current_bin == '11':
                nextBin = '11'
            flashcard.time_cooldown = timespan[nextBin]
            flashcard.current_bin = nextBin
        else:
            flashcard.hard_to_remember += 1
            flashcard.time_cooldown = 5
            flashcard.current_bin = '1'
        flashcard.last_bin_change = datetime.now(timezone.utc)
        flashcard.save()
        print(f'Flashcard_id: {flashcard_id}' + f' Has new bin: {flashcard.current_bin}')
        sendBack = {
            'flashcard_id': flashcard_id,
            'time_cooldown': flashcard.time_cooldown,
            'question': flashcard.question,
            'answer': flashcard.answer
        }
        return JsonResponse(sendBack)
    
    # get all flashcards that are not in the last bin or hard to remember==10
    flashcards = Flashcard.objects.filter(user_id=request.user)\
        .exclude(current_bin='11').exclude(hard_to_remember=10).order_by('time_cooldown')
    # serializing so that it is easier to parse on the frontend
    flashcards_json = serializers.serialize('json', flashcards)
    context = {
        'flashcards_json': flashcards_json
    }
    return render(request, 'flash/home.html', context)

def hard_to_remember(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # get all flashcards that have a hard_to_remember value of 10
    flashcards = Flashcard.objects.filter(user_id=request.user, hard_to_remember=10)
    context = {
        'flashcards_json': flashcards
    }
    return render(request, 'flash/hard_to_remember.html', context)

def card_admin(request):
    # read
    if not request.user.is_authenticated:
        return redirect('login')
    updateTimes(request.user)
    flashcards = Flashcard.objects.filter(user_id=request.user)
    context = {
        'flashcards': flashcards
    }
    return render(request, 'flash/card_admin.html', context)

def card_admin_create(request):
    # create
    if request.method == 'POST':
        question = request.POST['question']
        answer = request.POST['answer']
        flashcard = Flashcard(question=question, answer=answer, user_id=request.user)
        flashcard.save()
        return JsonResponse({'flashcard_id': flashcard.id})
    return JsonResponse({'flashcard_id': -1})

def card_admin_delete(request):
    # delete
    if request.method == 'POST':
        flashcard_id = request.POST['flashcard_id']
        flashcard = Flashcard.objects.get(id=flashcard_id)
        flashcard.delete()
        return JsonResponse({'flashcard_id': flashcard_id})
    return JsonResponse({'flashcard_id': -1})

def card_admin_update(request, pk):
    # update
    flashcard = Flashcard.objects.get(id=pk)
    flashcards = Flashcard.objects.filter(user_id=request.user)
    if request.method == 'POST':
        question = request.POST['question']
        answer = request.POST['answer']
        flashcard.question = question
        flashcard.answer = answer
        flashcard.save()
        return render(request, 'flash/card_admin.html', {'flashcards': flashcards})
    else:
        return render(request, 'flash/card_admin_update.html', {'flashcard': flashcard})

def admin_tool(request):
    # nice tool to clear all cooldowns, bin, and hard_to_remember values
    # -------not needed in production-------
    if not request.user.is_authenticated:
        return redirect('login')
    all_flashcards = Flashcard.objects.all()
    flashcards = Flashcard.objects.filter(user_id=request.user)
    for x in all_flashcards:
        x.time_cooldown = 0
        x.hard_to_remember = 0
        x.current_bin = '0'
        x.save()
    flashcards_json = serializers.serialize('json', flashcards)
    return render(request, 'flash/home.html', {'flashcards_json': flashcards})
