"""
URL configuration for litracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('home/', include("book.urls")),
    path('', include('authentication.urls')),
    path('upvote_book/', include('upvote_book.urls')),
    path('review_book/', include('review_book.urls')),
    path('reading_history/', include('reading_history.urls')),
    # path('favorite_book/', include('favorite_book.urls')),
    path('admin/', admin.site.urls),
]
