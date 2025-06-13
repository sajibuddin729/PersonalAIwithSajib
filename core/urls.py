from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_content, name='upload_content'),
    path('material/<int:pk>/', views.material_detail, name='material_detail'),
    path('material/<int:pk>/generate/', views.generate_study_materials, name='generate_study_materials'),
    path('material/<int:pk>/ask/', views.ask_question, name='ask_question'),
    path('material/<int:pk>/flashcards/', views.flashcards_view, name='flashcards'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('material/<int:pk>/chart-data/', views.summary_chart_data, name='summary_chart_data'),
]
