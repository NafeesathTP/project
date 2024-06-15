from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('property_details/', views.property_details, name='property_details'),
    path('search/', views.search_results, name='search_results'),
    path('house/',views.house_list,name='house_list'),
    path('apartment/',views.apartment_list,name='apartment_list'),
    path('land/',views.land_list,name='land_list'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),
    path('about/',views.about,name='about'),
    path('favorites/', views.favorites, name='favorites'),
    path('view_favorites/', views.favorites, name='view_favorites'),
    path('contacts/', views.contacts, name='contacts'),

]
