from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
    path('profiles/preferences/', views.PreferenceList.as_view()),
    path('profiles/preferences/<int:pk>/', views.PreferenceDetail.as_view()),
]
