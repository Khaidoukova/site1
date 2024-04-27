from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from main.models import Competition
from history.models import History
from history.forms import HistoryForm
from roles.models import Competitor
from users.models import Dogs


class HistoryList(ListView):
    """Класс для вывода списка соревнований"""
    model = History
    template_name = 'history/history_list.html'
    context_object_name = 'competitions'

    def get_queryset(self):
        # Получаем текущего пользователя
        user = self.request.user

        # Получаем все соревнования, в которых участвовал пользователь
        competitions = Competition.objects.filter(competitor__user=user).distinct().order_by('-date_competition')

        # Словарь для хранения количества оценок "Отлично" по категориям
        ex_count_dict = {
            'ex_count_ro_dety': 0,
            'ex_count_ro_shenki': 0,
            'ex_count_ro_debut': 0,
            'ex_count_ro_veterany': 0,
            'ex_count_ro_1': 0,
            'ex_count_ro_2': 0,
            'ex_count_ro_3': 0,
            'ex_count_ro_4': 0,
        }
        # Добавляем результаты участия пользователя к каждому соревнованию
        for competition in competitions:
            competition.competitors = Competitor.objects.filter(user=user, competition=competition)
            for competitor in competition.competitors:
                if competitor.grade_competitor == 'Отлично':
                    competition_class = competitor.class_comp
                    ex_count_dict[f'ex_count_{competition_class}'] += 1

        # Подсчитываем количество оценок "Отлично" для объектов History
        history_objects = History.objects.filter(user=user)
        for history_obj in history_objects:
            if history_obj.grade == 'excellent':
                ex_count_dict[f'ex_count_{history_obj.class_dog}'] += 1

        # Обновляем поля в модели User для текущего пользователя
        user.ex_count_ro_dety = ex_count_dict['ex_count_ro_dety']
        user.ex_count_ro_shenki = ex_count_dict['ex_count_ro_shenki']
        user.ex_count_ro_debut = ex_count_dict['ex_count_ro_debut']
        user.ex_count_ro_veterany = ex_count_dict['ex_count_ro_veterany']
        user.ex_count_ro_1 = ex_count_dict['ex_count_ro_1']
        user.ex_count_ro_2 = ex_count_dict['ex_count_ro_2']
        user.ex_count_ro_3 = ex_count_dict['ex_count_ro_3']
        user.ex_count_ro_4 = ex_count_dict['ex_count_ro_4']
        user.save()

        return competitions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_owner = self.request.user
        context['is_owner'] = is_owner

        history = History.objects.order_by('-date_competition')
        context['history'] = history
        return context




class HistoryCreate(CreateView):
    """Класс для добавления других соревнований в свою историю"""
    model = History
    form_class = HistoryForm
    success_url = reverse_lazy('index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)

class HistoryUpdate(UpdateView):
    model = History
    form_class = HistoryForm
    success_url = reverse_lazy('history:history')


class HistoryDelete(DeleteView):
    model = History
    success_url = reverse_lazy('history:history')
