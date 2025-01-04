from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .models import Quiz, Question, Choice



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
