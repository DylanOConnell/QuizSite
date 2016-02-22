from django.db import models

class answer(models.Model):
    text = models.CharField(max_length=200)
    #pub_date = models.DateTimeField('date published')
    correct_type = models.IntegerField(default=0)

#class questions_answers(models.Model):
#    answer_fk = models.ForeignKey(answer)
#    question_fk = models.ForeignKey(question)

class questions(models.Model):
    text = models.CharField(max_length=200)
    answers = models.ManyToManyField(answer)

class quiz(models.Model):
    questions = models.ManyToManyField(questions)

class users(models.Model):
    user_type = models.IntegerField(default=0)

class quiz_results(models.Model):
    score = models.IntegerField(default=0)
    user = models.ForeignKey(users)
    quiz = models.ForeignKey(quiz)

class answer_results(models.Model):
    quiz = models.ForeignKey(quiz)
    question = models.ForeignKey(questions)
    answer = models.ForeignKey(answer)
    selected = models.BooleanField()








#class questions(models.Model):

#class Choice(models.Model):
#    question = models.ForeignKey(Question)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)
