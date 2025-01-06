from django.db import models
<<<<<<< HEAD

from django.contrib.auth.models import User

class Quiz(models.Model):

=======
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class Quiz(models.Model):
    description = RichTextField()
>>>>>>> 7e79dcb39adf4aace1ca4763daa5ae0b61a6bac4
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
<<<<<<< HEAD


    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='quiz_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    duration = models.IntegerField(help_text="Duration in minutes",default=2)
=======
>>>>>>> 7e79dcb39adf4aace1ca4763daa5ae0b61a6bac4
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='Medium'
    )
<<<<<<< HEAD
=======


    title = models.CharField(max_length=200)
    description = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
>>>>>>> 7e79dcb39adf4aace1ca4763daa5ae0b61a6bac4
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_quizzes'
    )
<<<<<<< HEAD
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
=======

    duration = models.IntegerField(help_text="Duration in minutes", default=30)
    attempts = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_quizzes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = "Quizzes"
>>>>>>> 7e79dcb39adf4aace1ca4763daa5ae0b61a6bac4

    def __str__(self):
        return self.title

<<<<<<< HEAD
    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']
=======
>>>>>>> 7e79dcb39adf4aace1ca4763daa5ae0b61a6bac4

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
<<<<<<< HEAD

=======
    
>>>>>>> 7e79dcb39adf4aace1ca4763daa5ae0b61a6bac4
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text
# Create your models here.
