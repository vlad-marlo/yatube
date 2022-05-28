from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserCreationForm


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'
