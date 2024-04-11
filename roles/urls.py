from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from roles.views import CreateJudgeView, create_conductor, add_dog_conductor, CreateOrganizationView, \
    CreateCompetitorView, search_dogs, CompetitorDeleteView, CompetitorUpdateView

app_name = 'roles'

urlpatterns = [
    path('create_judge/', CreateJudgeView.as_view(), name='create_judge'),
    path('create_conductor/', create_conductor, name='create_conductor'),
    path('add_dog_conductor/', add_dog_conductor, name='add_dog_conductor'),

    path('detail/<int:pk>/', CreateCompetitorView.as_view(), name='competitor_form'),  # Добавляется участником

    path('delete_competitor/<int:pk>', CompetitorDeleteView.as_view(), name='competitor_confirm_delete'),  # Удаление из участия
    path('competitor_detail/<int:pk>', CompetitorUpdateView.as_view(), name='competitor_detail'),  # страница участника, результаты, оценки

    path('search_dogs/', search_dogs, name='search_dogs'),

    path('create_organization/', CreateOrganizationView.as_view(), name='create_organization'),
]


