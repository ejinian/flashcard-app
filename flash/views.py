from django.shortcuts import render, redirect
from .models import Flashcard
from django.core import serializers
from django.http import JsonResponse

timespan = {
    'bin0': 0,
    'bin1': 2,
    'bin2': 3,
    'bin3': 4,
    'bin4': 5,
    'bin5': 3600,
    'bin6': 18000,
    'bin7': 86400,
    'bin8': 432000,
    'bin9': 2160000,
    'bin10': 10520000,
    'bin11': -1,
}


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        flashcard_id = request.POST['id']
        correct = request.POST['correct']
        time_cooldown = request.POST['time_cooldown']
        current_bin = request.POST['current_bin']
        flashcard = Flashcard.objects.get(id=flashcard_id)
        if correct == 'true':
            nextBin = 'bin' + str(int(current_bin[-1]) + 1)
            flashcard.time_cooldown = timespan[nextBin]
            flashcard.current_bin = nextBin
            if flashcard.time_cooldown == -1:
                flashcard.current_bin = 'bin11'
        else:
            flashcard.hard_to_remember += 1
            flashcard.time_cooldown = 5
            flashcard.current_bin = 'bin1'
        flashcard.save()
        print(f'Flashcard_id: {flashcard_id}' + f' Has new cooldown: {flashcard.time_cooldown}')
        sendBack = {
            'flashcard_id': flashcard_id,
            'time_cooldown': flashcard.time_cooldown,
            'question': flashcard.question,
            'answer': flashcard.answer
        }
        return JsonResponse(sendBack)
    
    flashcards = Flashcard.objects.filter(user_id=request.user)\
        .exclude(time_cooldown=-1).exclude(hard_to_remember=10).order_by('time_cooldown')
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
        context = {
            'flashcard': flashcard
        }
        return render(request, 'flash/card_admin_update.html', context)

def admin_tool(request):
    # tool to clear all cooldowns and hard_to_remember values
    all_flashcards = Flashcard.objects.all()
    for x in all_flashcards:
        x.time_cooldown = 0
        x.hard_to_remember = 0
        x.current_bin = 'bin0'
        x.save()
    flashcards_json = serializers.serialize('json', all_flashcards)
    return render(request, 'flash/home.html', {'flashcards_json': flashcards_json})