# These are the models for our Django objects/SQL database.
# The readme has some high level info on how these interact. The docstrings 
# and comments have further details. The naming is intended to be intuitive,
# and understandable to a viewer of the code.
from django.db import models
from django.contrib.auth.models import User


# Our site stores quizzes, which have a name, and are referenced through a m2m relationship with questions.
class Quiz(models.Model):
    """Each Quiz has a name, and a m2m relationship with questions"""
    name = models.CharField(max_length=200, null=True)
    # We allow a m2m relationship between quizzes and questions because as the quizsite grows, it makes sense
    # for instructors to be able to reuse particularly good questions. This helps ensure that we do not repeat ourselves.
    questions = models.ManyToManyField('Question', through='QuestionOrdering')

    def __str__(self):
        """This determines the display name of our quiz"""
        if self.name:
            return self.name
        else:
            return '{} {}'.format('Quiz #:', self.id)


# Questions are what users have to answer, and are referenced by many answers, and have a m2m relationship
# with Quizzes. They have 'text' which is the question itself.
class Question(models.Model):
    """Each question is connected to quiz by m2m, is referenced by many answers, and has its own text"""
    text = models.CharField(max_length=200)

    def __str__(self):
        """The proper display name for the Question""" 
        return '{} {}'.format('Question #:', self.id)

#Due to the m2m relationship of quizzes and questions, we must have something that tracks 
# the ordering of each question for each quiz it is in. Thus, we use the through table,
# with ordering storing that data.
class QuestionOrdering(models.Model):
    """
    quiz and question have m2m relation with through table. QuestionOrdering allows us to track
    the ordering of the questions in each quiz.
    """
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    ordering = models.PositiveIntegerField()


class Answer(models.Model):
    """ Each answer references a question, and has its own text, and whether it is correct"""
    text = models.CharField(max_length=200)
# An answer can either be fully correct, partly wrong, or fully wrong, and we store which of these 3 possibilities is the answer
# See the readme.txt for scoring details.
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
        """It is displayed as just its text"""
        return self.text


# This is created when a user starts a quiz. When they submit the quiz, finished is set to True.
# When a superuser views the quizresult, the score is computed and stored.
class QuizResult(models.Model):
    """Each user attempt at a quiz is stored in a QuizResult. It stores user, quiz, whether it is finished, and the score"""
    # The score is initially 0. The score is only updated when a superuser views the results for that quiz, and is 
    # not meaningful before then.
    score = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    finished = models.BooleanField(default=False)


# The user's responses to a quiz are stored as answer results. For every possible answer in a quiz, 
# we store an AnswerResult object that stores whether or not he selected it (in 'selected')
class AnswerResult(models.Model):
    """
    Users submit answers with an AnswerResult per answer that stores the user, the quiz, the question, the answer, and whether or
    not they did select that answer.
    """
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(User, null=True, blank=True)
    selected = models.BooleanField()


class BugReport(models.Model):
    """Users submit bug reports which store the user, the text of the report, and the timestamp of submission"""
    user = models.ForeignKey(User)
    report = models.CharField(max_length=1000, verbose_name="Bug Report")
    timestamp = models.DateTimeField(null=True)
