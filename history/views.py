from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from history.models import History
from history.forms import HistoryForm


class HistoryList(ListView):
    """Класс для вывода списка соревнований"""
    model = History


class HistoryCreate(CreateView):
    """Класс для добавления других соревнований в свою историю"""
    model = History
    form_class = HistoryForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()

        return super().form_valid(form)

