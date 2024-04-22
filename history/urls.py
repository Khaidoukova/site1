from django.urls import path

from history.apps import HistoryConfig
from history.views import HistoryList, HistoryCreate

app_name = HistoryConfig.name

urlpatterns = [
    path('', HistoryList.as_view(), name='history'),
    path('history_create', HistoryCreate.as_view(), name='history_create')

]
