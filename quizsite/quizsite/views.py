from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from quizcreator.models import Quiz, Question, Answer
#from quizcreator.models import Question
#from quizcreator.models import Answer

# View for the overall list of quizzes. Each quiz id is shown, and provides a link to the first question of that quiz
def quizzes(request):
	quizzes_list = Quiz.objects.all()
	#first_question = get_object_or_404(Question.objects.filter( )
	template = loader.get_template('quizsite/quizzes.html')
	context = {
		'quizzes_list' : quizzes_list,
	}
	return HttpResponse(template.render(context,request))

# view for viewing a question. Needs both the associated quiz and question id
def question(request, quiz_id, question_id):
	quiz = get_object_or_404(Quiz, pk = quiz_id)
	# we use a filter to find only the question with this id within this quiz M2M field
	# Thus, if this question does not belong to this quiz, we will say no question exists
#	question = Question.objects.get(quiz__id = quiz_id, pk = question_id ) 
	question = get_object_or_404( Question.objects.filter( pk = question_id, quiz__id = quiz_id )) 
	#question = get_object_or_404(Question, pk = question_id) 
	# We use a filter to find all answers that have the requisite question_id
	answer_list = Answer.objects.filter(question__id = question_id)
	try:
		next_question = Question.objects.get(quiz__id = quiz.id, questionordering__ordering =  ( question.questionordering_set.get(quiz_id = question.quiz_set.get().id).ordering+1))
	except:
		next_question = None	
	#next_question =dQuestion.objects.get((question.questionordering_set.get(quiz.id = quiz_id).ordering +1)
	#next_question = Question.objects.filter(quiz__id = quiz_id, questionordering__ordering = question.questionoordering__ordering + 1)
	template = loader.get_template('quizsite/question.html')
	context = {
		'quiz' : quiz,
		'question' : question,
		'answer_list' : answer_list,
		'next_question' : next_question,
	}
	return HttpResponse(template.render(context,request))

#def createquiz(request):
#	template = loader.get_template('quizsite/createquiz.html')
#	context = {
#		'user' : user,
#	}
#	return HttpResponse(template.render(context,request))
#
