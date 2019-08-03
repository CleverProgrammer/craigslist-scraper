"""test_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from css import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from my_app import views
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home_page'),
    path('css/', include('my_app.urls')),
    path('admin/', admin.site.urls),
    path('new-search/', views.new_search, name='new_search'),
]
