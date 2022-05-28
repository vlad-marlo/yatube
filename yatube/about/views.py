from django.views.generic.base import TemplateView


class TechView(TemplateView):
    template_name = 'about/tech.html'


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'
