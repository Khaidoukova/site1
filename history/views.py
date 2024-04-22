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
        competitions = Competition.objects.filter(competitor__user=user).order_by('-date_competition')
        # Добавляем результаты участия пользователя к каждому соревнованию
        for competition in competitions:
            competitors = Competitor.objects.filter(user=user, competition=competition)
            for competitor in competitors:
                competitor.class_comp = competitor.get_class_comp_display()


        return competitions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

