from django.urls import path

from trainer.views import TrainerMessageCreateView, TrainerMessageUpdateView, TrainerMessageDeleteView

app_name = 'trainer'

urlpatterns = [
    path('create_trainer/', TrainerMessageCreateView.as_view(), name='create_trainer'),
    path('edit_trainer/<pk>/', TrainerMessageUpdateView.as_view(), name='edit_trainer'),
    path('delete_trainer/<pk>', TrainerMessageDeleteView.as_view(), name='delete_trainer')

]
