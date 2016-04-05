from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    name = models.CharField(max_length=200,null=True)
    questions = models.ManyToManyField('Question',through ='QuestionOrdering')
    def __str__(self):
        return '{} {}'.format('Quiz #:', self.id)
   #Similarly, do we actually want an M2M field here? #Dylan: Actually in this case I think I would like to be able to reuse questions between quizzes. I did change the other instances where a FK would be better!

class Question(models.Model):
    text = models.CharField(max_length=200)
    def __str__(self):
        return '{} {}'.format('Question #:',self.id)

class QuestionOrdering(models.Model):
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    ordering = models.PositiveIntegerField()

class Answer(models.Model):
    text = models.CharField(max_length=200)
# An answer can either be fully correct, partly wrong, or fully wrong, and we store which of these 3 possibilities is the answer
    correct = 'COR'
    partly_wrong = 'PART_W'
    fully_wrong  = 'FULL_W'
    answer_choices = (
        (correct, 'Correct'),
        (partly_wrong, 'Partly Wrong'),
        (fully_wrong, 'Fully Wrong'),
    )
    correct_type = models.CharField(max_length=6,choices=answer_choices, default = fully_wrong)   
    question = models.ForeignKey(Question,null=True,blank=True) # For now, I will allow answers that don't have associated questions to be stored for future use! 
# This is outdated and unused. Will soon be replaced by a real user system.
#class User(models.Model):
    # users can be either reg_users or admins. reg_users can take tests, admins can see everyone's results
#    admin = 'adm'
#    reg_user = 'usr'
#    user_choices = ( (admin, 'Admin'), (reg_user, 'User'))
#    user_type = models.CharField(max_length=3,choices = user_choices,default = reg_user)


# The results system has not been implemented. These are placeholder models.
class QuizResult(models.Model):
    score = models.IntegerField(default=0)
    user = models.ForeignKey(User,null=True)
    quiz = models.ForeignKey(Quiz)

class AnswerResult(models.Model):
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    selected = models.BooleanField() # CASEY: Clever. :)

