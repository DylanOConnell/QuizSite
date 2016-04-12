from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import AddQuestionForm, AddAnswerForm, AddQuizForm, QuizResultForm, AnswerResultForm
from quizcreator.models import Quiz, Question, Answer, QuestionOrdering, QuizResult, AnswerResult
from django.db.models import Max
from django.contrib.auth import login, logout


# This is our basic homepage. For now, provides links to other pages.
def home(request):
    return render(request,'quizsite/home.html')
# Use login
# use is_authenticate

def login_view(request):
#   return render(request, 'registration/login.html')
    return redirect('/login')

# Logout a user
def logout_view(request):
    logout(request)
    return redirect('/')

#    try:
#       del request.session['member_id']
#    except KeyError:
#        pass
#    return HttpResponse("Logout successful.")

# View for the overall list of quizzes. Each quiz id is shown, and provides a link to the first question of that quiz
def quizzes(request):
    quizzes_list = Quiz.objects.all()
    context = {
        'quizzes_list' : quizzes_list,
    }
    return render(request,'quizsite/quizzes.html',context)

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

    context = {
        'quiz' : quiz,
        'question' : question,
        'answer_list' : answer_list,
        'next_question' : next_question,
        'next_question_number' : next_question_number,
        'prev_question' : prev_question,
        'prev_question_number' : prev_question_number,
    }
    return render(request,'quizsite/question.html',context)


#   def answer(request,quiz_id,question_id){
#   question = get_object_or_404(Question, pk = question_id)
#   try:
#       userchoice = question.answer_set(pk = request.POST['answer'])
#   except:
#       userchoice = None
#   else:
#       newquizresult = models.QuizResult(quiz = quiz_id)
#       newanswerresult = models.AnswerResult(question = question_id, answer = userchoice, selected = True)  
#   }

# This page has two purposes. It either accepts a post request to create a new question, or it displays two forms, which can be used to send a post request to create a new question or new answer.
def addquestion(request):
    # If post request, we take the informtion from a post request. 
    if request.method=="POST":
        questionform = AddQuestionForm(request.POST)
        # We clean the data, save the question, and then add its correct numbering, as well as QuestionOrdering object
        if questionform.is_valid():
            newquestion = Question(text=questionform.cleaned_data['text']) 
            newquestion.save()
            if QuestionOrdering.objects.filter(quiz = questionform.cleaned_data['quiz']).aggregate(Max('ordering'))['ordering__max']:
                nextnumber = QuestionOrdering.objects.filter(quiz = questionform.cleaned_data['quiz']).aggregate(Max('ordering'))['ordering__max'] + 1
            else:
                nextnumber = 0
            qordering = QuestionOrdering(quiz = questionform.cleaned_data['quiz'], question = newquestion, ordering = nextnumber )
            qordering.save()
            # Then, we display another Form to take in new information
            questionform = AddQuestionForm()
            answerform = AddAnswerForm()
            quizform = AddQuizForm()
    # Tell the user (using the django functionality) telling the user why their form was not valid.
    # if post information not provided, simply display both forms.
    else:
        questionform = AddQuestionForm()
        answerform = AddAnswerForm()
        quizform = AddQuizForm()
    context = {
        'questionform':questionform,
        'answerform':answerform,
        'quizform':quizform,
    }
    return render(request,'quizsite/addquestion.html',context)

# This either takes in a POST request to create an answer, or simply redirects to the AddQuestion page.
def addanswer(request):
    if request.method=="POST":
        answerform = AddAnswerForm(data=request.POST)
        if answerform.is_valid():
            answerform.save()
            return redirect('/quizzes/addquestion')
    else:
        return redirect('/quizzes/addquestion')

def addquiz(request):
    if request.method=="POST":
        quizform = AddQuizForm(data=request.POST)
        if quizform.is_valid():
            quizform.save()
            return redirect('/quizzes/addquestion')
    else:
        return redirect('/quizzes/addquestion')



def submitanswer(request, quiz_id, question_id):
    if request.method =="POST":
        selected_answers = request.POST.getlist('answer')
#       for answer in Answer.objects.filter(question__id = question_id):
#           newanswerresult = AnswerResult(question =  
#       for answer in selected_answers:
        return HttpResponse(selected_answers)
    else:
        return redirect('/quizzes')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

        

#def createquiz(request):
#   template = loader.get_template('quizsite/createquiz.html')
#   context = {
#       'user' : user,
#   }
#   return HttpResponse(template.render(context,request))
# 
