from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from config.settings import EMAIL_HOST_USER
from main.models import Competition
from roles.forms import CreateCompetitorForm, CompetitorUpdateForm
from roles.models import Judge, Conductor, Competitor, AdditionalScore
from users.models import Dogs, User


class CreateJudgeView(View):
    """Получения юзером статуса организатора"""
    def get(self, request):
        # Логика для обработки GET-запроса
        return render(request, 'create_judge.html')

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            # Создаем нового судью, связанного с текущим пользователем
            new_judge = Judge.objects.create(user=user)
            # Меняем значение поля judge_status на True
            new_judge.judge_status = True
            # Сохраняем изменения
            new_judge.save()
            user_profile_url = reverse('users:user_detail', kwargs={'pk': user.pk})
            # Составляем письмо админу
            message = f'Запрос на получение статуса судьи от пользователя: {user.first_name} {user.last_name}\n' \
                      f'Email: {user.email}\n' \
                      f'Ссылка на профиль: {self.request.build_absolute_uri(user_profile_url)}'

            # Получение адресов электронной почты администраторов или пользователей с нужными статусами
            admin_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)

            # Отправка письма администартору
            send_mail(
                subject='Заявка на получение статуса организатора',
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=admin_emails,
            )

            # Возвращаем ответ или перенаправляем пользователя на другую страницу
            return redirect('users:user_detail', pk=request.user.pk)


def create_conductor(request):
    """Создание проводника"""
    if request.method == 'POST':
        # Создаем проводника, связанного с текущим пользователем
        conductor = Conductor.objects.create(user=request.user)
        conductor.dogs.clear()
        # Если проводник только что создан, устанавливаем его атрибуты
        conductor.save()
        # Редиректим на страницу профиля пользователя после создания проводника
        return redirect('users:user_detail', pk=request.user.pk)

    return render(request, 'create_conductor.html')


def search_dogs(request):
    query = request.GET.get('query', '')
    dogs = Dogs.objects.filter(id_dog__icontains=query) | Dogs.objects.filter(
        home_name__icontains=query) | Dogs.objects.filter(dog_name__icontains=query)

    # Возвращаем JSON-ответ для использования с AJAX
    data = {'html': render_to_string('dog_suggestions.html', {'dogs': dogs})}
    return JsonResponse(data)




# Привязка собаки к проводнику
@login_required
def add_dog_conductor(request):
    if request.method == 'GET':
        dogs = Dogs.objects.all().order_by('-id_dog')
        context = {'dogs': dogs}
        return render(request, 'add_dog_conductor.html', context)

    if request.method == 'POST':
        try:
            conductor = request.user.conductor
        except Conductor.DoesNotExist:
            conductor = Conductor(user=request.user)

        id_dog = request.POST.get('id_dog')
        if not id_dog:
            messages.error(request, 'ID собаки не был передан')
            dogs = Dogs.objects.all().order_by('-id_dog')
            context = {'dogs': dogs}
            return render(request, 'add_dog_conductor.html', context)

        try:
            dog = Dogs.objects.get(id_dog=id_dog)
        except Dogs.DoesNotExist:
            messages.error(request, 'Собака не найдена или не правильно указаны данные')
            dogs = Dogs.objects.all().order_by('-id_dog')
            context = {'dogs': dogs}
            return render(request, 'add_dog_conductor.html', context)

        if dog in conductor.dogs.all():
            messages.error(request, 'Эта собака уже добавлена к проводнику')
            dogs = Dogs.objects.all().order_by('-id_dog')
            context = {'dogs': dogs}
            return render(request, 'add_dog_conductor.html', context)

        conductor.dogs.add(dog)
        messages.success(request, f'Собака {dog} успешно добавлена к проводнику.')
        conductor.save()
        # Редиректим на страницу профиля пользователя после добавления собаки к проводнику
        return redirect('users:user_detail', pk=request.user.pk)

class CreateOrganizationView(View):
    """Получения юзером статуса организатора"""
    def get(self, request):
        # Логика для обработки GET-запроса
        return render(request, 'create_organization.html')

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            # Меняем значение поля get_check на True
            user.get_check = True
            # Сохраняем изменения
            user.save()
            user_profile_url = reverse('users:user_detail', kwargs={'pk': user.pk})
            # Составляем письмо админу
            message = f'Запрос на получение статуса организатора от пользователя: {user.first_name} {user.last_name}\n' \
                      f'Email: {user.email}\n' \
                      f'Ссылка на профиль: {self.request.build_absolute_uri(user_profile_url)}'

            # Получение адресов электронной почты администраторов или пользователей с нужными статусами
            admin_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)

            # Отправка письма администартору
            send_mail(
                subject='Заявка на получение статуса организатора',
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=admin_emails,
            )

            # Возвращаем ответ или перенаправляем пользователя на другую страницу
            return redirect('users:user_detail', pk=request.user.pk)
        # Здесь можно добавить логику для POST-запроса, если нужно
        return render(request, 'create_organization.html')  # Возвращает страницу снова, можно изменить на redirect


class CreateCompetitorView(CreateView):
    """Добавление участником в определнное соревнование"""
    model = Competitor
    form_class = CreateCompetitorForm
    template_name = 'competitor_form.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        # Получаем текущее соревнование из URL
        competition_id = self.kwargs['pk']
        competition = Competition.objects.get(pk=competition_id)  # Устанавливаем соревнование для участника
        form.instance.competition = competition
        # Устанавливаем текущего пользователя в качестве пользователя участника
        form.instance.user = self.request.user
        # Устанавливаем текущего conductor в качестве кондуктора участника
        form.instance.conductor = Conductor.objects.get(user=self.request.user)
        # количество уже добавленных участников
        current_competitors_count = Competitor.objects.filter(competition=competition).count()
        max_players = competition.max_players

        if current_competitors_count >= max_players:
            # Если количество участников равно или больше максимального, устанавливаю статус участника в резерве
            form.instance.competitor_reserve = True
        else:
            form.instance.competitor_reserve = False

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        competition_id = self.kwargs['pk']
        competition = Competition.objects.get(id=competition_id)
        conductor = Conductor.objects.get(user=self.request.user)
        kwargs['selected_classes'] = competition.get_selected_classes()
        kwargs['conductor'] = conductor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competition_id = self.kwargs['pk']
        competition = Competition.objects.get(pk=competition_id)
        current_competitors_count = Competitor.objects.filter(competition=competition).count()
        max_players = competition.max_players
        if current_competitors_count >= max_players:
            context['competitors_limit_reached'] = True
        else:
            context['competitors_limit_reached'] = False
        context['competition_name'] = competition.name_competition
        return context

    def get_success_url(self):
        competition_id = self.kwargs['pk']
        return reverse('detail_com', kwargs={'pk': competition_id})


class CompetitorDeleteView(DeleteView):
    """Удаление участника"""
    model = Competitor
    template_name = 'competitor_confirm_delete.html'
    success_url = reverse_lazy('index')


class CompetitorUpdateView(UpdateView):
    """Изменение участие, выставление оценок"""
    model = Competitor
    template_name = 'competitor_detail.html'
    form_class = CompetitorUpdateForm
    context_object_name = 'competitor_info'

    def get_success_url(self):
        # Получаем юзер pk
        pk = self.object.pk
        # Строим URL с использованием полученного pk
        return reverse('roles:competitor_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        context['competitor_info'] = self.object
        # Добавляем данные о времени участника в контекст
        context['min_time_competitor'] = self.object.min_time_competitor
        context['sec_time_competitor'] = self.object.sec_time_competitor


        # Получаем список дополнительных оценок для текущего участника
        additional_scores = AdditionalScore.objects.filter(competitor=self.object)
        context['additional_scores'] = additional_scores

        return context

