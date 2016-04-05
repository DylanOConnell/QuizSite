from django.conf.urls import include, url
from quizsite import views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.home, name = "home"),
# More info on what the below includes is described here
# https://docs.djangoproject.com/en/1.8/topics/auth/default/#module-django.contrib.auth.views
    url(r'', include('django.contrib.auth.urls')),
    url(r'^quizzes/', include('quizcreator.urls', namespace = "quizzes", app_name = 'quizcreator')),
    url(r'^account/', include('quizsite.account_urls', namespace = "account", app_name = 'account')),
#    url(r'^register/$', views.register, name='register'),
]
