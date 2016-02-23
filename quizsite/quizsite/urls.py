from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'quizsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.login, name='login'),
    url(r'^quizzes/)$', views.quizzes, name='quizzes'),
    url(r'^(P?<quiz_id>[0-9]+)/(P?<question_id>[0-9]+)/$', views.question, name='question'),
    url(r'^(P?<quiz_id>[0-9]+)/results/$', views.results, name='results'),



]
