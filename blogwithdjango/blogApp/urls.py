from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about , name="about"),
    path('category/<slug:slug>/', views.category, name='category'),
    path("single-audio/<slug:slug>/", views.singleaudio, name="single-audio"),
    path("single-video/<slug:slug>/", views.singlevideo, name="single-video"),
    path("contact", views.contact, name="contact"),
    path("styles", views.styles, name="styles"),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('videos/', views.video_articles, name='video-articles'),
    path('audios/', views.audio_articles, name='audio-articles'),
    path('standard/', views.Standard_articles, name='standard-articles'),
    path('search/', views.search_view, name='search'),

    

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)