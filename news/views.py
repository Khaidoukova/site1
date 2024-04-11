from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from news.models import News
from pytils.translit import slugify


class NewsCreateView(CreateView):
    """Контроллер создания новости"""
    model = News
    fields = ('title', 'body', 'preview', )
    success_url = reverse_lazy('news:list')

    def form_valid(self, form):
        """ Добавляем слаг для формирования удобной ссылки на новость"""
        if form.is_valid():
            self.object = form.save()
            self.object.slug = slugify(self.object.title) # создание уникального slug идентификатора новости
            self.object.save()
        return super().form_valid(form)


class NewsListView(ListView):
    """Контроллер просмотра списка новостей"""
    model = News


class NewsUpdateView(UpdateView):
    """Контроллер изменения отдельной новости"""
    model = News
    fields = ('title', 'body', 'preview',)
    success_url = reverse_lazy('news:list')

    def form_valid(self, form):
        """ Корректируем слаг для формирования удобной ссылки на новость"""
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.slug = slugify(self.object.title)  # Автоматическое обновление slug
            self.object.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('news:view', kwargs={'slug': self.object.slug})


class NewsDetailView(DetailView):
    """Контроллер просмотра отдельной новости"""
    model = News


class NewsDeleteView(DeleteView):
    """Контроллер удаления отдельной новости"""
    model = News
    success_url = reverse_lazy('news:list')


