from django.shortcuts import render
from .models import Flashcard
from django.core import serializers
from django.http import JsonResponse

timespan = [0, 2, 3, 4, 5, 3600, 18000, 86400, 432000, 2160000, 10520000, -1]


def home(request):
    if request.method == 'POST':
        flashcard_id = request.POST['id']
        correct = request.POST['correct']
        time_cooldown = request.POST['time_cooldown']
        flashcard = Flashcard.objects.get(id=flashcard_id)
        if correct == 'true':
            index = timespan.index(int(time_cooldown))
            print("Index of timespan array: " + f'{index}')
            if index < len(timespan) - 1:
                flashcard.time_cooldown = timespan[index + 1]
        else:
            flashcard.hard_to_remember += 1
            flashcard.time_cooldown = 5
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
    # get all flashcards that have a hard_to_remember value of 10
    flashcards = Flashcard.objects.filter(user_id=request.user, hard_to_remember=10)
    context = {
        'flashcards_json': flashcards
    }
    return render(request, 'flash/hard_to_remember.html', context)

def card_admin(request):
    return render(request, 'flash/card_admin.html')

def admin_tool(request):
    all_flashcards = Flashcard.objects.all()
    for x in all_flashcards:
        x.time_cooldown = 0
        x.hard_to_remember = 0
        x.save()
    flashcards_json = serializers.serialize('json', all_flashcards)
    return render(request, 'flash/home.html', {'flashcards_json': flashcards_json})