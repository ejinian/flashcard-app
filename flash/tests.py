from django.test import TestCase
from django.contrib.auth.models import User
from .models import Flashcard
# import any python api libraries here
import requests

# Create your tests here.
word1 = "ocean"
word2 = "mountain"
word3 = "forest"

class FlashcardTestManual(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.flashcard = Flashcard.objects.create(question='test question', answer='test answer', user_id=self.user)
    
    def test_flashcard_creation(self):
        self.assertEqual(self.flashcard.question, 'test question')
        self.assertEqual(self.flashcard.answer, 'test answer')
        self.assertEqual(self.flashcard.hard_to_remember, 0)
        self.assertEqual(self.flashcard.time_cooldown, 0)
        self.assertEqual(self.flashcard.current_bin, '0')
        self.assertEqual(self.flashcard.last_bin_change, '2000-01-01 00:00:00.000000+00:00')
        self.assertEqual(self.flashcard.user_id, self.user)

    def test_flashcard_update(self):
        self.flashcard.question = 'updated question'
        self.flashcard.answer = 'updated answer'
        self.flashcard.hard_to_remember = 1
        self.flashcard.time_cooldown = 5
        self.flashcard.current_bin = '1'
        self.flashcard.last_bin_change = '2001-01-01 00:00:00.000000+00:00'
        self.flashcard.save()
        self.assertEqual(self.flashcard.question, 'updated question')
        self.assertEqual(self.flashcard.answer, 'updated answer')
        self.assertEqual(self.flashcard.hard_to_remember, 1)
        self.assertEqual(self.flashcard.time_cooldown, 5)
        self.assertEqual(self.flashcard.current_bin, '1')
        self.assertEqual(self.flashcard.last_bin_change, '2001-01-01 00:00:00.000000+00:00')
        self.assertEqual(self.flashcard.user_id, self.user)

    def test_flashcard_delete(self):
        flashcard_count = Flashcard.objects.count()
        self.flashcard.delete()
        self.assertEqual(Flashcard.objects.count(), flashcard_count - 1)

class FlashcardTestAPI(TestCase):
    def setUp(self):
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word1}')
        response2 = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word2}')
        response3 = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word3}')
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        question = response.json()[0]['word']
        answer = response.json()[0]['meanings'][0]['definitions'][0]['definition']
        self.flashcard1 = Flashcard.objects.create(question=question, answer=answer, user_id=self.user)
        question = response2.json()[0]['word']
        answer = response2.json()[0]['meanings'][0]['definitions'][0]['definition']
        self.flashcard2 = Flashcard.objects.create(question=question, answer=answer, user_id=self.user)
        question = response3.json()[0]['word']
        answer = response3.json()[0]['meanings'][0]['definitions'][0]['definition']
        self.flashcard3 = Flashcard.objects.create(question=question, answer=answer, user_id=self.user)
    
    def test_flashcard_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302) # should be a redirect to login page
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/card_admin')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['flashcards']), 3)
        response = self.client.get(f'/card_admin_update/{self.flashcard1.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['flashcard'].question, self.flashcard1.question)
        self.assertEqual(response.context['flashcard'].answer, self.flashcard1.answer)
        response = self.client.get(f'/card_admin_update/{self.flashcard2.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['flashcard'].question, self.flashcard2.question)
        self.assertEqual(response.context['flashcard'].answer, self.flashcard2.answer)
        self.assertEqual(response.context['flashcard'].user_id, self.user)
        self.assertEqual(self.flashcard1.question, word1)
        self.assertEqual(self.flashcard2.question, word2)
        self.assertEqual(self.flashcard3.question, word3)

    def test_flashcard_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/card_admin_update/1/', {'question': 'updated question', 'answer': 'updated answer'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Flashcard.objects.get(id=1).question, 'updated question')
        self.assertEqual(Flashcard.objects.get(id=1).answer, 'updated answer')
        response = self.client.post('/card_admin_update/2/', {'question': 'updated question', 'answer': 'updated answer'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Flashcard.objects.get(id=2).question, 'updated question')
        self.assertEqual(Flashcard.objects.get(id=2).answer, 'updated answer')
        response = self.client.post('/card_admin_update/3/', {'question': 'updated question', 'answer': 'updated answer'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Flashcard.objects.get(id=3).question, 'updated question')
        self.assertEqual(Flashcard.objects.get(id=3).answer, 'updated answer')
        self.assertEqual(Flashcard.objects.get(id=1).question, Flashcard.objects.get(id=2).question)
        self.assertEqual(Flashcard.objects.get(id=1).question, Flashcard.objects.get(id=3).question)
        self.assertEqual(Flashcard.objects.get(id=1).answer, Flashcard.objects.get(id=2).answer)
        self.assertEqual(Flashcard.objects.get(id=1).answer, Flashcard.objects.get(id=3).answer)

    def test_flashcard_delete(self):
        self.client.login(username='testuser', password='12345')
        self.flashcard1.delete()
        self.assertEqual(Flashcard.objects.count(), 2)