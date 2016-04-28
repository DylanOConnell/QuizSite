from django.test import TestCase
from quizcreator.models import *


class QuizTestCase(TestCase):
    def setUp(self):
        Quiz.objects.create(name="General Knowledge")

    def test_existence(self):
        genquiz = Quiz.objects.get(name="General Knowledge")
        self.assertEqual(genquiz.name, "GeneralKnowledge")

