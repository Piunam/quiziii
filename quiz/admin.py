# from django.contrib import admin
# from .models import Quiz, Question, Choice

# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

# class QuestionAdmin(admin.ModelAdmin):
#     inlines = [ChoiceInline]

# class QuestionInline(admin.TabularInline):
#     model = Question
#     extra = 1

# class QuizAdmin(admin.ModelAdmin):
#     inlines = [QuestionInline]

# admin.site.register(Quiz, QuizAdmin)
# admin.site.register(Question, QuestionAdmin)
# # Register your models here.


from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Quiz, Question, Choice

# Choice Admin Inline
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    fields = ('text', 'is_correct')
    min_num = 2  # Minimum number of choices required
    max_num = 4  # Maximum number of choices allowed

# Question Admin
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'get_choices_count', 'created_at')
    list_filter = ('quiz', 'created_at')
    search_fields = ('text', 'quiz__title')
    ordering = ('quiz', 'created_at')
    inlines = [ChoiceInline]
    # readonly_fields = ('created_at',)

    def get_choices_count(self, obj):
        return obj.choice_set.count()
    get_choices_count.short_description = 'Number of Choices'

# Question Inline for Quiz
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True
    fields = ('text',  'quiz',)
    # readonly_fields = ('get_choices_count',)

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
        # return format_html(
        #     '<span class="badge badge-{}">{}</span>',
        #     colors.get(obj.difficulty, 'primary'),
        #     obj.difficulty
        # )
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.difficulty, 'black'),
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
    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected quizzes marked as active.")
    mark_active.short_description = "Mark selected quizzes as Active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected quizzes marked as inactive.")
    mark_inactive.short_description = "Mark selected quizzes as Inactive"


# Register models
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)

# Customize Admin Site
admin.site.site_header = "Quiz Administration🎓"
admin.site.site_title = "Quiz Admin Portal"
admin.site.index_title = "Welcome to Quiz Admin Portal"