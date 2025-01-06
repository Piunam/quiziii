from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .models import Quiz, Question, Choice
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib.auth.models import User

@staff_member_required
def custom_admin_dashboard(request):
    # Get basic statistics
    total_quizzes = Quiz.objects.count()
    total_questions = Question.objects.count()
    total_users = User.objects.count()
    
    # Get recent quizzes
    recent_quizzes = Quiz.objects.all().order_by('-created_at')[:5]
    
    # Get most attempted quizzes
    popular_quizzes = Quiz.objects.annotate(
        total_attempts=Count('attempts')
    ).order_by('-total_attempts')[:5]

    # Get quizzes by difficulty
    difficulty_stats = Quiz.objects.values('difficulty').annotate(
        count=Count('id')
    ).order_by('difficulty')

    # Get monthly quiz creation stats
    monthly_stats = Quiz.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Convert monthly stats to chart data
    chart_data = json.dumps(
        list(monthly_stats),
        cls=DjangoJSONEncoder
    )

    context = {
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'total_users': total_users,
        'recent_quizzes': recent_quizzes,
        'popular_quizzes': popular_quizzes,
        'difficulty_stats': difficulty_stats,
        'chart_data': chart_data,
    }

    return render(request, 'admin/dashboard.html', context)


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.question_set.all()
        return context

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        questions = quiz.question_set.all()
        score = 0
        user_answers = []
        
        # Calculate score and collect answers
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                selected_choice = Choice.objects.get(id=answer_id)
                is_correct = selected_choice.is_correct
                if is_correct:
                    score += 1
                
                user_answers.append({
                    'question_text': question.text,
                    'user_answer': selected_choice.text,
                    'correct_answer': question.choice_set.filter(is_correct=True).first().text,
                    'is_correct': is_correct
                })

        # Calculate percentage
        total_questions = len(questions)
        score_percentage = (score / total_questions) * 100 if total_questions > 0 else 0

        context = {
            'quiz': quiz,
            'score': round(score_percentage),
            'correct_answers': score,
            'total_questions': total_questions,
            'user_answers': user_answers,
        }

        return render(request, 'quiz/quiz_result.html', context)

class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/quiz_list.html'
    context_object_name = 'quizzes'


# Create your views here.
