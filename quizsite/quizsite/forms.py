from django import forms
from quizcreator.models import Quiz, Question, Answer, QuestionOrdering
#from quizcreator.models import Quiz,Question,Answer,QuestionOrdering,QuizResult,AnswerResult

class AddQuestionForm(forms.Form):
	text = forms.CharField(label="Question Text",max_length=200)
	quiz = forms.ModelChoiceField(queryset = Quiz.objects.all())

	def __init__(self, *args, **kwargs):
       		super(AddQuestionForm, self).__init__(*args, **kwargs)
		self.fields['text'].label = "Question Text"
		self.fields['quiz'].label = "Quiz ID"

	#def __init__(*args,**kwargs):
