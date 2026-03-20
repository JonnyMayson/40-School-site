"""
URL configuration for qundylyq_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from content import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('team/<int:category_id>/', views.team_detail, name='team_detail'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('api/update-image/', views.update_image_url, name='update_image_url'),
    path('api/create-hero/', views.create_hero_block, name='create_hero_block'),
    path('api/clear-image/', views.clear_image_url, name='clear_image_url'),
    path('api/update-text/', views.update_text, name='update_text'),
    path('api/update-site-settings/', views.update_site_settings, name='update_site_settings'),
    path('api/update-section-order/', views.update_section_order, name='update_section_order'),
    path('api/update-section-bg/', views.update_section_bg, name='update_section_bg'),
    path('api/toggle-section/', views.toggle_section, name='toggle_section'),
    path('api/update-element-style/', views.update_element_style, name='update_element_style'),
    path('api/update-section-card-bg/', views.update_section_card_bg, name='update_section_card_bg'),
    path('api/create-element/', views.create_element, name='create_element'),
    path('api/delete-element/', views.delete_element, name='delete_element'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
