from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, DeleteView
import random

from history.models import History
from main.models import Competition
from roles.models import Judge, Conductor,Competitor
from trainer.models import Trainer
from users.forms import UserRegisterForm, UserProfileForm, DogsForm, UserLoginForm
from users.models import User, Dogs


class DogsCreate(CreateView):
    model = Dogs
    form_class = DogsForm

    def get_success_url(self):
        # Получаем созданный объект Dogs
        created_dogs = self.object
        # Получаем юзер pk
        pk = self.request.user.pk
        # Строим URL с использованием полученного pk
        return reverse('users:user_detail', kwargs={'pk': pk})

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class DogsDetailView(DetailView):
    model = Dogs
    context_object_name = 'dog_info'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog = self.get_object()
        if Competitor.objects.filter(selected_dog=dog):
            # Получаем всех участников собаки
            competitors = Competitor.objects.filter(selected_dog=dog)

            # Получаем все соревнования, в которых участвуют собаки этого участника
            competitions = [competitor.competition for competitor in competitors]

            context['competitions'] = competitions

        # Проверяем, является ли текущий пользователь владельцем собаки
        is_owner = self.request.user == dog.owner
        context['is_owner'] = is_owner

        history = History.objects.filter(user=dog.owner)
        context['user_history'] = history

        return context


class DogsUpdateView(UpdateView):
    model = Dogs
    form_class = DogsForm

    def get_success_url(self):
        # Получаем созданный объект Dogs
        dog = self.object
        # Получаем pk обновленной собаки
        pk = dog.pk
        # Строим URL с использованием полученного pk
        return reverse('dogs_detail', kwargs={'pk': pk})


class DogsDelete(DeleteView):
    """Удаление Соревнования"""
    model = Dogs
    success_url = reverse_lazy('index')

    def get_success_url(self):
        # Получаем pk текущего пользователя
        pk = self.request.user.pk
        # Строим URL с использованием полученного pk
        return reverse('users:user_detail', kwargs={'pk': pk})


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):  # отправляет письмо на почту нового пользователя со ссылкой на авторизацию
        self.object = form.save()
        email_confirm_key = self.object.email_confirm_key
        email_confirm_url = self.request.build_absolute_uri(
            reverse("users:verify_email", kwargs={"key": email_confirm_key}))
        send_mail(
            subject='Вы зарегистрировались на ралли обидиенс',
            message=f'Нужно срочно пройти авторизацию. Пожалуйста, перейдите по ссылке: {email_confirm_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]
        )
        return redirect(self.success_url)


class UserLoginView(LoginView):
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_invalid(self, form):
        messages.error(self.request, 'Вам нужно подтвердить свой почтовый адрес, прежде чем войти.')
        return super().form_invalid(form)


class ProfileView(UpdateView):
    """Изменить профиль"""
    model = User
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        # Получаем юзер pk
        pk = self.request.user.pk
        # Строим URL с использованием полученного pk
        return reverse('users:user_detail', kwargs={'pk': pk})


class UserDetailView(DetailView):
    model = User
    context_object_name = 'object_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        trainer = Trainer.objects.filter(user=user)
        context['trainer'] = trainer

        dogs = Dogs.objects.filter(owner=user)
        context['user_dogs'] = dogs

        competitions = Competition.objects.filter(owner=user)
        context['user_competition'] = competitions

        judge = Judge.objects.filter(user=user).first()
        context['judge_info'] = judge

        conductor = Conductor.objects.filter(user=user).first()
        context['conductor'] = conductor

        history = History.objects.filter(user=user)
        context['user_history'] = history

        # Проверяем, является ли текущий пользователь владельцем страницы
        is_owner = self.request.user == user
        context['is_owner'] = is_owner

        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user = self.get_object()
            # Логика для действия 1
            if 'action1' in request.POST:
                # Меняем значение поля get_check на True
                user.org_status = True
                # Сохраняем изменения
                user.save()

                return redirect('users:user_detail', pk=request.user.pk)

            # Логика для действия 1
            if 'action2' in request.POST:
                judge = Judge.objects.get(user=user)
                # Меняем значение поля get_check на True
                judge.check_admin = True
                # Сохраняем изменения
                judge.save()

                return redirect('users:user_detail', pk=request.user.pk)

        return redirect('users:user_detail', pk=request.user.pk)


def verify_email(request, key):
    user = get_object_or_404(User, email_confirm_key=key)
    user.is_active = True
    user.save()
    return redirect('users:login')


def generate_new_password(request):
    new_password = ''.join(str(random.randint(0, 9)) for _ in range(6))
    send_mail(
        subject='Изменение пароля',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse_lazy('index'))
