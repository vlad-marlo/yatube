from django.conf import settings as s
from django.core.paginator import Paginator


def paginator(request, post_list):
    paginator_ = Paginator(post_list, s.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator_.get_page(page_number)
    return page_obj
