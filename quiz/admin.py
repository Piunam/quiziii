from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.shortcuts import render
from .models import Quiz, Question, Choice

# Choice Admin Inline
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    fields = ('text', 'is_correct')
    min_num = 2
    max_num = 4

# Question Admin
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'get_choices_count', 'created_at')
    list_filter = ('quiz', 'created_at')
    search_fields = ('text', 'quiz__title')
    ordering = ('quiz', 'created_at')
    inlines = [ChoiceInline]
    readonly_fields = ('created_at',)

    def get_choices_count(self, obj):
        return obj.choice_set.count()
    get_choices_count.short_description = 'Number of Choices'

# Question Inline for Quiz
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True
    fields = ('text',)
    readonly_fields = ('get_choices_count',)

    def get_choices_count(self, obj):
        if obj.id:
            return obj.choice_set.count()
        return 0
    get_choices_count.short_description = 'Choices'

# Quiz Admin
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty_badge', 'duration', 'get_questions_count', 
                   'attempts', 'is_active', 'created_at')
    list_filter = ('difficulty', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    inlines = [QuestionInline]
    readonly_fields = ('attempts', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Quiz Settings', {
            'fields': ('difficulty', 'duration', 'is_active')
        }),
        ('Statistics', {
            'fields': ('attempts', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def difficulty_badge(self, obj):
        colors = {
            'Easy': 'success',
            'Medium': 'warning',
            'Hard': 'danger'
        }
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            colors.get(obj.difficulty, 'primary'),
            obj.difficulty
        )
    difficulty_badge.short_description = 'Difficulty'

    def get_questions_count(self, obj):
        return obj.question_set.count()
    get_questions_count.short_description = 'Questions'

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new quiz
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Custom Admin Site Class
class CustomAdminSite(admin.AdminSite):
    site_header = "Quiz Administration"
    site_title = "Quiz Admin Portal"
    index_title = "Welcome to Quiz Admin Portal"

    def get_urls(self):
        urls = super().get_urls()
        from django.urls import path
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='admin_dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Get basic statistics
        total_quizzes = Quiz.objects.count()
        total_questions = Question.objects.count()
        
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
        
        context = {
            'total_quizzes': total_quizzes,
            'total_questions': total_questions,
            'recent_quizzes': recent_quizzes,
            'popular_quizzes': popular_quizzes,
            'difficulty_stats': difficulty_stats,
        }
        
        return render(request, 'admin/dashboard.html', context)

# Create custom admin site instance
custom_admin_site = CustomAdminSite(name='quiz-admin')

# Register models with custom admin site
custom_admin_site.register(Quiz, QuizAdmin)
custom_admin_site.register(Question, QuestionAdmin)

# Register models with default admin site
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)

# Default admin site customization
admin.site.site_header = "Quiz Administration"
admin.site.site_title = "Quiz Admin Portal"
admin.site.index_title = "Welcome to Quiz Admin Portal"