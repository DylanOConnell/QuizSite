from django.conf.urls import include, url
from quizsite import views

urlpatterns = [
    url(r'^$', views.quizzes, name='quizzes'),
    url(r'^(?P<quiz_id>[0-9]+)/(?P<question_id>[0-9]+)/$', views.question, name='question'),
    url(r'^addquestion$', views.addquestion, name='addquestion'),
#    url(r'^(?P<quiz_id>[0-9]+)/startquiz$', views.startquiz, name='startquiz'),
    url(r'^(?P<quiz_id>[0-9]+)/beginquiz$', views.beginquiz, name='beginquiz'),
    url(r'^(?P<quiz_id>[0-9]+)/finishquiz$', views.finishquiz, name='finishquiz'),
    url(r'^(?P<quiz_id>[0-9]+)/checkresults$', views.checkresults, name='checkresults'),
    url(r'^(?P<quiz_id>[0-9]+)/(?P<username>\w+)/quizresults$', views.quizresults, name='quizresults'),
    url(r'^addanswer$', views.addanswer, name='addanswer'),
    url(r'^addquiz$', views.addquiz, name='addquiz'),
    url(r'^(?P<quiz_id>[0-9]+)/(?P<question_id>[0-9]+)/submitanswer$', views.submitanswer, name='submitanswer'),
]

