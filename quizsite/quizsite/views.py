from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from quizcreator.models import Quiz, Question, Answer
#from quizcreator.models import Question
#from quizcreator.models import Answer

# View for the overall list of quizzes. Each quiz id is shown, and provides a link to the first question of that quiz
def quizzes(request):
	quizzes_list = Quiz.objects.all()
	template = loader.get_template('quizsite/quizzes.html')
	context = {
		'quizzes_list' : quizzes_list,
	}
	return HttpResponse(template.render(context,request))

# view for viewing a question. Needs both the associated quiz and question id
def question(request, quiz_id, question_id):
	quiz = get_object_or_404(Quiz,pk = quiz_id)
	question = quiz.questions.filter(pk = question_id)
#	if quiz.questions.filter(pk = question_id):
#		question = get_object_or_404(Question, pk = question_id)
#	else:
#		question = None
	# We use the relation manager in Django to find all answers associated with a certain question
#	answer_list = question.answer_set.all
	answer_list = Answer.objects.filter(question__id = question_id)
	template = loader.get_template('quizsite/question.html')
	context = {
		'quiz' : quiz,
		'question' : question,
		'answer_list' : answer_list,
	}
	return HttpResponse(template.render(context,request))

#def createquiz(request):
#	template = loader.get_template('quizsite/createquiz.html')
#	context = {
#		'user' : user,
#	}
#	return HttpResponse(template.render(context,request))
#
