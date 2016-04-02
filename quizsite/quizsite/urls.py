from django.conf.urls import include, url
from quizsite import views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.home, name = "home"),
#    url(r'^login/$',views.login, name = "login"),
    url(r'', include('django.contrib.auth.urls')),
#    url(r'^login/$', views.login, name='login'),
    url(r'^quizzes/', include('quizcreator.urls', namespace = "quizzes", app_name = 'quizcreator')),
]
