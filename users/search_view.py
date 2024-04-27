from django.shortcuts import render
from django.views.generic import TemplateView

from roles.models import Judge
from users.models import User, Dogs


class SearchListUsersView(TemplateView):
    template_name = 'users/search_list_users.html'

    def post(self, request, *args, **kwargs):

        search_param = request.POST.get('search', None)

        if search_param:
            users = User.objects.filter(first_name__icontains=search_param) | \
                    User.objects.filter(email__icontains=search_param) | \
                    User.objects.filter(last_name__icontains=search_param)
        else:
            users = User.objects.all()

        context = {'users': users}
        return render(request, self.template_name, context)


class SearchListDogsView(TemplateView):
    template_name = 'users/search_list_dogs.html'

    def post(self, request, *args, **kwargs):

        search_param = request.POST.get('search', None)

        if search_param:
            dogs = Dogs.objects.filter(dog_name__icontains=search_param) | \
                    Dogs.objects.filter(home_name__icontains=search_param) | \
                    Dogs.objects.filter(breed_dog__icontains=search_param) | \
                    Dogs.objects.filter(owner__first_name__icontains=search_param) | \
                    Dogs.objects.filter(owner__last_name__icontains=search_param)

        else:
            dogs = Dogs.objects.all()

        context = {'dogs': dogs}
        return render(request, self.template_name, context)


class SearchListJudgeView(TemplateView):
    template_name = 'users/search_list_judge.html'

    def post(self, request, *args, **kwargs):

        search_param = request.POST.get('search', None)

        if search_param:
            judge = Judge.objects.filter(user__first_name__icontains=search_param) | \
                    Judge.objects.filter(user__last_name__icontains=search_param) | \
                    Judge.objects.filter(user__email__icontains=search_param)

        else:
            judge = Judge.objects.all()

        context = {'judges': judge}
        return render(request, self.template_name, context)
