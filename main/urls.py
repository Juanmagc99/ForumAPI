
from django.urls import path
from .views import SavedThreadView


urlpatterns = [
    path("saved_thread/", SavedThreadView.as_view()),
    path("saved_thread/<int:pk>/", SavedThreadView.as_view()),
]