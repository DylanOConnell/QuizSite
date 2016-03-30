from django.conf.urls import include, url

from quizsite import views

urlpatterns = [
    url(r'^$', views.quizzes, name='quizzes'),
    url(r'^(?P<quiz_id>[0-9]+)/(?P<question_id>[0-9]+)/$', views.question, name='question'),
    url(r'^addquestion$', views.addquestion, name='addquestion'),

#    url(r'^polls/', include('polls.urls')),
#    url(r'^admin/', include(admin.site.urls)),
]

