from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from main.models import Competition
from roles.models import Competitor, Conductor
from users.models import User, Dogs


class CompetitorAddView(View):
    template_name = 'competitor_add.html'

    def get(self, request, pk):
        """Отображение формы добавления участника"""
        user = User.objects.get(pk=pk)  # Передаем юзера
        current_user = request.user  # Передаем текущего юзера

        if current_user.is_staff:  # если юзер персонал
            competitions = Competition.objects.all()  # то показываем все соревнования
        else:  # если нет, то
            competitions = Competition.objects.filter(owner=current_user.pk)  # фильруем соревнования по организатору(текущему юзеру)

        # Получаем объект проводника текущего пользователя
        conductor = get_object_or_404(Conductor, user=current_user)

        # Получаем все собаки проводника
        user_dogs = conductor.dogs.all()

        return render(request, self.template_name, {'user': user, 'current_user': current_user, 'user_dogs': user_dogs,
                                                    'competitions': competitions})

    def post(self, request, pk):
        """Обработка отправленной формы"""
        # Получаем поля пост запроса
        class_comp = request.POST.get('class_comp')
        user_dog_id = request.POST.get('user_dog')
        competition_id = request.POST.get('competition')
        competitior_vnezachet = request.POST.get('vnezachet', False) == 'true'
        # Сопоставляем с необходимыми нам полями
        user = User.objects.get(pk=pk)
        conductor = get_object_or_404(Conductor, user=user)
        user_dog = get_object_or_404(Dogs, pk=user_dog_id)
        competition = get_object_or_404(Competition, pk=competition_id)  # Получаем объект Competition
        # Создаем участника
        Competitor.objects.create(
            user=user,
            competition=competition,
            class_comp=class_comp,
            conductor=conductor,
            selected_dog=user_dog,
            competitior_vnezachet=competitior_vnezachet

        )

        return redirect('detail_com', pk=competition_id)

