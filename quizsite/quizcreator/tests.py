from django.test import TestCase
from quizcreator.models import *

class QuizTestCase(TestCase):
        def setUp(self):
            """Create a sample database of our objects for testing"""
            Quiz.objects.create(name="General Knowledge")
            Quiz.objects.create(name="Haverford College Trivia")
            Question.objects.create(text="When was Haverford founded?")
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="Haverford College Trivia"), question = Question.objects.get(text="When was Haverford founded?"))
            QuestionOrdering.objects.create(ordering=1, quiz=Quiz.objects.get(name="General Knowledge"), question = Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1823",correct_type="PART_W", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="1833",correct_type="COR", question=Question.objects.get(text="When was Haverford founded?"))
            Answer.objects.create(text="2012",correct_type="FULL", question=Question.objects.get(text="When was Haverford founded?")h

        def test_existence(self):
        """Test whether the Django objects are created and have the right attributes"""
            genquiz = Quiz.objects.get(name="General Knowledge")
            hcquiz = Quiz.objects.get(name="Haverford College Trivia")
            hcquestion1 = Question.objects.get(text="When was Haverford founded?")
            self.assertEqual(genquiz.name, "General Knowledge")
            self.assertEqual(hcquiz.name, "Haverford College Trivia")
