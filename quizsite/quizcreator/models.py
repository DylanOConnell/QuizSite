from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=200, null=True)
    questions = models.ManyToManyField('Question', through='QuestionOrdering')

    def __str__(self):
        if self.name:
            return self.name
        else:
            return '{} {}'.format('Quiz #:', self.id)


class Question(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return '{} {}'.format('Question #:', self.id)


class QuestionOrdering(models.Model):
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    ordering = models.PositiveIntegerField()


class Answer(models.Model):
    text = models.CharField(max_length=200)
# An answer can either be fully correct, partly wrong, or fully wrong, and we store which of these 3 possibilities is the answer
    correct = 'COR'
    partly_wrong = 'PART_W'
    fully_wrong = 'FULL_W'
    answer_choices = (
        (correct, 'Correct'),
        (partly_wrong, 'Partly Wrong'),
        (fully_wrong, 'Fully Wrong'),
    )
    correct_type = models.CharField(max_length=6, choices=answer_choices, default=fully_wrong)
    question = models.ForeignKey(Question, null=True, blank=True)

    def __str__(self):
        return self.text


class QuizResult(models.Model):
    score = models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True, blank=True)
    quiz = models.ForeignKey(Quiz)
    finished = models.BooleanField(default=False)


class AnswerResult(models.Model):
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(User, null=True, blank=True)
    selected = models.BooleanField()


class BugReport(models.Model):
    user = models.ForeignKey(User)
    report = models.CharField(max_length=1000, verbose_name="Bug Report")
    timestamp = models.DateTimeField(null=True)

