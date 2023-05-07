from django.contrib import admin

from .models import Flashcard
# Register your models here.

class FlashcardAdmin(admin.ModelAdmin):
    readonly_fields = ['last_bin_change']

admin.site.register(Flashcard, FlashcardAdmin)