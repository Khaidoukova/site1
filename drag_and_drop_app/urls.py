from django.urls import path
from drag_and_drop_app.views import create_pdf, DragAndDropAppView, ImageListView, ImageUpdate
from django.conf import settings
from django.conf.urls.static import static

app_name = 'drag_and_drop_app'

urlpatterns = [
    path('', DragAndDropAppView.as_view(), name='drag_and_drop_app'),
    path('create_pdf/', create_pdf, name='create_pdf'),
    path('image_list/', ImageListView.as_view(), name='image_list'),
    path('image_update/<int:pk>', ImageUpdate.as_view(), name='image_update'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
