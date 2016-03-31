from django.http import HttpResponse 
from django.shortcuts import get_object_or_404, render
from django.template import loader
from .forms import AddQuestionForm
from quizcreator.models import Quiz, Question, Answer, QuestionOrdering
from django.db.models import Max

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
	quiz = get_object_or_404(Quiz, pk = quiz_id)
	# We use a filter to find only the question with this id within this quiz M2M field
	# Thus, if this question does not belong to this quiz, we will say no question exists
	question = get_object_or_404( Question.objects.filter( pk = question_id, quiz__id = quiz_id )) 
	# We use a filter to find all answers that have the requisite question_id
	answer_list = Answer.objects.filter(question__id = question_id)
	# We find the next and previous question using questionordering, if they exist. It also grabs the number, for display purposes
	try:
		next_question = Question.objects.get(quiz__id = quiz.id, questionordering__ordering =  ( question.questionordering_set.get(quiz_id = quiz.id).ordering+1))
		next_question_number = next_question.questionordering_set.get(quiz_id = quiz.id).ordering
	except:
		next_question = None	
		next_question_number = None
	try:
                prev_question = Question.objects.get(quiz__id = quiz.id, questionordering__ordering =  ( question.questionordering_set.get(quiz_id = quiz.id).ordering-1))
		prev_question_number = prev_question.questionordering_set.get(quiz_id = quiz.id).ordering
        except:
                prev_question = None
		prev_question_number = None

	template = loader.get_template('quizsite/question.html')
	context = {
		'quiz' : quiz,
		'question' : question,
		'answer_list' : answer_list,
		'next_question' : next_question,
		'next_question_number' : next_question_number,
		'prev_question' : prev_question,
		'prev_question_number' : prev_question_number,
	}
	return HttpResponse(template.render(context,request))

"""
	def answer(request,quiz_id,question_id){
	question = get_object_or_404(Question, pk = question_id)
	try:
		userchoice = question.answer_set(pk = request.POST['answer'])
	except:
		userchoice = None
	else:
		newquizresult = models.QuizResult(quiz = quiz_id)
		newanswerresult = models.AnswerResult(question = question_id, answer = userchoice, selected = True)  
	}

"""

# This page has two purposes. It either accepts a post request to create a new question, or it displays a form which can be used to send a post request to create a new question.
def addquestion(request):
	# If post request, we take the informtion from a post request. 
	if request.method=="POST":
		questionform = AddQuestionForm(request.POST)
		# We clean the data, save the question, and then add its correct numbering, as well as QuestionOrdering object
		if questionform.is_valid():
			newquestion = Question(text=questionform.cleaned_data['text']) 
			newquestion.save()
			nextnumber = QuestionOrdering.objects.filter(quiz = questionform.cleaned_data['quiz']).aggregate(Max('ordering'))['ordering__max'] + 1
			qordering = QuestionOrdering(quiz = questionform.cleaned_data['quiz'], question = newquestion, ordering = nextnumber )
			qordering.save()
			# Then, we display another Form to take in new information
			questionform = AddQuestionForm()
	else:
		questionform = AddQuestionForm()
	template = loader.get_template('quizsite/addquestion.html')
	context = {
		'questionform':questionform,
	}
	return HttpResponse(template.render(context,request))



#def createquiz(request):
#	template = loader.get_template('quizsite/createquiz.html')
#	context = {
#		'user' : user,
#	}
#	return HttpResponse(template.render(context,request))
#
