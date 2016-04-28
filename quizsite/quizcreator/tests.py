from django.test import TestCase
from quizcreator.models import *

class QuizTestCase(TestCase):
        def setUp(self):
            Quiz.objects.create(name="General Knowledge")
            Quiz.objects.create(name="Haverford College Trivia")


        def test_existence(self):
            genquiz = Quiz.objects.get(name="General Knowledge")
            hcquiz = Quiz.objects.get(name="Haverford College Trivia")
            self.assertEqual(genquiz.name, "General Knowledge")
            self.assertEqual(gen
