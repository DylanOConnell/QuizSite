from django.db import models

class question(models.Model):
    text = models.CharField(max_length=200)

class answer(models.Model):
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
    question = models.ForeignKey(question,null=True,blank=True) # For now, I will allow answers that don't have associated questions to be stored for future use! 

class quiz(models.Model):
    questions = models.ManyToManyField(question) #CASEY: Similarly, do we actually want an M2M field here? #Dylan: Actually in this case I think I would like to be able to reuse questions between quizzes. I did change the other instances where a FK would be better!

class user(models.Model):
    # users can be either reg_users or admins. reg_users can take tests, admins can see everyone's results
    admin = 'adm'
    reg_user = 'usr'
    user_choices = ( (admin, 'Admin'), (reg_user, 'User'))
    user_type = models.CharField(max_length=3,choices = user_choices,default = reg_user)

class quiz_results(models.Model):
    score = models.IntegerField(default=0)
    user = models.ForeignKey(user)
    quiz = models.ForeignKey(quiz)

class answer_results(models.Model):
    quiz = models.ForeignKey(quiz)
    question = models.ForeignKey(question)
    answer = models.ForeignKey(answer)
    selected = models.BooleanField() # CASEY: Clever. :)

#class Choice(models.Model):
#    question = models.ForeignKey(Question)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)
