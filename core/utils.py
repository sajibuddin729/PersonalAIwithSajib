import PyPDF2
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import re
from urllib.parse import urlparse, parse_qs
from django.conf import settings
import json

def get_openai_client():
    """Get OpenAI client with proper error handling"""
    api_key = getattr(settings, 'OPENAI_API_KEY', None)
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in settings. Please check your .env file.")
    return OpenAI(api_key=api_key)

def extract_pdf_text(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"

def get_youtube_video_id(url):
    """Extract video ID from YouTube URL"""
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        if parsed_url.path[:7] == '/embed/':
            return parsed_url.path.split('/')[2]
        if parsed_url.path[:3] == '/v/':
            return parsed_url.path.split('/')[2]
    return None

def get_youtube_transcript(video_id):
    """Get transcript from YouTube video"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        return f"Error getting YouTube transcript: {str(e)}"

def generate_summary(content):
    """Generate summary using OpenAI"""
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise, informative summaries of educational content. Focus on key concepts, main ideas, and important details."},
                {"role": "user", "content": f"Please summarize the following content in a clear, structured way:\n\n{content[:4000]}"}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def generate_flashcards(content, num_cards=10):
    """Generate flashcards using OpenAI"""
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates educational flashcards. Create clear, concise questions and answers that test understanding of key concepts. Return the response as a JSON array of objects with 'question', 'answer', and 'difficulty' fields."},
                {"role": "user", "content": f"Create {num_cards} flashcards from this content:\n\n{content[:3000]}"}
            ],
            max_tokens=1500,
            temperature=0.4
        )
        
        flashcards_text = response.choices[0].message.content
        # Try to parse JSON, fallback to manual parsing if needed
        try:
            return json.loads(flashcards_text)
        except:
            # Manual parsing fallback
            return parse_flashcards_manually(flashcards_text)
    except Exception as e:
        return [{"question": f"Error generating flashcards: {str(e)}", "answer": "Please try again", "difficulty": "easy"}]

def generate_quiz(content, num_questions=5):
    """Generate quiz questions using OpenAI"""
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates educational quizzes. Create multiple choice questions with 4 options each. Return as JSON array with 'question', 'options' (array), 'correct_answer' (index), and 'explanation' fields."},
                {"role": "user", "content": f"Create {num_questions} multiple choice quiz questions from this content:\n\n{content[:3000]}"}
            ],
            max_tokens=1500,
            temperature=0.4
        )
        
        quiz_text = response.choices[0].message.content
        try:
            return json.loads(quiz_text)
        except:
            return parse_quiz_manually(quiz_text)
    except Exception as e:
        return [{"question": f"Error generating quiz: {str(e)}", "options": ["Try again", "Check connection", "Verify API key", "Contact support"], "correct_answer": 0, "explanation": "Please try again"}]

def answer_question(content, question):
    """Answer question based on content using OpenAI"""
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant. Answer questions based on the provided content. Be accurate, informative, and cite specific parts of the content when possible."},
                {"role": "user", "content": f"Based on this content:\n\n{content[:3000]}\n\nQuestion: {question}"}
            ],
            max_tokens=800,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error answering question: {str(e)}"

def parse_flashcards_manually(text):
    """Fallback parser for flashcards"""
    flashcards = []
    lines = text.split('\n')
    current_card = {}
    
    for line in lines:
        if 'question' in line.lower() or 'q:' in line.lower():
            if current_card:
                flashcards.append(current_card)
            current_card = {'question': line.split(':', 1)[-1].strip(), 'difficulty': 'medium'}
        elif 'answer' in line.lower() or 'a:' in line.lower():
            current_card['answer'] = line.split(':', 1)[-1].strip()
    
    if current_card:
        flashcards.append(current_card)
    
    return flashcards[:10]  # Limit to 10 cards

def parse_quiz_manually(text):
    """Fallback parser for quiz questions"""
    questions = []
    # Simple fallback - create basic questions
    questions.append({
        "question": "What is the main topic of this content?",
        "options": ["Topic A", "Topic B", "Topic C", "Topic D"],
        "correct_answer": 0,
        "explanation": "Based on the content analysis"
    })
    return questions
