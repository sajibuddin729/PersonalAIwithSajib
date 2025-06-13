from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
from .models import StudyMaterial, Flashcard, Quiz, ChatMessage
from .utils import (
    extract_pdf_text, get_youtube_video_id, get_youtube_transcript,
    generate_summary, generate_flashcards, generate_quiz, answer_question
)

def home(request):
    """Home page with upload form"""
    recent_materials = StudyMaterial.objects.all().order_by('-created_at')[:5]
    return render(request, 'core/home.html', {'recent_materials': recent_materials})

def upload_content(request):
    """Handle content upload and processing"""
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled')
        content_type = request.POST.get('content_type')
        
        study_material = StudyMaterial.objects.create(
            title=title,
            content_type=content_type,
            user=request.user if request.user.is_authenticated else None
        )
        
        try:
            if content_type == 'pdf' and 'file' in request.FILES:
                # Handle PDF upload
                uploaded_file = request.FILES['file']
                study_material.file = uploaded_file
                study_material.save()
                
                # Extract text from PDF
                file_path = study_material.file.path
                raw_content = extract_pdf_text(file_path)
                study_material.raw_content = raw_content
                
            elif content_type == 'youtube':
                # Handle YouTube URL
                youtube_url = request.POST.get('youtube_url')
                study_material.youtube_url = youtube_url
                
                # Extract video ID and get transcript
                video_id = get_youtube_video_id(youtube_url)
                if video_id:
                    raw_content = get_youtube_transcript(video_id)
                    study_material.raw_content = raw_content
                else:
                    raise Exception("Invalid YouTube URL")
                    
            elif content_type == 'text':
                # Handle direct text input
                raw_content = request.POST.get('text_content', '')
                study_material.raw_content = raw_content
            
            # Generate summary
            if study_material.raw_content:
                summary = generate_summary(study_material.raw_content)
                study_material.summary = summary
                study_material.save()
                
                messages.success(request, f'Content "{title}" uploaded and processed successfully!')
                return redirect('material_detail', pk=study_material.pk)
            else:
                raise Exception("No content could be extracted")
                
        except Exception as e:
            study_material.delete()
            messages.error(request, f'Error processing content: {str(e)}')
            return redirect('home')
    
    return redirect('home')

def material_detail(request, pk):
    """Display study material details"""
    material = get_object_or_404(StudyMaterial, pk=pk)
    flashcards = material.flashcards.all()
    quizzes = material.quizzes.all()
    chat_messages = material.chat_messages.all().order_by('-created_at')[:10]
    
    context = {
        'material': material,
        'flashcards': flashcards,
        'quizzes': quizzes,
        'chat_messages': chat_messages,
    }
    return render(request, 'core/material_detail.html', context)

def generate_study_materials(request, pk):
    """Generate flashcards and quiz for study material"""
    material = get_object_or_404(StudyMaterial, pk=pk)
    
    try:
        # Generate flashcards
        flashcards_data = generate_flashcards(material.raw_content)
        for card_data in flashcards_data:
            Flashcard.objects.create(
                study_material=material,
                question=card_data.get('question', ''),
                answer=card_data.get('answer', ''),
                difficulty=card_data.get('difficulty', 'medium')
            )
        
        # Generate quiz
        quiz_data = generate_quiz(material.raw_content)
        quiz = Quiz.objects.create(
            study_material=material,
            title=f"Quiz: {material.title}"
        )
        quiz.set_questions(quiz_data)
        quiz.save()
        
        messages.success(request, 'Study materials generated successfully!')
        
    except Exception as e:
        messages.error(request, f'Error generating study materials: {str(e)}')
    
    return redirect('material_detail', pk=pk)

@csrf_exempt
@require_http_methods(["POST"])
def ask_question(request, pk):
    """Handle Q&A for study material"""
    material = get_object_or_404(StudyMaterial, pk=pk)
    
    try:
        data = json.loads(request.body)
        question = data.get('question', '')
        
        if not question:
            return JsonResponse({'error': 'Question is required'}, status=400)
        
        # Generate answer using AI
        answer = answer_question(material.raw_content, question)
        
        # Save chat message
        chat_message = ChatMessage.objects.create(
            study_material=material,
            question=question,
            answer=answer
        )
        
        return JsonResponse({
            'answer': answer,
            'timestamp': chat_message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def quiz_detail(request, pk):
    """Display quiz"""
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.get_questions()
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'material': quiz.study_material
    }
    return render(request, 'core/quiz_detail.html', context)

def flashcards_view(request, pk):
    """Display flashcards"""
    material = get_object_or_404(StudyMaterial, pk=pk)
    flashcards = material.flashcards.all()
    
    context = {
        'material': material,
        'flashcards': flashcards
    }
    return render(request, 'core/flashcards.html', context)

def summary_chart_data(request, pk):
    """Provide data for summary visualization"""
    material = get_object_or_404(StudyMaterial, pk=pk)
    
    # Simple word frequency analysis for chart
    words = material.summary.lower().split()
    word_freq = {}
    
    # Filter common words and count frequency
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
    
    for word in words:
        clean_word = ''.join(c for c in word if c.isalnum())
        if len(clean_word) > 3 and clean_word not in common_words:
            word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
    
    # Get top 10 words
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
    chart_data = {
        'labels': [word[0] for word in top_words],
        'data': [word[1] for word in top_words]
    }
    
    return JsonResponse(chart_data)
