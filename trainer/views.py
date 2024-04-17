from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from trainer.models import Trainer


# Create your views here.
class TrainerMessageCreateView(CreateView):
    """Создаем сообщение от тренера"""
    model = Trainer
    fields = ('trainer_title', 'trainer_text', 'trainer_banner')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Устанавливаем текущего пользователя как создателя тренера
        return super().form_valid(form)

    def get_success_url(self):
        # Получаем юзер pk
        pk = self.request.user.pk
        # Строим URL с использованием полученного pk
        return reverse('users:user_detail', kwargs={'pk': pk})


class TrainerMessageUpdateView(UpdateView):
    """Меняем сообщение от тренера"""
    model = Trainer
    fields = ('trainer_title', 'trainer_text', 'trainer_banner')

    def get_success_url(self):
        # Получаем юзер pk
        pk = self.request.user.pk
        # Строим URL с использованием полученного pk
        return reverse('users:user_detail', kwargs={'pk': pk})


class TrainerMessageDeleteView(DeleteView):
    """Удаляем сообщение от тренера"""
    model = Trainer

    def get_success_url(self):
        # Получаем юзер pk
        pk = self.request.user.pk
        # Строим URL с использованием полученного pk
        return reverse('users:user_detail', kwargs={'pk': pk})
