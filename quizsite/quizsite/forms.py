from django import forms
from django.forms import ModelForm
from quizcreator.models import Quiz, Question, Answer, QuestionOrdering, QuizResult, AnswerResult 
#from quizcreator.models import Quiz,Question,Answer,QuestionOrdering,QuizResult,AnswerResult

# This takes in the required information, and creates a question with text and links it to a quiz.
class AddQuestionForm(forms.Form):
    text = forms.CharField(label="Question Text",max_length=200)
    quiz = forms.ModelChoiceField(queryset = Quiz.objects.all())

    def __init__(self, *args, **kwargs):
        super(AddQuestionForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Question Text"
        self.fields['quiz'].label = "Quiz ID"

# This modelform provides the fields to create an answer.
class AddAnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correct_type', 'question'] 

class LoginForm(forms.Form):
    username = forms.CharField(label="User")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class QuizResultForm(ModelForm): 
    class Meta:
        model = QuizResult
        fields = ['score','user','quiz']

# custom validation for a form: only valid inputs, even with hidden field
class AnswerResultForm(ModelForm):
    class Meta:
        model = AnswerResult
        fields = ['quiz','question','answer','selected']
