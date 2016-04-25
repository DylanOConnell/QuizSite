from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import AddQuestionForm, AddAnswerForm, AddQuizForm, QuizResultForm, AnswerResultForm
from django.forms import modelformset_factory
from quizcreator.models import Quiz, Question, Answer, QuestionOrdering, QuizResult, AnswerResult
from django.db.models import Max
from django.contrib.auth import login, logout


# FormSets


# This is our basic homepage. For now, provides links to other pages.
def home(request):
    return render(request,'quizsite/home.html')
# Use login
# use is_authenticate

def login_view(request):
    return redirect('/login')

# Logout a user
def logout_view(request):
    logout(request)
    return redirect('/')

# View for the overall list of quizzes. Each quiz id is shown, and provides a link to the first question of that quiz
def quizzes(request):
    quizzes_list = Quiz.objects.all()
#    try:
#        curr_user = request.USER
#        test_list = []
#        for curr_quiz in quizzes_list:
#            if QuizResult.objects.filter(user = curr_user, quiz = curr_quiz):
#
#    except:
#        started_quizzes = None
#    test_list = []
#    for quiz in quizzes_list:
#        if QuizResult.objects.filter(
  #  quizresult_list = QuizResult.objects.all()
    context = {
        'quizzes_list' : quizzes_list,
 #       'quizresult_list' : quizresult_list,
    }
    return render(request,'quizsite/quizzes.html',context)

def beginquiz(request,quiz_id):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, pk = quiz_id)
#        first_question = quiz.questions.all().first()
        return redirect('/quizzes/{}/{}'.format(quiz_id,quiz.questions.all().first().id))
    else:
        quiz = get_object_or_404(Quiz, pk = quiz_id)
        if not request.user.is_authenticated():
            context = {'error' : "You must be logged in to begin a quiz."}
            return render(request, 'quizsite/error.html', context)
        else:
            user = request.user
            quizresultform = QuizResultForm(initial = {'quiz' : quiz, 'user' : user, 'finished' : False})
        context = {        
                'quiz' : quiz,
                'quizresultform' : quizresultform,
                }
        return render(request, 'quizsite/beginquiz.html',context)

# view for viewing a question. Needs both the associated quiz and question id
def question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk = quiz_id)
    # We use a filter to find only the question with this id within this quiz M2M field
    # Thus, if this question does not belong to this quiz, we will say no question exists
    question = get_object_or_404( Question.objects.filter( pk = question_id, quiz__id = quiz_id )) 
    # We use a filter to find all answers that have the requisite question_id
    answer_list = Answer.objects.filter(question__id = question_id)
    answerresult_formset = modelformset_factory(AnswerResult,AnswerResultForm,extra=len(answer_list))#, extra=2)
    formset = answerresult_formset(queryset=AnswerResult.objects.none(),initial=[
        {'quiz': quiz, 'question': question, 'answer': answer} for answer in answer_list])
    formset_answers = zip(formset, answer_list)
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
    try:
       curr_question_number = question.questionordering_set.get(quiz_id = quiz.id).ordering
    except:
        curr_question_number = None
    context = {
        'quiz' : quiz,
        'question' : question,
        'answer_list' : answer_list,
        'next_question' : next_question,
        'next_question_number' : next_question_number,
        'prev_question' : prev_question,
        'prev_question_number' : prev_question_number,
        'curr_question_number' : curr_question_number,
#        'formset' : formset,
        'formset_answers': formset_answers,
    }
    return render(request,'quizsite/question.html',context)

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
        answerresult_formset = modelformset_factory(AnswerResult,AnswerResultForm,extra=1)#, extra=2)
        formset = answerresult_formset(request.POST)
        if formset.is_valid():
            new_formset = formset.save(commit=False)
            # Num correct, num partially wrong, num fully wrong
            correct_tally = [0,0,0]
            for form in new_formset:
                if form.quiz.id == long(quiz_id) and form.question.id == long(question_id):
                    try:
                        form.user = request.user
                        if AnswerResult.objects.filter(quiz__id = quiz_id, question__id = question_id, user = request.user, answer = form.answer):
                            try:
                                AnswerResult.objects.filter(quiz__id = quiz_id, question__id = question_id, user = request.user,answer = form.answer).delete()
                                #return HttpResponse(form.answer.id)
                            except:
                                context = {'error' : "You've already submitted an answer to that question."}
                                return render(request, 'quizsite/error.html', context)

                        form.save()
                        if form.selected:
                            if form.answer.correct_type == 'COR':
                                correct_tally[0] = correct_tally[0] + 1
                            if form.answer.correct_type == 'PART_W':
                                correct_tally[1] = correct_tally[1] + 1
                            if form.answer.correct_type == 'FULL_W':
                                correct_tally[2] = correct_tally[2] + 1
                        #return HttpResponse(form.answer.id)
                    except:
                        context = {'error' : "You must be logged in to submit an answer."}
                        return render(request, 'quizsite/error.html', context)# HttpResponse("You must be logged in to submit an answer")
                        
                else:
                    context = {'error' : "Invalid answer submission."}
                    return render(request, 'quizsite/error.html', context)
                    #return HttpResponse("Invalid Answer Submission")#str(form.quiz.id) + " "  + str(form.question.id) + " " +  str(quiz_id) + " " +  str(question_id))
#            return HttpResponse(correct_tally)
            return redirect('/quizzes/{}/{}'.format(str(quiz_id),str(question_id)))
        #return HttpResponse(formset.errors)
        context = {'error' : formset.errors}
        return render(request, 'quizsite/error.html', context)
    else:
        return redirect('/')

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
