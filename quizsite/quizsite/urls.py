from django.conf.urls import include, url
#from . import views
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'quizsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
#    url(r'^login/$', views.login, name='login'),
    url(r'^quizzes/', include('quizcreator.urls', namespace = "quizzes", app_name =' quizcreator')),
#    url(r'^createquestion/$', views.createquestion, name='createquestion'),
#    url(r'^(?P<quiz_id>[0-9]+)/results/$', views.results, name='results'),



]
