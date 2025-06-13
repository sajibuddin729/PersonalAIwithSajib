from django.db import models
from django.contrib.auth.models import User
import json

class StudyMaterial(models.Model):
    CONTENT_TYPES = [
        ('pdf', 'PDF Document'),
        ('youtube', 'YouTube Video'),
        ('text', 'Text Content'),
    ]
    
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    raw_content = models.TextField()
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title

class Flashcard(models.Model):
    study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='flashcards')
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Flashcard: {self.question[:50]}..."

class Quiz(models.Model):
    study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    questions_data = models.TextField()  # JSON field for questions
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_questions(self):
        return json.loads(self.questions_data) if self.questions_data else []
    
    def set_questions(self, questions):
        self.questions_data = json.dumps(questions)
    
    def __str__(self):
        return self.title

class ChatMessage(models.Model):
    study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, related_name='chat_messages')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Q: {self.question[:50]}..."
