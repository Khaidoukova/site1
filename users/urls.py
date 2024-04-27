from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.search_view import SearchListUsersView, SearchListDogsView, SearchListJudgeView
from users.views import RegisterView, ProfileView, generate_new_password, DogsCreate, UserDetailView, verify_email, \
    UserLoginView, SearchListView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('verify/<str:key>/', verify_email, name='verify_email'),
    path('user_detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('search_list', SearchListView.as_view(), name='search_list'),  # Представление для страницы поиска выбор
    path('search_list_users', SearchListUsersView.as_view(), name='search_list_users'),  # Поиск юзеров
    path('search_list_dogs', SearchListDogsView.as_view(), name='search_list_dogs'),  # Поиск собак
    path('search_list_judge', SearchListJudgeView.as_view(), name='search_list_judge'),  # Поиск судей

]
