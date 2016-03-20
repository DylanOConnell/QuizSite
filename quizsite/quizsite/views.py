from django.http import HttpResponse
from django.template import loader

from quizcreator.models import quiz
#from models import quiz
def quizzes(request):
	quizzes_list = quiz.objects.all()
	template = loader.get_template('quizsite/quizzes.html')
	context = {
		'quizzes_list' : quizzes_list,
	}
	return HttpResponse(template.render(context,request))
