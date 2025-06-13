from django.contrib import admin
from .models import StudyMaterial, Flashcard, Quiz, ChatMessage

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'created_at', 'user']
    list_filter = ['content_type', 'created_at']
    search_fields = ['title', 'summary']
    readonly_fields = ['created_at']

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['question', 'difficulty', 'study_material', 'created_at']
    list_filter = ['difficulty', 'created_at']
    search_fields = ['question', 'answer']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'study_material', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['question', 'study_material', 'created_at']
    list_filter = ['created_at']
    search_fields = ['question', 'answer']
