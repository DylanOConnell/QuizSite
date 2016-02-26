from django.db import models

class answer(models.Model):
    text = models.CharField(max_length=200)
    #pub_date = models.DateTimeField('date published')
    correct_type = models.IntegerField(default=0) # CASEY: Why use an integer for this? You could also use a `choices` string: https://docs.djangoproject.com/en/1.8/ref/models/fields/#choices . Write a comment here explaining what you're intending to do.

#class questions_answers(models.Model):
#    answer_fk = models.ForeignKey(answer)
#    question_fk = models.ForeignKey(question)

class questions(models.Model):
    text = models.CharField(max_length=200)
    answers = models.ManyToManyField(answer) # CASEY: Does this need to be an M2M? Sure a question can have multiple answers, but can an answer have multiple questions? You might actually just want a ForeignKey.

class quiz(models.Model):
    questions = models.ManyToManyField(questions) #CASEY: Similarly, do we actually want an M2M field here?

class users(models.Model):
    user_type = models.IntegerField(default=0) #CASEY: Again, `choices` vs integer. I'd recommend you use whatever is less confusing for someone trying to learn your setup. :)

class quiz_results(models.Model):
    score = models.IntegerField(default=0)
    user = models.ForeignKey(users)
    quiz = models.ForeignKey(quiz)

class answer_results(models.Model):
    quiz = models.ForeignKey(quiz)
    question = models.ForeignKey(questions)
    answer = models.ForeignKey(answer)
    selected = models.BooleanField() # CASEY: Clever. :)








#class questions(models.Model):

#class Choice(models.Model):
#    question = models.ForeignKey(Question)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)
