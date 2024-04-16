from django.urls import path
from main.views import CompetitionCreate, CompetitionList, CompetitionDelete, CompetitionUpdate, CompetitionDetail, \
    CompetitionResult, RulesView

urlpatterns = [
    path('', CompetitionList.as_view(), name='index'),

    path('create_com', CompetitionCreate.as_view(), name='create_com'),  # Создание соревнования
    path('update/<int:pk>', CompetitionUpdate.as_view(), name='update_com'),  # Изменения соревнование
    path('delete/<int:pk>', CompetitionDelete.as_view(), name='delete_com'),  # Удаление соревнования
    path('detail/<int:pk>', CompetitionDetail.as_view(), name='detail_com'),  # Детали , вьюлист соревнования
    path('competition_result/<int:pk>', CompetitionResult.as_view(), name='competition_result'),  # страница результатов соревнования

    path('rules/', RulesView.as_view(), name='rules'),  # страница с правилами
]
