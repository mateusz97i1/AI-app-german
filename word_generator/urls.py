from django.urls import path
from . import views

app_name='word_generator'

urlpatterns = [
    path('',views.home,name="home"),
    path('learn',views.learn_words,name="learn_word"),
  path('dictionary/', views.dictionary_view, name='dictionary'),
    path('dictionary/api/', views.autocomplete_api, name='autocomplete')
]

    

