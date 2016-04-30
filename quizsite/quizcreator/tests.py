# This file implements Django's unittests. These will be run in a sqlite database, 
# and will test the functionality of our models, views, and forms
from django.test import TestCase, Client, RequestFactory
from quizsite.views import *
from quizcreator.models import *
from quizsite.forms import *


# Tests our models in the database, and their expected properties
class QuizModelsTestCase(TestCase):
        """This testcase covers the models in our database"""
        def setUp(self):
            """Create a sample database of our objects for testing"""
            Quiz.objects.create(name="General Knowledge")
            Quiz.objects.create(name="Haverford College Trivia")
            Question.objects.create(text="When was Haverford founded?")
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="Haverford College Trivia"), question=Question.objects.get(text="When was Haverford founded?"))
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="General Knowledge"), question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1823", correct_type="PART_W", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1833", correct_type="COR", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="2012", correct_type="FULL_W", question=Question.objects.get(text="When was Haverford founded?"))

        def test_existence(self):
            """Test whether the Django objects are created and have the right attributes"""
            genquiz = Quiz.objects.get(name="General Knowledge")
            hcquiz = Quiz.objects.get(name="Haverford College Trivia")
            hcquestion1 = Question.objects.get(text="When was Haverford founded?")
            hcanswer1 = Answer.objects.get(text="2012")
            hcquestion1 = Question.objects.get(text="When was Haverford founded?")
            self.assertEqual(genquiz.name, "General Knowledge")
            self.assertEqual(hcquiz.name, "Haverford College Trivia")
            self.assertEqual(hcquestion1.text, "When was Haverford founded?")
            self.assertEqual(hcanswer1.text, "2012")

# We test the views that cover the beginning and ending of a quiz. Each test covers the functionality of 
# that specific view.
class BeginEndQuizViewsTestCase(TestCase):
        """This TestCase tests the view relating to beginning and ending quizzes"""
        def setUp(self):
            """Create a sample database of our objects for testing"""
            Quiz.objects.create(name="General Knowledge")
            Quiz.objects.create(name="Haverford College Trivia")
            Question.objects.create(text="When was Haverford founded?")
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="Haverford College Trivia"), question=Question.objects.get(text="When was Haverford founded?"))
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="General Knowledge"), question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1823", correct_type="PART_W", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1833", correct_type="COR", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="2012", correct_type="FULL_W", question=Question.objects.get(text="When was Haverford founded?"))
            self.factory = RequestFactory()
            User.objects.create_user(username='testuser', password='testuser')
            self.client = Client()

        def test_view_quizzes(self):
            """Test functionality of the quizzes view"""
            resp = self.client.get('/quizzes/')
            self.assertEqual(resp.status_code, 200)
            self.assertTrue('quizzes_list' in resp.context)
            self.assertEqual(resp.context['quizzes_list'].first(), Quiz.objects.get(name="General Knowledge"))
            self.assertEqual(resp.context['quizzes_list'].last(), Quiz.objects.get(name="Haverford College Trivia"))

        def test_view_beginquiz(self):
            """Test the beginquiz view """
            user = User.objects.get(username='testuser')
            self.client.login(username=user.username, password='testuser')
            genquiz = Quiz.objects.get(pk=1)
            request = self.factory.get('/quizzes/{}/beginquiz'.format(genquiz.id))
            request.user = user
            response = endofquiz(request, 1)
            self.assertEqual(response.status_code, 200)
            resp = self.client.get('/quizzes/1/beginquiz')
            self.assertEqual(resp.context['user'], user)
            self.assertEqual(resp.context['quiz'], genquiz)
            self.assertTrue('quizresultform' in resp.context) 

        def test_view_endofquiz(self):
            """Test the endofquiz view """
            user = User.objects.get(username='testuser')
            self.client.login(username=user.username, password='testuser')
            genquiz = Quiz.objects.get(pk=1)
            request = self.factory.get('/quizzes/{}/beginquiz'.format(genquiz.id))
            request.user = user
            response = endofquiz(request, 1)
            self.assertEqual(response.status_code, 200)
            resp = self.client.get('/quizzes/1/endofquiz')
            self.assertEqual(resp.context['user'], user)
            self.assertEqual(resp.context['quiz'], genquiz)
            self.assertEqual(resp.context['first_question'], Question.objects.all().first())


# These tests cover the views related to taking the quiz as a user
class QuizzesViewsTestCase(TestCase):
        """This TestCase tests the view relating to taking the quiz itself"""
        def setUp(self):
            """Create a sample database of our objects for testing"""
            Quiz.objects.create(name="General Knowledge")
            Quiz.objects.create(name="Haverford College Trivia")
            Question.objects.create(text="When was Haverford founded?")
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="Haverford College Trivia"), question=Question.objects.get(text="When was Haverford founded?"))
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="General Knowledge"), question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1823", correct_type="PART_W", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1833", correct_type="COR", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="2012", correct_type="FULL_W", question=Question.objects.get(text="When was Haverford founded?"))
            Question.objects.create(text="Who is your favorite professor?")
            QuestionOrdering.objects.create(ordering=2, quiz=Quiz.objects.get(name="General Knowledge"), question=Question.objects.get(text="Who is your favorite professor?"))
            Answer.objects.create(text="Einstein", correct_type="PART_W", question=Question.objects.get(text="Who is your favorite professor?"))
            Answer.objects.create(text="Phil Adler", correct_type="COR", question=Question.objects.get(text="Who is your favorite professor?"))
            Answer.objects.create(text="Genghis Khan", correct_type="FULL_W", question=Question.objects.get(text="Who is your favorite professor?"))
            self.factory = RequestFactory()
            User.objects.create_user(username='testuser', password='testuser')
            self.client = Client()

        def test_view_question(self):
            """Test the question view """
            user = User.objects.get(username='testuser')
            self.client.login(username=user.username, password='testuser')
            genquiz = Quiz.objects.get(pk=1)
            yearquestion = Question.objects.get(pk=1)
            request = self.factory.get('/quizzes/{}/{}/'.format(genquiz.id, yearquestion.id))
            request.user = user
            response = question(request, genquiz.id, yearquestion.id)
            self.assertEqual(response.status_code, 200)
            resp = self.client.get('/quizzes/{}/{}/'.format(genquiz.id, yearquestion.id))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.context['user'], user)
            self.assertEqual(resp.context['quiz'], genquiz)
            self.assertEqual(resp.context['question'], yearquestion)
            self.assertEqual(resp.context['curr_question_number'], 1)
            self.assertEqual(resp.context['next_question_number'], 2)
            self.assertEqual(resp.context['prev_question_number'], None)
            self.assertTrue('formset' in resp.context) 
            self.assertTrue('formset_answers' in resp.context) 
            self.assertTrue('answer_list' in resp.context) 


# These tests cover the functionality of superusers adding content to the quizzes.
class AddToQuizViewsTestCase(TestCase):
        """This TestCase tests the view that allows for the creation of quizzes, questions, and answers, 'addquestion' """
        def setUp(self):
            """Create a sample database of our objects for testing"""
            Quiz.objects.create(name="General Knowledge")
            Quiz.objects.create(name="Haverford College Trivia")
            Question.objects.create(text="When was Haverford founded?")
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="Haverford College Trivia"), question=Question.objects.get(text="When was Haverford founded?"))
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="General Knowledge"), question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1823", correct_type="PART_W", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1833", correct_type="COR", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="2012", correct_type="FULL_W", question=Question.objects.get(text="When was Haverford founded?"))
            Question.objects.create(text="Who is your favorite professor?")
            QuestionOrdering.objects.create(ordering=2, quiz=Quiz.objects.get(name="General Knowledge"), question=Question.objects.get(text="Who is your favorite professor?"))
            Answer.objects.create(text="Einstein", correct_type="PART_W", question=Question.objects.get(text="Who is your favorite professor?"))
            Answer.objects.create(text="Phil Adler", correct_type="COR", question=Question.objects.get(text="Who is your favorite professor?"))
            Answer.objects.create(text="Genghis Khan", correct_type="FULL_W", question=Question.objects.get(text="Who is your favorite professor?"))
            self.factory = RequestFactory()
            User.objects.create_superuser(username='testuser', password='testuser', email='testuser@email.com')
            self.client = Client()

        def test_view_addquestion(self):
            """Verify that the addquestion view returns a response with the proper forms when accessed by a user """
            user = User.objects.get(username='testuser', is_superuser=True)
            self.client.login(username=user.username, password='testuser')
            genquiz = Quiz.objects.get(pk=1)
            yearquestion = Question.objects.get(pk=1)
            request = self.factory.get('/quizzes/addquestion/')
            request.user = user
            response = addquestion(request)
            self.assertEqual(response.status_code, 200)
            resp = self.client.get('/quizzes/addquestion')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.context['user'], user)
            self.assertTrue('quizform' in resp.context) 
            self.assertTrue('answerform' in resp.context) 
            self.assertTrue('questionform' in resp.context) 


#These tests cover the functionality of the other miscellaneous pages used by the site
class UserMiscViewsTestCase(TestCase):
        """This TestCase tests the views that handle miscellaneous tasks, bugreport and register """
        def test_view_bugreport(self):
            """Verify that bugreport returns the proper response when accessed by a user """
            self.factory = RequestFactory()
            User.objects.create_user(username='testuser', password='testuser')
            c = Client()
            user = User.objects.get(username='testuser')
            newbugreport = BugReport.objects.create(user=user, report="Why doesn't it use Javascript?")
            c.login(username=user.username, password='testuser')
            request = self.factory.get('/quizzes/bugreport/')
            request.user = user
            response = bugreport(request)
            self.assertEqual(response.status_code, 200)
            resp = c.get('/quizzes/bugreport')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.context['user'], user)
            self.assertTrue('bugreportform' in resp.context) 


# These tests cover the views used by superusers to view the scored quiz results of users.
# each test covers the functionality of a different view.
class CheckResultsViewsTestCase(TestCase):
        """This TestCase tests the views for checking quiz results """
        def setUp(self):
            """Create a sample database of our objects for testing"""
            Quiz.objects.create(name="General Knowledge")
            Quiz.objects.create(name="Haverford College Trivia")
            Question.objects.create(text="When was Haverford founded?")
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="Haverford College Trivia"), question=Question.objects.get(text="When was Haverford founded?"))
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="General Knowledge"), question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1823", correct_type="PART_W", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1833", correct_type="COR", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="2012", correct_type="FULL_W", question=Question.objects.get(text="When was Haverford founded?"))
            Question.objects.create(text="Who is your favorite professor?")
            QuestionOrdering.objects.create(ordering=2, quiz=Quiz.objects.get(name="General Knowledge"), question=Question.objects.get(text="Who is your favorite professor?"))
            Answer.objects.create(text="Einstein", correct_type="PART_W", question=Question.objects.get(text="Who is your favorite professor?"))
            Answer.objects.create(text="Phil Adler", correct_type="COR", question=Question.objects.get(text="Who is your favorite professor?"))
            Answer.objects.create(text="Genghis Khan", correct_type="FULL_W", question=Question.objects.get(text="Who is your favorite professor?"))
            self.factory = RequestFactory()
            User.objects.create_superuser(username='testuser', password='testuser', email='testuser@email.com')
            self.client = Client()

        def test_view_listquizresults(self):
            """Verify that the listquizresults view returns a response with the proper forms when accessed by a user """
            user = User.objects.get(username='testuser', is_superuser=True)
            self.client.login(username=user.username, password='testuser')
            genquiz = Quiz.objects.get(pk=1)
            yearquestion = Question.objects.get(pk=1)
            request = self.factory.get('/quizzes/listquizresults/')
            request.user = user
            response = addquestion(request)
            self.assertEqual(response.status_code, 200)
            resp = self.client.get('/quizzes/listquizresults')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.context['user'], user)
            self.assertTrue('quizzes_list' in resp.context) 
            
        def test_view_checkquizresults(self):
            """Verify that the checkquizresults view returns a response with the proper forms when accessed by a user """
            user = User.objects.get(username='testuser', is_superuser=True)
            self.client.login(username=user.username, password='testuser')
            genquiz = Quiz.objects.get(pk=1)
            yearquestion = Question.objects.get(pk=1)
            request = self.factory.get('/quizzes/{}/checkresults/'.format(genquiz.id))
            request.user = user
            response = addquestion(request)
            self.assertEqual(response.status_code, 200)
            resp = self.client.get('/quizzes/{}/checkresults'.format(genquiz.id))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.context['user'], user)
            self.assertEqual(resp.context['quiz'], genquiz)
            self.assertTrue('user_list' in resp.context) 

        def test_view_quizresults(self):
            """Verify that the quizresults view returns a response with the proper forms when accessed by a user """
            user = User.objects.get(username='testuser', is_superuser=True)
            self.client.login(username=user.username, password='testuser')
            genquiz = Quiz.objects.get(pk=1)
            yearquestion = Question.objects.get(pk=1)
            request = self.factory.get('/quizzes/{}/{}/quizresults/'.format(genquiz.id, user.username))
            request.user = user
            response = addquestion(request)
            self.assertEqual(response.status_code, 200)
            resp = self.client.get('/quizzes/{}/{}/quizresults'.format(genquiz.id, user.username))
            self.assertEqual(resp.status_code, 200)
            self.assertTrue('error' in resp.context) # there there is no valid quizresult, so this correctly throws error
            QuizResult.objects.create(user=user, quiz=genquiz, score=0, finished=True)
            request = self.factory.get('/quizzes/{}/{}/quizresults/'.format(genquiz.id, user.username))
            request.user = user
            response = addquestion(request)
            self.assertEqual(response.status_code, 200)
            resp = self.client.get('/quizzes/{}/{}/quizresults'.format(genquiz.id, user.username))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.context['error'], 'There is not exactly one submitted answer for Quiz: General Knowledge, Question: Question #: 1. Answer: 1823') 

