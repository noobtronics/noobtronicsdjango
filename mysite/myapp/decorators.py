
from django.utils.functional import wraps
import traceback
from products.models import *
from django_q.tasks import async_task
from django.utils import timezone
from django.http import Http404




def staff_or_404(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, raising a 404 if necessary.
    """
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)

        else:
            raise Http404

    return wraps(view_func)(_checklogin)


def url_history_logger(url, csrf_token, referer, remote_addr, mmid, visited):
    if url:
        uhist = UrlHistory(url = url,  mmid = mmid, csrf_token = csrf_token, referer=referer, remote_addr=remote_addr, visited=visited)
        uhist.save()


def log_urlhistory(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, raising a 404 if necessary.
    """
    def _log(request, *args, **kwargs):
        try:
            url = request.META.get('PATH_INFO')
            csrf_token = request.META.get('CSRF_COOKIE')
            referer = request.META.get('HTTP_REFERER')
            mmid = request.COOKIES.get('mmid')
            remote_addr = request.META.get('HTTP_X_REAL_IP')
            visited = timezone.now()
            async_task('myapp.decorators.url_history_logger', url, csrf_token, referer, remote_addr, mmid, visited)

        except:
            traceback.print_exc()
        return view_func(request, *args, **kwargs)

    return wraps(view_func)(_log)
