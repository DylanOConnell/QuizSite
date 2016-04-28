from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import AddQuestionForm, AddAnswerForm, AddQuizForm, QuizResultForm, AnswerResultForm, BugReportForm
from django.forms import modelformset_factory
from quizcreator.models import Quiz, Question, Answer, QuestionOrdering, QuizResult, AnswerResult, BugReport
from django.db.models import Max
from django.contrib.auth import login, logout


# This is our basic homepage. For now, provides links to other pages.
def home(request):
    """Returns the home page of the website."""
    return render(request, 'quizsite/home.html')

# Provides a destination for login_view, and redirects to the Django login page. 
def login_view(request):
    """Returns our basic login page"""
    return redirect('/login')

# Logs out a user using django.contrib.auth, and redirects to home
def logout_view(request):
    """Returns our basic logout page"""
    logout(request)
    return redirect('/')


# View for the overall list of quizzes. Each quiz id is shown, and provides a link to the first question of that quiz
def quizzes(request):
    """Returns the page with a list of available quizzes."""
    quizzes_list = Quiz.objects.all()
    context = {
        'quizzes_list': quizzes_list,
    }
    return render(request, 'quizsite/quizzes.html', context)

# For a given quiz, allows the user to begin a quiz attempt
def beginquiz(request, quiz_id):
    """Returns a page which allows the user to begin a quiz
    
    If it receives a post request, it creates a QuizResult object.
    Otherwise, it provides a form to create a QuizResult object.
    """
    if request.method == "POST":
        # Only logged in users can begin a quiz
        if request.user.is_authenticated():
            quiz = get_object_or_404(Quiz, pk=quiz_id)
            quizresultform = QuizResultForm(request.POST)
            if quizresultform.is_valid():
                # Do not let a user begin a quiz they've already started.
                if QuizResult.objects.filter(quiz=quiz, user=request.user):
                    context = {'error': "You've already begun that quiz.", 'quiz': quiz}
                    return render(request, 'quizsite/alreadybegunquiz.html', context)
                # Otherwise, we save this QuizResult, and begin the quiz.
                else:
                    # Check that the submitted form has not had its values tampered with.
                    if quizresultform.cleaned_data['quiz'] == quiz and quizresultform.cleaned_data['user'] == request.user:
                        quizresultform.save()  
                        return redirect('/quizzes/{}/{}'.format(quiz_id, quiz.questions.all().first().id))
                    else:
                        context = {'error': "Invalid Submission."}
                        return render(request, 'quizsite/error.html', context)
            else:
                context = {'error': "Invalid Submission."}
                return render(request, 'quizsite/error.html', context)
        else:
            context = {'error': "You must be logged in to begin a quiz."}
            return render(request, 'quizsite/error.html', context)

    else:
        # If not POST, we display the QuizResult form to begin a quiz.
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        if not request.user.is_authenticated():
            context = {'error': "You must be logged in to begin a quiz."}
            return render(request, 'quizsite/error.html', context)
        else:
            user = request.user
            # We provide the initial data for the QuizResult form.
            quizresultform = QuizResultForm(initial={'quiz': quiz, 'user': user, 'finished': False})
            context = {
                    'quiz': quiz,
                    'quizresultform': quizresultform,
                    }
            return render(request, 'quizsite/beginquiz.html', context)

# After submitting the final answer, this view allows the user to choose 
# whether to submit the quiz attempt, or to return to the quiz
def endofquiz(request, quiz_id):
    """ Gives the user the option submit quiz, or go back to start"""
    if request.user.is_authenticated():
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        # We find the first question in the quiz, if available
        try:
            first_question = quiz.questions.all().first()
        except:
            first_question = None
        context = {'quiz': quiz, 'first_question': first_question}
        return render(request, 'quizsite/endofquiz.html', context)
    else:
        context = {'error': "Must be logged in to end a quiz."}
        return render(request, 'quizsite/error.html', context)


def finishquiz(request, quiz_id):
    """For a given quiz, attempts to submit the current users answers.

    This checks if the user has submitted an AnswerResult for each question on the quiz.
    If they have, it sets QuizResult.finished to True. It does not yet score the quiz.
    """
    # Only logged in users can submit a quiz
    if request.user.is_authenticated():
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        # Check that the user has started the quiz, display error if not.
        if QuizResult.objects.filter(quiz=quiz, user=request.user):
            # Doublecheck that there are not two QuizResults in the system. This should be impossible, but we check anyways.
            if len(QuizResult.objects.filter(quiz=quiz, user=request.user)) == 1:
                # Check if they have completed the quiz
                if QuizResult.objects.filter(quiz=quiz, user=request.user).first().finished:
                    context = {'error': "You have already completed this quiz."}
                    return render(request, 'quizsite/error.html', context)
                # If there is a single, valid, unfinished quiz attempt, we verify that there is one answerresult for each answer
                else:
                    quizresult = QuizResult.objects.filter(quiz=quiz, user=request.user).first()
                    question_list = Question.objects.filter(quiz__id=quiz_id)
                    #For each answer, check that there is an answer result. Otherwise, display what answer is missing.
                    for question in question_list:
                        answer_list = question.answer_set.all()
                        for answer in answer_list:
                            try:
                                result = AnswerResult.objects.get(user=request.user, quiz=quiz, question=question, answer=answer)
                            except:
                                context = {'error': "There is not exactly one submitted answer for Quiz: {}, Question: {}. Answer: {}".format(quiz, question, answer)}
                                return render(request, 'quizsite/error.html', context)
                    # If the answers are all there, finish the quiz.
                    quizresult.finished = True
                    quizresult.save()
                    context = {'quiz': quiz}
                    return render(request, 'quizsite/submittedquiz.html', context)
            else:
                context = {'error': "There is an error, more than one quiz attempt active. Contact an administrator."}
                return render(request, 'quizsite/error.html', context)

        else:
            context = {'error': "You have not yet begun this quiz."}
            return render(request, 'quizsite/error.html', context)
    else:
        context = {'error': "Must be logged in to end a quiz."}
        return render(request, 'quizsite/error.html', context)


def listquizresults(request):
    """For superuser, provides a link to the result page for each quiz (checkresults)""" 
    # Only superusers can view quizresults
    if request.user.is_authenticated() and request.user.is_superuser:
        quizzes_list = Quiz.objects.all()
        context = {
            'quizzes_list': quizzes_list,
        }
        # This template will provide links to the checkresults page for each quiz
        return render(request, 'quizsite/listquizresults.html', context)


def checkresults(request, quiz_id):
    """For superuser and a given quiz, provides links to the result of each user who took quiz"""
    # Only superusers can view quizresults
    if request.user.is_authenticated() and request.user.is_superuser:
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        quizresult_list = QuizResult.objects.filter(quiz=quiz, finished=True)
        user_list = User.objects.filter(id__in=quizresult_list.values('user_id'))
        context = {'quiz': quiz, 'user_list': user_list}
        # This page provides links to the result page for each user who finished the quiz.
        return render(request, 'quizsite/checkresults.html', context)
    else:
        context = {'error': "Only superusers can see quiz results."}
        return render(request, 'quizsite/error.html', context)


def quizresults(request, quiz_id, username):
    """If superuser, given a quiz and username, calculates and displays the total scoring of that quiz submission"""
    # Only superusers can view quizresults
    if request.user.is_authenticated() and request.user.is_superuser:
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        user = get_object_or_404(User, username=username)
        if len(QuizResult.objects.filter(quiz=quiz, user=user)) == 1:
            if len(QuizResult.objects.filter(quiz=quiz, user=user, finished=True)) == 1:
                quizresult = get_object_or_404(QuizResult, quiz=quiz, user=user, finished=True)
                question_list = Question.objects.filter(quiz__id=quiz_id)
                # This is the first time that score is properly calculated, and set, in the QuizResult object.
                # The quiz is not scored until a superuser checks the results.
                score = 0
                for question in question_list:
                    # For a question, tracks the # correct, # partially correct, # fully wrong.
                    correct_tally = [0, 0, 0]
                    answer_list = question.answer_set.all()
                    for answer in answer_list:
                        try:
                            result = AnswerResult.objects.get(user=user, quiz=quiz, question=question, answer=answer)
                            # If they selected this answer, we record which type it truly was 
                            if result.selected:
                                if answer.correct_type == 'COR':
                                    correct_tally[0] += 1
                                if answer.correct_type == 'PART_W':
                                    correct_tally[1] += 1
                                if answer.correct_type == 'FULL_W':
                                    correct_tally[2] += 1
                        except:
                            context = {'error': "There is not exactly one submitted answer for Quiz: {}, Question: {}. Answer: {}".format(quiz, question, answer)}
                            return render(request, 'quizsite/error.html', context)
                    # We calculate their score for this question using this formula
                    if correct_tally[2]>0:
                        score += 0
                    else:
                        score += correct_tally[0]*((.5)**(correct_tally[1]))
                quizresult.score = score
                quizresult.save()
                # We need to provide the template  with the questions, the answers, and the users responses.
                # We zip the answers and responses together, then zip the list of those lists with the list of questions.
                # This allows the template to easily iterate through these lists and display them.
                # We sort the answers and answerresults by answer.id so that they correctly match
                answer_lists = zip(question_list, [zip(sorted(question.answer_set.all(), key=lambda x: x.id), sorted(question.answerresult_set.filter(user=user), key=lambda x: x.answer.id)) for question in question_list])
                context = {
                        'quiz': quiz,
                        'answer_lists': answer_lists,
                        'score': score,
                        'this_user': user,
                        }
                return render(request, 'quizsite/quizresults.html', context)
            else:
                context = {'error': "The user has not yet submitted this quiz."}
                return render(request, 'quizsite/error.html', context)
        else:
            context = {'error': "The user has not yet begun this quiz, or there is a duplicate attempt in the system."}
            return render(request, 'quizsite/error.html', context)
    else:
        context = {'error': "Only superusers can see quiz results."}
        return render(request, 'quizsite/error.html', context)


# view for viewing a question. Needs both the associated quiz and question id
def question(request, quiz_id, question_id):
    """Given quiz and question, displays the question and modelformset for answer submission"""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    # We use a filter to find only the question with this id within this quiz M2M field
    # Thus, if this question does not belong to this quiz, we will say no question exists
    question = get_object_or_404(Question.objects.filter(pk=question_id, quiz__id=quiz_id))
    # We use a filter to find all answers that have the requisite question_id
    answer_list = Answer.objects.filter(question__id=question_id)
    answerresult_formset = modelformset_factory(AnswerResult, AnswerResultForm, extra=len(answer_list))
    formset = answerresult_formset(queryset=AnswerResult.objects.none(), initial=[
        {'quiz': quiz, 'question': question, 'answer': answer} for answer in answer_list])
    #We combine the formset with answer_list, so our template can display the answer text with each form.
    formset_answers = zip(formset, answer_list)
    # For display purposes, we grab the number for the previous, current, and next question.
    # We do not simply add and substract 1 from the current question number in case there is an issue with the numbering.
    try:
        next_question = Question.objects.get(quiz__id=quiz.id, questionordering__ordering=(question.questionordering_set.get(quiz_id=quiz.id).ordering+1))
        next_question_number = next_question.questionordering_set.get(quiz_id=quiz.id).ordering
    except:
        next_question = None
        next_question_number = None
    try:
        prev_question = Question.objects.get(quiz__id=quiz.id, questionordering__ordering=(question.questionordering_set.get(quiz_id=quiz.id).ordering-1))
        prev_question_number = prev_question.questionordering_set.get(quiz_id=quiz.id).ordering
    except:
        prev_question = None
        prev_question_number = None
    try:
        curr_question_number = question.questionordering_set.get(quiz_id=quiz.id).ordering
    except:
        curr_question_number = None
    context = {
        'quiz': quiz,
        'question': question,
        'answer_list': answer_list,
        'next_question': next_question,
        'next_question_number': next_question_number,
        'prev_question': prev_question,
        'prev_question_number': prev_question_number,
        'curr_question_number': curr_question_number,
        'formset': formset,
        'formset_answers': formset_answers,
    }
    return render(request, 'quizsite/question.html', context)


# This page has two purposes. It either accepts a post request to create a new question, or it displays two forms, which can be used to send a post request to create a new question or new answer.
def addquestion(request):
    """Displays the forms for adding a quiz, question, and answer for a superuser. Also processes an AddQuestion form"""
    # This page only processes the AddQuestion forms, but displays all 3.
    if request.method == "POST":
        if request.user.is_superuser:
            questionform = AddQuestionForm(request.POST)
            # We clean the data, save the question, and then add its correct numbering, as well as QuestionOrdering object
            if questionform.is_valid():
                newquestion = Question(text=questionform.cleaned_data['text'])
                newquestion.save()
                #We give the created question the next number for that quiz.
                if QuestionOrdering.objects.filter(quiz=questionform.cleaned_data['quiz']):
                    nextnumber = QuestionOrdering.objects.filter(quiz=questionform.cleaned_data['quiz']).aggregate(Max('ordering'))['ordering__max'] + 1
                #Otherwise, this is the first question.
                else:
                    nextnumber = 1
                #Save this new questionordering object.
                qordering = QuestionOrdering(quiz=questionform.cleaned_data['quiz'], question=newquestion, ordering=nextnumber)
                qordering.save()
                # Then, we display a new set of forms
                questionform = AddQuestionForm()
                answerform = AddAnswerForm()
                quizform = AddQuizForm()
                context = {
                    'questionform': questionform,
                    'answerform': answerform,
                    'quizform': quizform,
                }
                return render(request, 'quizsite/addquestion.html', context)
            #Tell the user (using the django functionality) telling the user why their form was not valid.
            else:
                context = {'error': questionform.errors}
                return render(request, 'quizsite/error.html', context)
        else:
            context = {'error': "Only superusers can change quizzes."}
            return render(request, 'quizsite/error.html', context)
    # if post information not provided, simply display both forms.
    else:
        if request.user.is_superuser:
            questionform = AddQuestionForm()
            answerform = AddAnswerForm()
            quizform = AddQuizForm()
            context = {
                'questionform': questionform,
                'answerform': answerform,
                'quizform': quizform,
            }
            return render(request, 'quizsite/addquestion.html', context)
        else:
            context = {'error': "Only superusers can edit the quizzes."}
            return render(request, 'quizsite/error.html', context)

# Process POST request addanswerform to add new answer
def addanswer(request):
    """Processes an addanswerform from a POST request"""
    if request.method == "POST":
        answerform = AddAnswerForm(data=request.POST)
        if answerform.is_valid():
            answerform.save()
            return redirect('/quizzes/addquestion')
    # Redirect to main askquestion page if not a POST request
    else:
        return redirect('/quizzes/addquestion')

# Process POST request addquizform to add new quiz
def addquiz(request):
    """Processes an addquizform from a POST request"""
    if request.method == "POST":
        quizform = AddQuizForm(data=request.POST)
        if quizform.is_valid():
            quizform.save()
            return redirect('/quizzes/addquestion')
    else:
        return redirect('/quizzes/addquestion')

# Processes a POST request modelformset of answerresults and submits the user answers to database
def submitanswer(request, quiz_id, question_id):
    """ Processes a answerresult_formset POST request and creates them as AnswerResult objects"""
    if request.method == "POST":
        # Only logged in users can submit answers
        if request.user.is_authenticated():
            try:
                # Check if there is exactly one quizresult which is unfinished
                QuizResult.objects.get(quiz__id=quiz_id, user=request.user, finished=False)
                answerresult_formset = modelformset_factory(AnswerResult, AnswerResultForm, extra=1)
                formset = answerresult_formset(request.POST)
                # Check that the formset has the right inputs
                if formset.is_valid():
                    # We save the formset, but do not commit, as we need further validation
                    new_formset = formset.save(commit=False)
                    # We now check that for each answer, there is exactly one valid answer result
                    for form in new_formset:
                        # Check that the user submitted the right quiz and question
                        if form.quiz.id == long(quiz_id) and form.question.id == long(question_id):
                            # Ensure that the submitted form has the correct user
                            form.user = request.user
                            # If the user has already submitted such an answer, DELETE it. The user is allowed to change their answers 
                            # as long as the quiz has not been submitted
                            if AnswerResult.objects.filter(quiz__id=quiz_id, question__id=question_id, user=request.user, answer=form.answer):
                                AnswerResult.objects.filter(quiz__id=quiz_id, question__id=question_id, user=request.user, answer=form.answer).delete()
                            # After this validation, save the updated form. This submits the answerresult into the database, for each answer
                            form.save()
                        else:
                            context = {'error': "Invalid answer submission."}
                            return render(request, 'quizsite/error.html', context)
                    # If the answer is submitted successfully, it will direct you to the next question in the quiz.
                    try:
                        quiz = get_object_or_404(Quiz, pk=quiz_id)
                        question = get_object_or_404(Question, pk=question_id)
                        next_question = Question.objects.get(quiz__id=quiz.id, questionordering__ordering=(question.questionordering_set.get(quiz_id=quiz.id).ordering+1))
                        return redirect('/quizzes/{}/{}'.format(str(quiz_id), str(next_question.id)))
                    # If there is no valid next question, send the user to the endofquiz pagen
                    except:
                        return redirect('/quizzes/{}/endofquiz'.format(str(quiz_id)))
                context = {'error': formset.errors}
                return render(request, 'quizsite/error.html', context)
            # If not exactly one valid quizresult, we check what the issue is, and display that error.
            except:
                try:
                    QuizResult.objects.get(quiz__id=quiz_id, user=request.user, finished=True)
                    context = {'error': "You have already submitted this quiz attempt. If you are eligible to retake this quiz, contact the administrator."}
                    return render(request, 'quizsite/error.html', context)
                except:
                    context = {'error': "There is not a valid quiz attempt available. You have either not begun this quiz, or there is an error and there is more than one quizzes."}
                    return render(request, 'quizsite/error.html', context)

        else:
            context = {'error': "You must be logged in to submit an answer"}
            return render(request, 'quizsite/error.html', context)
    #This page only accepts post requests
    else:
        return redirect('/')

#Displays a page to register a new user, or process the request to register a new user
def register(request):
    """Displays page to register new users, or processes a UserCreation POST request"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/')
        else:
            context = {'error': form.errors}
            return render(request, 'quizsite/error.html', context)
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)


# This page allows the user to submit a bug report, or it processes a submitted bug report 
# POST request and redirects the user to the home page.
def bugreport(request):
    """This page displays a bug report form, and processes a submitted bug report form"""
    if request.method == 'POST':
        # Only logged in users can submit bug reports
        if request.user.is_authenticated():
            bugreport = BugReportForm(request.POST)
            # We ensure that the bugreport has the current user and time
            bugreport.user = request.user
            bugreport.timestamp = datetime.now()
            if bugreport.is_valid():
                bugreport.save()
                # If bug is reported, sends user back to home page
                return redirect('/')
            else:
                context = {'error': bugreport.errors}
                return render(request, 'quizsite/error.html', context)
        else:
            context = {'error': "You must be logged in to submit a bug report"}
            return render(request, 'quizsite/error.html', context)
    else:
        bugreportform = BugReportForm(initial={'user': request.user, 'timestamp': datetime.now()})
        context = {
                'bugreportform': bugreportform,
                }
        return render(request, 'quizsite/bugreport.html', context)


# This page is for superusers, and displays a table of all submitted bug reports
def viewbugreports(request):
    """Superusers use this page to view all submitted bug reports"""
    if request.user.is_authenticated and request.user.is_superuser:
        bugreport_list = BugReport.objects.all()
        context = {'bugreport_list': bugreport_list}
        return render(request, 'quizsite/viewbugreports.html', context)
