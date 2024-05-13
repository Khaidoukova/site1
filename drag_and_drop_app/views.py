import base64
import json
import os
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, DeleteView

from .forms import ImageUpdateForm
from .models import Image
from .pdf_creator import create_dog_owner_pdf
from django.http import JsonResponse


class DragAndDropAppView(View):

    def get(self, request):
        pk = request.GET.get('pk')  # Получаем pk из параметров запроса
        # Создаем экземпляр формы
        return render(request, 'drag_and_drop_app.html', {'competition_id': pk})

    def post(self, request):
        if request.method == 'POST' and request.POST.get('image_data') and request.POST.get('image_name'):
            try:
                image_data = request.POST['image_data']
                image_name = request.POST['image_name']
                image_list = request.POST['image_list']  # Получаем содержимое поля "image-list"

                # Преобразуем данные изображения обратно в формат изображения
                img_data = base64.b64decode(image_data.split(',')[1])

                # Путь для сохранения изображения
                save_path = os.path.join('media', image_name)

                # Если изображение с таким именем уже существует, добавляем к имени порядковый номер
                count = 1
                while os.path.exists(save_path):
                    name, ext = os.path.splitext(image_name)
                    image_name = f"{name}_{count}{ext}"
                    save_path = os.path.join('media', image_name)
                    count += 1

                # Сохраняем изображение
                with open(save_path, 'wb') as f:
                    f.write(img_data)
                image_url = request.build_absolute_uri(save_path)
                # Выводим ссылку на изображение в терминал
                # print("Image URL:", image_url)
                # Создаем экземпляр класса Image и сохраняем его в базе данных
                image_instance = Image.objects.create(
                    user=request.user,  # текущий пользователь
                    file_link=image_url,  # или другое поле, если требуется
                    image_name=image_name,
                    image_list=image_list,
                    # другие поля, если требуется
                )

                return JsonResponse({'message': 'Image saved successfully', 'image_name': image_name})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No image data or image name found in the request'}, status=400)


def create_pdf(request):
    owner = 'Иван Иванович'
    dog = 'Тузик'
    dog_classes = 'РО-Дети', 'РО-Старики'
    judge = 'Петр Петрович'
    competition = 'Чемпионат по рыбной ловле'
    signs = ['знак_1', 'знак_2', 'знак_3']

    # Создание PDF-файла с помощью функции create_dog_owner_pdf
    pdf_file = create_dog_owner_pdf(owner, dog, dog_classes, judge, competition, signs)

    # Открытие файла в новой вкладке браузера
    with open(pdf_file, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="dog_owner.pdf"'
    return response


class ImageListView(ListView):
    """Просмотр списка всех созданных трасс"""
    model = Image
    template_name = 'image_list.html'
    context_object_name = 'image_list'

    def get_queryset(self):
        # Получаем QuerySet всех объектов Image, отсортированных по полю pk в обратном порядке
        queryset = super().get_queryset().order_by('-pk')
        return queryset


class ImageDeleteView(DeleteView):
    """Удаление трассы"""
    model = Image
    template_name = 'image_confirm_delete.html'
    success_url = reverse_lazy('drag_and_drop_app:image_list')

    def delete(self, request, *args, **kwargs):
        # Получаем объект Image
        self.object = self.get_object()
        print(self.object.file_link)
        # Удаляем файл изображения, если он существует
        if self.object.file_link:
            if os.path.exists(self.object.file_link):
                os.remove(self.object.file_link)

        # Удаляем объект Image
        self.object.delete()

        return super().delete(request, *args, **kwargs)


class ImageUpdate(UpdateView):
    model = Image
    template_name = 'image_update.html'
    form_class = ImageUpdateForm
    context_object_name = 'image_info'
    success_url = reverse_lazy('drag_and_drop_app:image_list')

    def get_success_url(self):
        return self.success_url





