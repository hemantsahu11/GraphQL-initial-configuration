from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Quizzes(models.Model):
    title = models.CharField(max_length=25, default="New Quiz")
    category = models.ForeignKey(Category, default=1, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    SCALE = (
        (0, 'Fundamental'),
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Expert'),
    )

    TYPE = (
        (0, 'Multiple Choice'),
    )

    quiz = models.ForeignKey(Quizzes, related_name='question', on_delete=models.DO_NOTHING)
    technique = models.IntegerField(choices=TYPE, default=0, verbose_name="Type of Question")
    title = models.CharField(max_length=255, verbose_name='Title')
    difficulty = models.IntegerField(choices=SCALE, default=0, verbose_name="Difficulty")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    is_active = models.BooleanField(default=False, verbose_name="Active Status")

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answer', on_delete=models.DO_NOTHING)
    answer_text = models.CharField(max_length=255, verbose_name='Answer Text')
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text
