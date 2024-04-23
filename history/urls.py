from django.urls import path

from history.apps import HistoryConfig
from history.views import HistoryList, HistoryCreate, HistoryUpdate, HistoryDelete

app_name = HistoryConfig.name

urlpatterns = [
    path('', HistoryList.as_view(), name='history'),
    path('history_create', HistoryCreate.as_view(), name='history_create'),
    path('history_update/<int:pk>', HistoryUpdate.as_view(), name='history_update'),
    path('history_delete/<int:pk>', HistoryDelete.as_view(), name='history_delete'),

]
